import React, { useState, useEffect } from 'react';
import './App.css';

const API = process.env.REACT_APP_API_URL || '';

async function api(path, options = {}) {
  const res = await fetch(`${API}${path}`, { headers: { 'Content-Type': 'application/json' }, ...options });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

function renderMarkdown(text) {
  if (!text) return '';
  let html = text
    .replace(/^### \*?\*?(.*?)\*?\*?\s*$/gm, '<h3>$1</h3>')
    .replace(/^## \*?\*?(.*?)\*?\*?\s*$/gm, '<h2>$1</h2>')
    .replace(/^# \*?\*?(.*?)\*?\*?\s*$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/^- (.*$)/gm, '<li>$1</li>')
    .replace(/^\d+\. (.*$)/gm, '<li>$1</li>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br/>');
  html = html.replace(/((?:<li>.*?<\/li>\s*(?:<br\/>)?)+)/g, '<ul>$1</ul>');
  html = html.replace(/<ul>(.*?)<\/ul>/gs, (m, inner) => '<ul>' + inner.replace(/<br\/>/g, '') + '</ul>');
  return '<p>' + html + '</p>';
}

/* ── Welcome ────────────────────────────────────────────────────────── */

function Welcome({ onStart }) {
  return (
    <div className="phase welcome">
      <div className="card wide">
        <h1>AI Personalization Study</h1>
        <p className="subtitle">Exploring how AI assistants can better adapt to <em>you</em></p>
        <div className="welcome-body">
          <p>In this study, you may answer questions about yourself, then work through 3 tasks with an AI assistant. You'll evaluate how well each response fits your needs.</p>
          <div className="info-box">
            <strong>What to expect:</strong>
            <ul>
              <li>Part 1: Answer questions about your preferences and personality</li>
              <li>Part 2: Work through 3 AI tasks and evaluate the responses</li>
              <li>Part 3: A few final reflection questions</li>
            </ul>
          </div>
          <p className="note">Your responses are stored with an anonymous ID. No personally identifiable information is collected.</p>
        </div>
        <button className="btn primary" onClick={onStart}>Begin Study</button>
      </div>
    </div>
  );
}

/* ── Profiling (same as Study 1, updated tiers) ─────────────────────── */

const TIER_LABELS = { primals: 'World Beliefs', bigfive: 'Personality', projective: 'Scenarios & Choices', vignettes: 'Communication Preferences' };
const TIER_ORDER = ['primals', 'bigfive', 'projective', 'vignettes'];
const TIER_INSTRUCTIONS = {
  primals: 'Rate how much you agree or disagree with each statement about the world.',
  bigfive: 'Rate how well each statement describes you as a person.',
  projective: 'For each question, choose the option that feels more like you. There are no right or wrong answers.',
  vignettes: 'For each scenario, imagine you are interacting with an AI assistant. The two descriptions represent different styles. Choose where your preference falls on the scale.',
};

function QuestionRenderer({ question, value, onChange }) {
  const { id, type, text, options, anchors } = question;
  if (type === 'bipolar7') {
    return (
      <div className="question">
        <p className="q-text q-scenario">{text}</p>
        <div className="bipolar-poles">
          <div className={'pole pole-left' + (value && value <= 3 ? ' pole-active' : '')}>
            <span className="pole-label">{question.left_anchor}</span>
          </div>
          <div className={'pole pole-right' + (value && value >= 5 ? ' pole-active' : '')}>
            <span className="pole-label">{question.right_anchor}</span>
          </div>
        </div>
        <div className="bipolar-scale">
          <div className="likert-buttons">
            {[1,2,3,4,5,6,7].map(v => <button key={v} className={'likert-btn' + (value === v ? ' selected' : '')} onClick={() => onChange(id, v)}>{v}</button>)}
          </div>
        </div>
      </div>
    );
  }
  if (type === 'likert5') {
    return (
      <div className="question">
        {question.stem && <p className="q-stem">{question.stem}</p>}
        <p className="q-text">{text}</p>
        <div className="likert-row">
          <span className="anchor left">{anchors?.[0]}</span>
          <div className="likert-buttons">
            {[1,2,3,4,5].map(v => <button key={v} className={'likert-btn' + (value === v ? ' selected' : '')} onClick={() => onChange(id, v)}>{v}</button>)}
          </div>
          <span className="anchor right">{anchors?.[1]}</span>
        </div>
      </div>
    );
  }
  if (type === 'likert6' || type === 'likert7') {
    const max = type === 'likert7' ? 7 : 6;
    return (
      <div className="question">
        <p className="q-text">{text}</p>
        <div className="likert-row">
          <span className="anchor left">{anchors?.[0]}</span>
          <div className="likert-buttons">
            {Array.from({length: max}, (_, i) => <button key={i+1} className={'likert-btn' + (value === i+1 ? ' selected' : '')} onClick={() => onChange(id, i+1)}>{i+1}</button>)}
          </div>
          <span className="anchor right">{anchors?.[1]}</span>
        </div>
      </div>
    );
  }
  if (type === 'forced_choice') {
    return (
      <div className="question">
        <p className="q-text">{text}</p>
        <div className="choice-versus">
          <button className={'choice-card' + (value === 0 ? ' selected' : '')} onClick={() => onChange(id, 0)}>{options[0]}</button>
          <div className="choice-or">or</div>
          <button className={'choice-card' + (value === 1 ? ' selected' : '')} onClick={() => onChange(id, 1)}>{options[1]}</button>
        </div>
      </div>
    );
  }
  return <p>Unknown type: {type}</p>;
}

function Profiling({ questions, onSubmit }) {
  const [answers, setAnswers] = useState({});
  const [currentTier, setCurrentTier] = useState(0);
  const tiers = TIER_ORDER.filter(t => questions.some(q => q.tier === t));
  const currentTierQs = questions.filter(q => q.tier === tiers[currentTier]);
  const tierDone = currentTierQs.every(q => { const v = answers[q.id]; return q.type === 'forced_choice' ? v !== undefined : v !== undefined && v !== ''; });
  const total = questions.filter(q => { const v = answers[q.id]; return q.type === 'forced_choice' ? v !== undefined : v !== undefined && v !== ''; }).length;

  return (
    <div className="phase profiling">
      <div className="card wide">
        <div className="progress-bar"><div className="progress-fill" style={{ width: `${(total / questions.length) * 100}%` }} /></div>
        <div className="tier-nav">
          {tiers.map((t, i) => <button key={t} className={'tier-tab' + (i === currentTier ? ' active' : '') + (i < currentTier ? ' done' : '')} onClick={() => i <= currentTier && setCurrentTier(i)}>{TIER_LABELS[t]}</button>)}
        </div>
        <h2>{TIER_LABELS[tiers[currentTier]]}</h2>
        {TIER_INSTRUCTIONS[tiers[currentTier]] && <p className="tier-instructions">{TIER_INSTRUCTIONS[tiers[currentTier]]}</p>}
        <p className="tier-progress">{total} of {questions.length} questions answered</p>
        <div className="questions-list">
          {currentTierQs.map(q => <QuestionRenderer key={q.id} question={q} value={answers[q.id]} onChange={(id, v) => setAnswers(p => ({...p, [id]: v}))} />)}
        </div>
        <div className="nav-buttons">
          {currentTier > 0 && <button className="btn secondary" onClick={() => setCurrentTier(p => p - 1)}>Previous Section</button>}
          {currentTier < tiers.length - 1
            ? <button className="btn primary" disabled={!tierDone} onClick={() => setCurrentTier(p => p + 1)}>Next Section</button>
            : <button className="btn primary" disabled={total < questions.length} onClick={() => onSubmit(answers)}>Submit & Continue</button>}
        </div>
      </div>
    </div>
  );
}

/* ── Content Questions (per task) ────────────────────────────────────── */

function TaskContentQuestions({ task, contentQuestions, numContentQs, taskIndex, totalTasks, onSubmit }) {
  const [answers, setAnswers] = useState({});
  const cqs = (contentQuestions[task.id] || []).slice(0, numContentQs);
  const allDone = cqs.every(cq => answers[cq.id] !== undefined);

  return (
    <div className="phase content-questions">
      <div className="card wide">
        <div className="progress-bar"><div className="progress-fill" style={{ width: `${(taskIndex / totalTasks) * 100}%` }} /></div>
        <p className="task-counter">Task {taskIndex + 1} of {totalTasks} - Help the AI Understand Your Situation</p>
        <div className="task-prompt-box">
          <span className="label">Your request to the AI:</span>
          <p className="task-prompt-text">{task.prompt}</p>
        </div>
        <div className="content-q-intro"><p>Before the AI generates a response, please answer these questions about your situation so it can better tailor its answer to you:</p></div>
        {cqs.map((cq, i) => (
          <div key={cq.id} className="content-q-item">
            <p className="content-q-text">{i + 1}. {cq.text}</p>
            <div className="content-q-options">
              {cq.options.map((opt, oi) => <button key={oi} className={'content-q-option' + (answers[cq.id] === oi ? ' selected' : '')} onClick={() => setAnswers(p => ({...p, [cq.id]: oi}))}>{opt}</button>)}
            </div>
          </div>
        ))}
        <button className="btn primary" disabled={!allDone} onClick={() => onSubmit(answers)}>Submit & Generate Response</button>
      </div>
    </div>
  );
}

/* ── Buffer ───────────────────────────────────────────────────────────── */

function Buffer() {
  return (
    <div className="phase buffer">
      <div className="card">
        <div className="spinner" />
        <h2>Preparing Your Response</h2>
        <p>Generating a personalized response based on your profile...</p>
        <p className="note">This usually takes 15-30 seconds.</p>
      </div>
    </div>
  );
}

/* ── Task Evaluation (single task) ───────────────────────────────────── */

function TaskEval({ taskData, taskIndex, totalTasks, attnCheck, onSubmit }) {
  const [ratings, setRatings] = useState({});
  const [relevance, setRelevance] = useState(null);
  const [openEnded, setOpenEnded] = useState('');
  const dims = ['content_fit', 'personalization', 'satisfaction', 'effort'];
  const labels = {
    content_fit: 'The response addressed my specific situation and needs, not just the general topic.',
    personalization: 'This response felt like it was written for someone like me, not a generic answer.',
    satisfaction: 'Overall, I am satisfied with this response.',
    effort: 'Getting a response that fit my needs felt easy and low-effort.',
  };
  const items = [];
  Object.entries(labels).forEach(([dim, label], idx) => {
    items.push({ key: dim, label });
    if (idx === 1 && attnCheck) items.push({ key: '_attn', label: attnCheck.text });
  });
  const allRated = dims.every(d => ratings[d] !== undefined) && relevance !== null && (!attnCheck || ratings['_attn'] !== undefined);

  return (
    <div className="phase evaluation">
      <div className="card wide">
        <div className="progress-bar"><div className="progress-fill" style={{ width: `${((taskIndex + 0.5) / totalTasks) * 100}%` }} /></div>
        <p className="task-counter">Task {taskIndex + 1} of {totalTasks} - Evaluate the Response</p>
        <div className="task-section">
          <div className="task-prompt"><span className="label">Your question to the AI:</span><p>{taskData.prompt}</p></div>
          <div className="task-response"><span className="label">AI Response:</span><div className="response-text" dangerouslySetInnerHTML={{ __html: renderMarkdown(taskData.response) }} /></div>
        </div>
        <div className="eval-section">
          <div className="eval-item relevance-item">
            <p className="eval-label">How relevant is this topic to you personally?</p>
            <div className="likert-row compact">
              <span className="anchor left">Not at all</span>
              <div className="likert-buttons">
                {[1,2,3,4,5,6,7].map(v => <button key={v} className={'likert-btn' + (relevance === v ? ' selected' : '')} onClick={() => setRelevance(v)}>{v}</button>)}
              </div>
              <span className="anchor right">Very relevant</span>
            </div>
          </div>
          <h3>How well did this response fit you?</h3>
          <p className="eval-instructions">Rate each statement from 1 (Strongly Disagree) to 7 (Strongly Agree)</p>
          {items.map(({ key, label }) => (
            <div key={key} className="eval-item">
              <p className="eval-label">{label}</p>
              <div className="likert-row compact">
                <span className="anchor left">Disagree</span>
                <div className="likert-buttons">
                  {[1,2,3,4,5,6,7].map(v => <button key={v} className={'likert-btn' + (ratings[key] === v ? ' selected' : '')} onClick={() => setRatings(p => ({...p, [key]: v}))}>{v}</button>)}
                </div>
                <span className="anchor right">Agree</span>
              </div>
            </div>
          ))}
          <div className="open-ended-section">
            <label className="eval-label">In one sentence, what would you change about this response?</label>
            <textarea className="free-text" rows={2} placeholder="Optional - but very helpful for our research" value={openEnded} onChange={e => setOpenEnded(e.target.value)} />
          </div>
          <button className="btn primary" disabled={!allRated} onClick={() => onSubmit({ ratings, relevance, openEnded, attnRating: ratings['_attn'] })}>
            {taskIndex < totalTasks - 1 ? 'Next Task' : 'Finish Evaluation'}
          </button>
        </div>
      </div>
    </div>
  );
}

/* ── Post-Study ───────────────────────────────────────────────────────── */

function PostStudy({ onSubmit }) {
  const [data, setData] = useState({ overall_quality: null, prefer_personalized: null, what_helped: '', what_missing: '', how_prefer_to_provide: '' });
  const complete = data.overall_quality !== null && data.prefer_personalized !== null;
  return (
    <div className="phase post-study">
      <div className="card wide">
        <h2>Final Reflections</h2>
        <p>Almost done - a few last questions about your overall experience.</p>
        <div className="question">
          <p className="q-text">Overall, how would you rate the quality of the AI's responses?</p>
          <div className="likert-row">
            <span className="anchor left">Very poor</span>
            <div className="likert-buttons">
              {[1,2,3,4,5,6,7].map(v => <button key={v} className={'likert-btn' + (data.overall_quality === v ? ' selected' : '')} onClick={() => setData(p => ({...p, overall_quality: v}))}>{v}</button>)}
            </div>
            <span className="anchor right">Excellent</span>
          </div>
        </div>
        <div className="question">
          <p className="q-text">Would you prefer an AI that adapts to you like this over a generic AI assistant?</p>
          <div className="choice-list">
            {['Strongly prefer personalized', 'Slightly prefer personalized', 'No preference', 'Slightly prefer generic', 'Strongly prefer generic'].map((opt, i) =>
              <button key={i} className={'choice-btn' + (data.prefer_personalized === i ? ' selected' : '')} onClick={() => setData(p => ({...p, prefer_personalized: i}))}>{opt}</button>)}
          </div>
        </div>
        <div className="question">
          <p className="q-text">What about the AI's responses felt most personalized to you?</p>
          <textarea className="free-text" rows={2} value={data.what_helped} onChange={e => setData(p => ({...p, what_helped: e.target.value}))} placeholder="e.g., It understood my specific dietary needs..." />
        </div>
        <div className="question">
          <p className="q-text">What information do you wish the AI had known about you or your situation?</p>
          <textarea className="free-text" rows={2} value={data.what_missing} onChange={e => setData(p => ({...p, what_missing: e.target.value}))} placeholder="e.g., My budget, my schedule constraints..." />
        </div>
        <div className="question">
          <p className="q-text">How would you prefer to provide this kind of information to an AI in the future?</p>
          <textarea className="free-text" rows={2} value={data.how_prefer_to_provide} onChange={e => setData(p => ({...p, how_prefer_to_provide: e.target.value}))} placeholder="e.g., Through a conversation, a questionnaire, by example..." />
        </div>
        <button className="btn primary" disabled={!complete} onClick={() => onSubmit(data)}>Submit & Finish</button>
      </div>
    </div>
  );
}

/* ── Thank You ────────────────────────────────────────────────────────── */

function ThankYou({ sessionId, prolificRedirectUrl }) {
  return (
    <div className="phase thank-you">
      <div className="card">
        <h1>Thank You!</h1>
        <p>Your responses have been recorded.</p>
        <div className="info-box"><p><strong>Session ID:</strong> {sessionId}</p><p>Please save this ID in case you need to reference your participation.</p></div>
        <p className="note">This study investigates how different levels of personalization information affect the quality of AI-generated responses.</p>
        {prolificRedirectUrl && <a className="btn primary" href={prolificRedirectUrl} style={{ marginTop: '1.5rem', display: 'inline-block', textDecoration: 'none' }}>Complete Study on Prolific</a>}
      </div>
    </div>
  );
}

/* ── Main App ─────────────────────────────────────────────────────────── */
/*
 * Flow: welcome -> profiling (skip NP) -> per-task loop -> post_study -> done
 * Per-task loop: content_qs (skip NP/P0) -> buffer (generate 1) -> evaluate -> next task
 */

export default function App() {
  const [phase, setPhase] = useState('welcome');
  const [sessionId, setSessionId] = useState(null);
  const [condition, setCondition] = useState(null);
  const [hasProfile, setHasProfile] = useState(true);
  const [numContentQs, setNumContentQs] = useState(0);
  const [numTasks, setNumTasks] = useState(3);
  const [taskOrder, setTaskOrder] = useState([]);
  const [taskDefs, setTaskDefs] = useState([]);  // from /api/session/create
  const [questions, setQuestions] = useState([]);
  const [contentQuestions, setContentQuestions] = useState({});
  const [evalAttentionChecks, setEvalAttentionChecks] = useState({});
  const [currentTaskIndex, setCurrentTaskIndex] = useState(0);
  const [currentTaskData, setCurrentTaskData] = useState(null);
  const [failedAttnCount, setFailedAttnCount] = useState(0);
  const [prolificRedirectUrl, setProlificRedirectUrl] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([api('/api/questions'), api('/api/content-questions')]).then(([qData, cqData]) => {
      setQuestions(qData.questions);
      if (qData.eval_attention_checks) setEvalAttentionChecks(qData.eval_attention_checks);
      setContentQuestions(cqData.content_questions);
    }).catch(console.error);
  }, []);

  // Get current task definition based on task_order
  const getCurrentTask = () => {
    if (!taskDefs.length || !taskOrder.length) return null;
    return taskDefs[taskOrder[currentTaskIndex]];
  };

  const handleStart = async () => {
    try {
      const params = new URLSearchParams(window.location.search);
      const session = await api('/api/session/create', { method: 'POST', body: JSON.stringify({ prolific_pid: params.get('PROLIFIC_PID') }) });
      setSessionId(session.session_id);
      setCondition(session.condition);
      setHasProfile(session.has_profile);
      setNumContentQs(session.num_content_qs);
      setNumTasks(session.num_tasks);
      setTaskOrder(session.task_order);
      setTaskDefs(session.tasks);
      if (session.prolific_redirect_url) setProlificRedirectUrl(session.prolific_redirect_url);

      if (session.has_profile) {
        setPhase('profiling');
      } else {
        // NP: skip profiling, go straight to first task
        setCurrentTaskIndex(0);
        startTask(session.session_id, 0, {});
      }
    } catch (err) { setError('Failed to create session. Please try again.'); }
  };

  const handleProfilingSubmit = async (answers) => {
    const checks = questions.filter(q => q.is_attention_check && q.insert_after);
    let failures = 0;
    checks.forEach(ac => { if (answers[ac.id] !== ac.expected_answer) failures++; });
    setFailedAttnCount(failures);
    if (failures >= 3) { setPhase('terminated'); return; }

    try {
      await api('/api/profiling/submit', { method: 'POST', body: JSON.stringify({ session_id: sessionId, answers }) });
      setCurrentTaskIndex(0);
      // Start first task
      if (numContentQs > 0) {
        setPhase('task_content');
      } else {
        startTask(sessionId, 0, {});
      }
    } catch (err) { setError('Failed to submit profile. Please try again.'); }
  };

  const startTask = async (sid, taskIdx, contentAnswers) => {
    setPhase('task_buffer');
    try {
      const result = await api('/api/task/generate', {
        method: 'POST',
        body: JSON.stringify({ session_id: sid, task_index: taskIdx, content_answers: contentAnswers }),
      });
      setCurrentTaskData(result);
      setPhase('task_eval');
    } catch (err) { setError('Failed to generate response. Please try again.'); }
  };

  const handleContentSubmit = (contentAnswers) => {
    startTask(sessionId, currentTaskIndex, contentAnswers);
  };

  const handleEvalSubmit = async ({ ratings, relevance, openEnded, attnRating }) => {
    try {
      await api('/api/evaluation/submit', {
        method: 'POST',
        body: JSON.stringify({
          session_id: sessionId, task_id: currentTaskData.task_id,
          eval_content_fit: ratings.content_fit, eval_personalization: ratings.personalization,
          eval_satisfaction: ratings.satisfaction, eval_effort: ratings.effort,
          eval_relevance: relevance, open_ended: openEnded,
        }),
      });
      // Handle attention check
      const attnCheck = evalAttentionChecks?.[String(currentTaskIndex)] || null;
      if (attnCheck && attnRating !== undefined) {
        try {
          await api('/api/attention-check/submit', { method: 'POST', body: JSON.stringify({ session_id: sessionId, check_id: attnCheck.id, expected: attnCheck.expected_answer, actual: attnRating }) });
        } catch (e) { console.error(e); }
        if (attnRating !== attnCheck.expected_answer) {
          setFailedAttnCount(p => { const n = p + 1; if (n >= 3) setPhase('terminated'); return n; });
        }
      }
      // Next task or post-study
      if (currentTaskIndex < numTasks - 1) {
        const next = currentTaskIndex + 1;
        setCurrentTaskIndex(next);
        setCurrentTaskData(null);
        window.scrollTo(0, 0);
        if (numContentQs > 0) {
          setPhase('task_content');
        } else {
          startTask(sessionId, next, {});
        }
      } else {
        setPhase('post_study');
      }
    } catch (err) { console.error('Failed to submit evaluation:', err); }
  };

  const handlePostStudy = async (data) => {
    try {
      await api('/api/post-study/submit', { method: 'POST', body: JSON.stringify({ session_id: sessionId, data }) });
      setPhase('done');
    } catch (err) { setError('Failed to submit. Please try again.'); }
  };

  if (error) return (
    <div className="phase"><div className="card"><h2>Something went wrong</h2><p>{error}</p>
    <button className="btn primary" onClick={() => { setError(null); setPhase('welcome'); }}>Start Over</button></div></div>
  );

  const currentTask = getCurrentTask();

  return (
    <div className="app">
      {phase === 'welcome' && <Welcome onStart={handleStart} />}
      {phase === 'profiling' && questions.length > 0 && <Profiling questions={questions} onSubmit={handleProfilingSubmit} />}
      {phase === 'task_content' && currentTask && (
        <TaskContentQuestions task={currentTask} contentQuestions={contentQuestions} numContentQs={numContentQs}
          taskIndex={currentTaskIndex} totalTasks={numTasks} onSubmit={handleContentSubmit} />
      )}
      {phase === 'task_buffer' && <Buffer />}
      {phase === 'task_eval' && currentTaskData && (
        <TaskEval taskData={currentTaskData} taskIndex={currentTaskIndex} totalTasks={numTasks}
          attnCheck={evalAttentionChecks?.[String(currentTaskIndex)] || null} onSubmit={handleEvalSubmit} />
      )}
      {phase === 'post_study' && <PostStudy onSubmit={handlePostStudy} />}
      {phase === 'done' && <ThankYou sessionId={sessionId} prolificRedirectUrl={prolificRedirectUrl} />}
      {phase === 'terminated' && (
        <div className="phase thank-you"><div className="card"><h1>Study Ended</h1>
        <p>Unfortunately, we were unable to verify that responses were being provided attentively, so the study has been ended. We appreciate your time.</p>
        {sessionId && <div className="info-box"><p><strong>Session ID:</strong> {sessionId}</p></div>}</div></div>
      )}
    </div>
  );
}
