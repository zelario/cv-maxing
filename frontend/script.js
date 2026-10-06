'use strict';

const state = {
  screen: 'landing',
  file: null,
  job: '',
  jobId: null,
  questionId: null,
  submitAnswer: null,
  result: null,
};

const byId = (id) => document.getElementById(id);
const screenIds = ['landing', 'upload', 'job', 'processing', 'questions', 'result'];

function showScreen(id) {
  state.screen = id;
  screenIds.forEach((screenId) => {
    const screen = byId(screenId);
    const isActive = screenId === id;
    screen.hidden = !isActive;
    screen.classList.toggle('is-active', isActive);
    if (isActive) {
      // Restart the entrance animation when revisiting a screen.
      screen.classList.remove('screen-entering');
      void screen.offsetWidth;
      screen.classList.add('screen-entering');
    } else {
      screen.classList.remove('screen-entering');
    }
  });
  window.scrollTo(0, 0);
  const heading = byId(id).querySelector('h1, h2, h3');
  if (heading) {
    heading.tabIndex = -1;
    heading.focus({ preventScroll: true });
  }
}

function selectFile(file) {
  if (!file) return;
  const validType = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
  const valid = validType && file.size <= 15 * 1024 * 1024;
  byId('upload-error').hidden = valid;
  if (!valid) return;
  state.file = file;
  byId('upload-name').textContent = file.name;
  byId('upload-name').classList.add('upload-file-name');
  byId('upload-detail').textContent = 'PDF selected · Maximum 15 MB';
  byId('upload-next').disabled = false;
}

function setupUpload() {
  const input = byId('cv-file');
  const trigger = byId('upload-trigger');
  trigger.addEventListener('click', () => input.click());
  input.addEventListener('change', () => selectFile(input.files[0]));
  trigger.addEventListener('dragover', (event) => {
    event.preventDefault();
    trigger.classList.add('is-dragging');
  });
  trigger.addEventListener('dragleave', () => trigger.classList.remove('is-dragging'));
  trigger.addEventListener('drop', (event) => {
    event.preventDefault();
    trigger.classList.remove('is-dragging');
    selectFile(event.dataTransfer.files[0]);
  });
}

function setupJobInput() {
  const input = byId('job-description');
  input.addEventListener('input', () => {
    state.job = input.value;
    byId('job-error').hidden = true;
  });
}

function showQuestion(questionId, question) {
  state.questionId = questionId;
  byId('current-question').textContent = question;
  byId('answer').value = '';
  byId('question-answer-error').hidden = true;
  byId('question-next').disabled = false;
  byId('answer').disabled = false;
  showScreen('questions');
}

function submitCurrentAnswer(answer) {
  if (!answer.trim()) {
    byId('question-answer-error').hidden = false;
    byId('answer').focus();
    return;
  }
  byId('question-next').disabled = true;
  byId('answer').disabled = true;
  state.submitAnswer?.(answer.trim());
}

function delay(milliseconds) {
  return new Promise((resolve) => window.setTimeout(resolve, milliseconds));
}

async function readResponse(response) {
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail || 'O pedido falhou.');
  return payload;
}

async function startOptimization() {
  if (!state.file) {
    showScreen('upload');
    byId('upload-error').hidden = false;
    return;
  }
  if (!state.job.trim()) {
    byId('job-error').hidden = false;
    byId('job-description').focus();
    return;
  }

  byId('start-button').disabled = true;
  showScreen('processing');
  byId('loading-screen').textContent = 'Starting the analysis…';
  try {
    const form = new FormData();
    form.append('cv', state.file);
    form.append('job', state.job.trim());
    const created = await readResponse(await fetch('/api/jobs', { method: 'POST', body: form }));
    state.jobId = created.id;
    await followOptimization();
  } catch (error) {
    state.jobId = null;
    showScreen('job');
    byId('job-error').textContent = error.message;
    byId('job-error').hidden = false;
  } finally {
    byId('start-button').disabled = false;
  }
}

async function followOptimization() {
  let seenQuestionId = null;
  while (state.jobId) {
    const current = await readResponse(await fetch(`/api/jobs/${state.jobId}`, { cache: 'no-store' }));
    if (current.status === 'error') throw new Error(current.error || 'Could not complete the optimization.');
    if (current.status === 'complete') {
      state.result = current.result;
      renderResult();
      state.jobId = null;
      showScreen('result');
      return;
    }
    if (current.status === 'waiting_question' && current.question_id !== seenQuestionId) {
      seenQuestionId = current.question_id;
      showQuestion(current.question_id, current.question);
      const answer = await new Promise((resolve) => { state.submitAnswer = resolve; });
      state.submitAnswer = null;
      showScreen('processing');
      byId('loading-screen').textContent = 'Answer submitted. Working on it…';
      await readResponse(await fetch(`/api/jobs/${state.jobId}/answer`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question_id: seenQuestionId, answer }),
      }));
      continue;
    }
    byId('loading-screen').textContent = 'Thinking about the details…';
    await delay(1200);
  }
}

function renderResult() {
  const result = state.result;

  const container = byId('cv-comparison');
  container.replaceChildren();
  const documentSection = document.createElement('section');
  const documentHeading = document.createElement('h3');
  documentHeading.className = 'comparison-heading';
  documentHeading.textContent = 'OPTIMIZED CV';
  const documentText = document.createElement('pre');
  documentText.className = 'cv-document optimized generated-document';
  documentText.textContent = result.markdown;
  documentSection.append(documentHeading, documentText);
  container.append(documentSection);
  byId('download-button').onclick = downloadResult;
}

function downloadResult() {
  const file = new Blob([state.result.markdown], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(file);
  const link = document.createElement('a');
  link.href = url;
  link.download = 'optimized-cv.md';
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function reset() {
  if (state.jobId) return;
  state.file = null;
  state.job = '';
  state.result = null;
  state.questionId = null;
  byId('cv-file').value = '';
  byId('upload-name').textContent = 'Upload your CV';
  byId('upload-name').classList.remove('upload-file-name');
  byId('upload-detail').textContent = 'Choose a PDF or drag it here';
  byId('upload-next').disabled = true;
  byId('job-description').value = '';
  byId('job-error').hidden = true;
  showScreen('landing');
}

setupUpload();
setupJobInput();
byId('brand-home').addEventListener('click', reset);
byId('begin-button').addEventListener('click', () => showScreen('upload'));
byId('upload-back').addEventListener('click', () => showScreen('landing'));
byId('upload-next').addEventListener('click', () => showScreen('job'));
byId('job-back').addEventListener('click', () => showScreen('upload'));
byId('start-button').addEventListener('click', startOptimization);
byId('question-next').addEventListener('click', () => submitCurrentAnswer(byId('answer').value));
byId('question-skip').addEventListener('click', () => submitCurrentAnswer('I do not know or have information to answer this question.'));
byId('answer').addEventListener('keydown', (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') submitCurrentAnswer(byId('answer').value);
});
byId('restart-button').addEventListener('click', reset);
