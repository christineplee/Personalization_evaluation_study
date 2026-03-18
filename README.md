# Study 2: Content-Specific Personalization — Dose-Response

Follow-up to Study 1 (Minimal Effective Question Set). Investigates whether
adding content-specific questions on top of the 16-item style profile improves
personalization, and at what point additional questions become a burden.

## Quick Start (Local)

**Terminal 1 — Backend:**
```bash
cd study2/backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # Edit with Azure credentials, or leave for demo mode
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd study2/frontend
npm install
npm start
```

Open http://localhost:3000. Demo mode shows `[DEMO]` placeholders if no Azure key is set.

## Study Design

**Research Questions:**
1. Does adding content-specific questions improve personalization beyond the style profile?
2. How many content questions before diminishing returns / burden?
3. What types of content questions are most valuable? (post-hoc coding)

**Design:** Between-subjects, 5 conditions × 50 participants = 250 total.

| Condition | Profile (16 items) | Content Questions | Description |
|-----------|--------------------|-------------------|-------------|
| NP        | No                 | 0                 | Pure baseline — no personalization |
| P0        | Yes                | 0                 | Profile only (Study 1 replication) |
| P3        | Yes                | 3                 | Profile + 3 content Qs per task |
| P6        | Yes                | 6                 | Profile + 6 content Qs per task |
| P10       | Yes                | 10                | Profile + 10 content Qs per task |

**Content questions** are pre-generated (GATE-style open-ended questions converted
to multiple-choice for Prolific). Questions are nested: P3 sees Q1–3, P6 sees
Q1–6, P10 sees Q1–10. This allows post-hoc coding of question types (situational,
preference, goal) to analyze which types contribute most to satisfaction.

**Tasks (3 per participant, randomized order):**
1. Planning: Meal planning for a busy non-cook
2. Advice: Navigating a friendship that's fading
3. Creative: Writing a thank-you message

**Measures (per task):**
- Content fit (1–7): "The response addressed my specific situation and needs"
- Perceived personalization (1–7): "This felt written for someone like me"
- Satisfaction (1–7): "Overall, I am satisfied with this response"
- Effort (1–7): "Getting a response that fit my needs felt easy and low-effort"
- Open-ended: "What would you change?"

All scales: higher = better. No reverse coding needed.

## Participant Flow

```
Prolific → Welcome

Condition NP:          Conditions P0–P10:
Skip profile           Answer 16-item profile
    │                       │
    ▼                       ▼
For each of 3 tasks:

NP / P0:               P3 / P6 / P10:
No content Qs          Answer 3/6/10 content Qs (multiple choice)
    │                       │
    ▼                       ▼
Buffer (LLM generates response)
    │
    ▼
Evaluate response (4 Likert + open-ended)
    │
    ▼
Next task...

Post-study questionnaire → Thank you / Prolific redirect
```

## Architecture

```
study2/
├── backend/
│   ├── main.py              # API routes, 5-condition logic, LLM integration
│   ├── questions.py         # 16 profile items, 3 tasks, 10 content Qs/task, eval scales
│   ├── requirements.txt
│   ├── .env.example
│   └── data/study.db        # Created at runtime
└── frontend/
    ├── public/index.html
    ├── package.json
    └── src/
        ├── App.js           # All phases: welcome → profile → content Qs → buffer → eval → post
        ├── App.css
        └── index.js
```

## API Endpoints

| Method | Path                     | Description |
|--------|--------------------------|-------------|
| GET    | `/api/questions`         | Profiling questions + attention checks |
| GET    | `/api/content-questions` | All content questions by task |
| GET    | `/api/evaluation-items`  | Evaluation scales |
| POST   | `/api/session/create`    | Create session, assign condition |
| POST   | `/api/profiling/submit`  | Store profile answers |
| POST   | `/api/task/generate`     | Generate LLM response for one task |
| POST   | `/api/evaluation/submit` | Store task evaluation |
| POST   | `/api/post-study/submit` | Store post-study data |
| GET    | `/api/admin/export`      | Export all data |
| GET    | `/api/admin/status`      | Counts by condition |

## Data Export

`/api/admin/export` includes per-response:
- `content_question_ids`: which content Qs were shown (for post-hoc type coding)
- `content_answers`: participant's selected options
- `system_prompt`: exact prompt sent to LLM
- `llm_response`: LLM output

## Analysis Plan

**Primary:** Linear regression with question count (0, 3, 6, 10) as predictor,
plus a separate comparison of NP vs P0 to validate the profile effect.
Quadratic term to test for diminishing returns.

**Secondary:** Post-hoc coding of content questions by type (situational,
preference, goal). Mixed-effects model with question type as predictor of
per-question marginal contribution to satisfaction.

**Qualitative:** Thematic analysis of open-ended responses + post-study
"How would you prefer to provide this information?" question.
