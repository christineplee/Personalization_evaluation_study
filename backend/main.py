"""
Study 2: Content-Specific Personalization -- Dose-Response.
Per-task generation flow. Participants choose 3 of 8 tasks.
"""

import json, os, random, sqlite3, time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional, List

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import AzureOpenAI

from questions import PROFILING_QUESTIONS, TASKS, CONTENT_QUESTIONS, EVALUATION_ITEMS, ATTENTION_CHECKS, get_profiling_questions_with_attention_checks

AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "https://YOUR-RESOURCE.openai.azure.com/")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
DB_PATH = os.getenv("DB_PATH", "data/study.db")
PROLIFIC_REDIRECT_URL = os.getenv("PROLIFIC_REDIRECT_URL", "")

CONDITIONS = {
    "NP":  {"profile": False, "num_content_qs": 0},
    "P0":  {"profile": True,  "num_content_qs": 0},
    "P3":  {"profile": True,  "num_content_qs": 3},
    "P6":  {"profile": True,  "num_content_qs": 6},
    "P10": {"profile": True,  "num_content_qs": 10},
}
CONDITION_KEYS = list(CONDITIONS.keys())

# Build a lookup dict for tasks by ID
TASK_LOOKUP = {t["id"]: t for t in TASKS}

app = FastAPI(title="Personalization Dose-Response Study")
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# ── Database ──────────────────────────────────────────────────────────────────

def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY, condition TEXT NOT NULL,
                created_at TEXT NOT NULL, status TEXT DEFAULT 'profiling',
                selected_tasks TEXT, profiling_data TEXT, post_study_data TEXT, prolific_pid TEXT
            );
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL,
                task_id TEXT NOT NULL, task_index INTEGER NOT NULL,
                content_question_ids TEXT, content_answers TEXT,
                system_prompt TEXT NOT NULL, llm_response TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            );
            CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL,
                task_id TEXT NOT NULL, eval_content_fit INTEGER, eval_personalization INTEGER,
                eval_satisfaction INTEGER, eval_effort INTEGER, eval_relevance INTEGER,
                open_ended TEXT, created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            );
            CREATE TABLE IF NOT EXISTS attention_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT NOT NULL,
                check_id TEXT NOT NULL, expected INTEGER NOT NULL, actual INTEGER NOT NULL,
                passed INTEGER NOT NULL, created_at TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            );
        """)

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

# ── Condition Assignment ──────────────────────────────────────────────────────

def assign_condition():
    with get_db() as conn:
        counts = {c: conn.execute("SELECT COUNT(*) FROM sessions WHERE condition=?", (c,)).fetchone()[0] for c in CONDITION_KEYS}
    min_count = min(counts.values())
    return random.choice([c for c, n in counts.items() if n == min_count])

# ── LLM ───────────────────────────────────────────────────────────────────────

def get_llm_client():
    if not AZURE_API_KEY or AZURE_API_KEY == "your-api-key-here":
        return None
    return AzureOpenAI(azure_endpoint=AZURE_ENDPOINT, api_key=AZURE_API_KEY, api_version=AZURE_API_VERSION)

def generate_llm_response(system_prompt, user_message):
    client = get_llm_client()
    if client is None:
        return f"[DEMO MODE] This is a placeholder response to: '{user_message}'. In production, this would be a personalized LLM response generated using the participant's profile. The system prompt contains {system_prompt.count(chr(10))} lines of profile information."
    response = client.chat.completions.create(
        model=AZURE_DEPLOYMENT,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
        temperature=0.7, max_tokens=1024,
    )
    return response.choices[0].message.content

# ── Prompt Construction (exact Study 1 wording) ──────────────────────────────

def build_profile_lines(profile_answers):
    lines = []
    for q in PROFILING_QUESTIONS:
        answer = profile_answers.get(q["id"])
        if answer is None:
            continue
        if q["type"] == "bipolar7":
            left = q.get("left_anchor", "")
            right = q.get("right_anchor", "")
            lines.append(f'- Scenario: {q["text"]} -- On a scale from "{left}" (1) to "{right}" (7), this user chose: {answer}/7')
        elif q["type"] == "likert6":
            a = q.get("anchors", ["1", "6"])
            lines.append(f'- {q["text"]} -- Response: {answer}/6 ({a[0]} to {a[1]})')
        elif q["type"] == "likert5":
            a = q.get("anchors", ["1", "5"])
            stem = q.get("stem", "")
            display = f"{stem} {q['text']}" if stem else q["text"]
            lines.append(f'- "{display}" -- Response: {answer}/5 ({a[0]} to {a[1]})')
        elif q["type"] == "forced_choice":
            if isinstance(answer, int) and "options" in q:
                answer_text = q["options"][answer] if answer < len(q["options"]) else str(answer)
            else:
                answer_text = str(answer)
            lines.append(f'- {q["text"]} -- Chose: "{answer_text}"')
    return "\n".join(lines)

def build_content_lines(task_id, content_answers):
    task_cqs = CONTENT_QUESTIONS.get(task_id, [])
    lines = []
    for cq in task_cqs:
        answer = content_answers.get(cq["id"])
        if answer is None:
            continue
        if isinstance(answer, int) and answer < len(cq["options"]):
            answer_text = cq["options"][answer]
        else:
            answer_text = str(answer)
        lines.append(f'- {cq["text"]} -- "{answer_text}"')
    return "\n".join(lines)

def build_system_prompt(has_profile, profile_answers, task_id, content_answers):
    if not has_profile and not content_answers:
        return "You are a helpful AI assistant."

    profile_section = build_profile_lines(profile_answers) if has_profile else ""
    content_section = build_content_lines(task_id, content_answers) if content_answers else ""

    if has_profile and profile_section:
        prompt = f"""You are a helpful AI assistant. You have been given information about the user you are about to interact with. Use this information to strongly adapt your response along four dimensions:

1. TONE: How warm/cold, formal/casual, supportive/direct should you be? Pay attention to their preferences about emotional acknowledgment, formality, and communication style.

2. VERBOSITY: How much detail should you provide? Some users want concise key points, others want comprehensive explanations. Adjust the length and depth of your response accordingly.

3. STRUCTURE: How should you organize your response? Some users prefer bullet points, headers, and structured layouts. Others prefer flowing conversational prose. Match their preference.

4. INITIATIVE: How proactive should you be? Some users want you to anticipate needs, suggest next steps, and flag things they haven't asked about. Others want you to answer exactly what was asked and nothing more.

USER PROFILE:
{profile_section}

IMPORTANT: Make strong, clear adaptations based on this profile. Two users with different profiles should receive noticeably different responses to the same question. Do not default to a generic middle-ground style. Do not mention that you have this profile information or refer to it explicitly."""
    else:
        prompt = "You are a helpful AI assistant."

    if content_section:
        prompt += f"""

The user was also asked specific questions about their situation and needs for this particular request. Use this information to tailor the CONTENT of your response to their specific circumstances:

USER'S SITUATION:
{content_section}

Use both the user profile AND these situational details to craft a highly personalized response. The profile captures who this user is and how they prefer to communicate. The situational details capture the specifics of this particular request. Both should influence what you say and how you say it."""

    return prompt

# ── Pydantic Models ───────────────────────────────────────────────────────────

class CreateSessionRequest(BaseModel):
    prolific_pid: Optional[str] = None

class TaskSelectionRequest(BaseModel):
    session_id: str
    selected_task_ids: List[str]  # exactly 3 task IDs

class ProfilingSubmission(BaseModel):
    session_id: str
    answers: dict

class TaskGenerateRequest(BaseModel):
    session_id: str
    task_index: int  # 0, 1, or 2 (index into selected_tasks)
    content_answers: dict = {}

class EvaluationSubmission(BaseModel):
    session_id: str
    task_id: str
    eval_content_fit: int
    eval_personalization: int
    eval_satisfaction: int
    eval_effort: int
    eval_relevance: int
    open_ended: str = ""

class PostStudySubmission(BaseModel):
    session_id: str
    data: dict

class AttentionCheckSubmission(BaseModel):
    session_id: str
    check_id: str
    expected: int
    actual: int

# ── API Routes ────────────────────────────────────────────────────────────────

@app.on_event("startup")
def startup():
    init_db()
    if AZURE_API_KEY and AZURE_API_KEY != "your-api-key-here":
        print(f"  Azure OpenAI configured: {AZURE_ENDPOINT} (deployment: {AZURE_DEPLOYMENT})")
    else:
        print("  Running in DEMO MODE -- set AZURE_OPENAI_API_KEY in .env for real LLM responses")

@app.get("/api/questions")
def get_questions():
    eval_attn_checks = {str(ac["in_task"]): ac for ac in ATTENTION_CHECKS if ac.get("in_task") is not None}
    return {"questions": get_profiling_questions_with_attention_checks(), "eval_attention_checks": eval_attn_checks}

@app.get("/api/evaluation-items")
def get_evaluation_items():
    return {"items": EVALUATION_ITEMS}

@app.get("/api/content-questions")
def get_content_questions():
    return {"content_questions": CONTENT_QUESTIONS}

@app.get("/api/tasks")
def get_all_tasks():
    """Return all 8 tasks for the task selection screen."""
    return {"tasks": [{"id": t["id"], "prompt": t["prompt"], "category": t["category"], "short_label": t["short_label"]} for t in TASKS]}

@app.post("/api/session/create")
def create_session(request: CreateSessionRequest = CreateSessionRequest()):
    condition = assign_condition()
    session_id = f"s2_{int(time.time()*1000)}_{random.randint(1000,9999)}"
    cond = CONDITIONS[condition]
    with get_db() as conn:
        conn.execute("INSERT INTO sessions (session_id, condition, created_at, prolific_pid) VALUES (?,?,?,?)",
                     (session_id, condition, datetime.utcnow().isoformat(), request.prolific_pid))
    return {"session_id": session_id, "condition": condition, "has_profile": cond["profile"],
            "num_content_qs": cond["num_content_qs"],
            "all_tasks": [{"id": t["id"], "prompt": t["prompt"], "category": t["category"], "short_label": t["short_label"]} for t in TASKS],
            "prolific_redirect_url": PROLIFIC_REDIRECT_URL}

@app.post("/api/tasks/select")
def select_tasks(request: TaskSelectionRequest):
    """Store the participant's 3 chosen tasks."""
    if len(request.selected_task_ids) != 3:
        raise HTTPException(status_code=400, detail="Must select exactly 3 tasks")
    for tid in request.selected_task_ids:
        if tid not in TASK_LOOKUP:
            raise HTTPException(status_code=400, detail=f"Unknown task: {tid}")
    with get_db() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id=?", (request.session_id,)).fetchone()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        conn.execute("UPDATE sessions SET selected_tasks=? WHERE session_id=?",
                     (json.dumps(request.selected_task_ids), request.session_id))
    return {"status": "ok", "selected_tasks": request.selected_task_ids}

@app.post("/api/profiling/submit")
def submit_profiling(submission: ProfilingSubmission):
    with get_db() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id=?", (submission.session_id,)).fetchone()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        conn.execute("UPDATE sessions SET profiling_data=?, status='tasks' WHERE session_id=?",
                     (json.dumps(submission.answers), submission.session_id))
        for ac in ATTENTION_CHECKS:
            if ac.get("insert_after") and ac["id"] in submission.answers:
                actual = submission.answers[ac["id"]]
                expected = ac["expected_answer"]
                passed = 1 if actual == expected else 0
                conn.execute("INSERT INTO attention_checks (session_id, check_id, expected, actual, passed, created_at) VALUES (?,?,?,?,?,?)",
                             (submission.session_id, ac["id"], expected, actual, passed, datetime.utcnow().isoformat()))
    return {"status": "ok"}

@app.post("/api/task/generate")
def generate_task(request: TaskGenerateRequest):
    """Generate ONE LLM response. task_index is 0/1/2 into the participant's selected_tasks."""
    with get_db() as conn:
        session = conn.execute("SELECT * FROM sessions WHERE session_id=?", (request.session_id,)).fetchone()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

    condition = session["condition"]
    cond = CONDITIONS[condition]
    selected_tasks = json.loads(session["selected_tasks"]) if session["selected_tasks"] else []

    if request.task_index >= len(selected_tasks):
        raise HTTPException(status_code=400, detail="Invalid task index")

    task_id = selected_tasks[request.task_index]
    task = TASK_LOOKUP[task_id]

    profile_answers = json.loads(session["profiling_data"]) if session["profiling_data"] else {}

    system_prompt = build_system_prompt(
        has_profile=cond["profile"],
        profile_answers=profile_answers,
        task_id=task["id"],
        content_answers=request.content_answers,
    )

    llm_response = generate_llm_response(system_prompt, task["prompt"])

    task_cqs = CONTENT_QUESTIONS.get(task["id"], [])
    shown_cq_ids = [cq["id"] for cq in task_cqs[:cond["num_content_qs"]]]

    with get_db() as conn:
        conn.execute(
            """INSERT INTO responses (session_id, task_id, task_index, content_question_ids, content_answers, system_prompt, llm_response, created_at)
               VALUES (?,?,?,?,?,?,?,?)""",
            (request.session_id, task["id"], request.task_index, json.dumps(shown_cq_ids),
             json.dumps(request.content_answers), system_prompt, llm_response, datetime.utcnow().isoformat()))

    return {"task_id": task["id"], "task_index": request.task_index, "category": task["category"],
            "prompt": task["prompt"], "response": llm_response, "content_question_ids": shown_cq_ids}

@app.post("/api/evaluation/submit")
def submit_evaluation(submission: EvaluationSubmission):
    with get_db() as conn:
        conn.execute(
            """INSERT INTO evaluations (session_id, task_id, eval_content_fit, eval_personalization, eval_satisfaction, eval_effort, eval_relevance, open_ended, created_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (submission.session_id, submission.task_id, submission.eval_content_fit, submission.eval_personalization,
             submission.eval_satisfaction, submission.eval_effort, submission.eval_relevance, submission.open_ended, datetime.utcnow().isoformat()))
    return {"status": "ok"}

@app.post("/api/post-study/submit")
def submit_post_study(submission: PostStudySubmission):
    with get_db() as conn:
        conn.execute("UPDATE sessions SET post_study_data=?, status='complete' WHERE session_id=?",
                     (json.dumps(submission.data), submission.session_id))
    return {"status": "ok"}

@app.post("/api/attention-check/submit")
def submit_attention_check(submission: AttentionCheckSubmission):
    passed = 1 if submission.actual == submission.expected else 0
    with get_db() as conn:
        conn.execute("INSERT INTO attention_checks (session_id, check_id, expected, actual, passed, created_at) VALUES (?,?,?,?,?,?)",
                     (submission.session_id, submission.check_id, submission.expected, submission.actual, passed, datetime.utcnow().isoformat()))
    return {"status": "ok", "passed": bool(passed)}

@app.get("/api/admin/export")
def export_data():
    with get_db() as conn:
        return {"sessions": [dict(r) for r in conn.execute("SELECT * FROM sessions").fetchall()],
                "responses": [dict(r) for r in conn.execute("SELECT * FROM responses").fetchall()],
                "evaluations": [dict(r) for r in conn.execute("SELECT * FROM evaluations").fetchall()],
                "attention_checks": [dict(r) for r in conn.execute("SELECT * FROM attention_checks").fetchall()],
                "questions": PROFILING_QUESTIONS, "tasks": TASKS, "content_questions": CONTENT_QUESTIONS, "conditions": CONDITIONS}

@app.get("/api/admin/status")
def study_status():
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        complete = conn.execute("SELECT COUNT(*) FROM sessions WHERE status='complete'").fetchone()[0]
        by_condition = {c: conn.execute("SELECT COUNT(*) FROM sessions WHERE condition=?", (c,)).fetchone()[0] for c in CONDITION_KEYS}
    return {"total_sessions": total, "complete": complete, "by_condition": by_condition}

