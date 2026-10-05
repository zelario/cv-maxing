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
const yesNoQuestionPattern = /^(?:(?:the candidate|the cv|the resume|you|they|he|she)\s+)?(?:do|does|did|is|are|was|were|have|has|had|can|could|would|will|should|may)\b|^(?:(?:voce|tu|ele|ela|o candidato|a candidata|a pessoa|o curriculo|a candidatura)\s+)?(?:nao\s+)?(?:tem|tens|e|sao|foi|foram|pode|podes|podem|consegue|consegues|conseguem|gostaria|aceita|aceitas|aceitam|esta|estas|estao|estava|estavam|fez|fizeste|existe|existem|ha|houve|possui|possuem|inclui|incluem|trabalha|trabalhas|sabe|sabes|sabem|conhece|conheces|conhecem|quer|queres|querem|pretende|pretendes|pretendem)\b|\b(?:answer|responda)\s+(?:yes\s+or\s+no|sim\s+ou\s+nao)\b/i;
const openQuestionPattern = /^(?:(?:please|can you|could you|would you)\s+)?(?:what|which|who|whom|whose|when|where|why|how|describe|explain|list|name|provide|share|specify|identify|give(?: me)?|o que|que|qual|quais|quem|quando|onde|por que|porque|como|descreva|explique|liste|enumere|indique|diga|forneca|partilhe|especifique|identifique)\b|^(?:(?:can|could|would)\s+you\s+)?(?:please\s+)?(?:describe|explain|list|name|provide|share|specify|identify)\b|\b(?:tell me|diga-me)\s+(?!(?:if|whether|se)\b)\w+|\b(?:if yes|if so|se sim|caso afirmativo)\s*[,;:]?\s*(?:what|which|how|describe|explain|list|qual|quais|como|descreva|explique|enumere)\b|\b(?:and|e)\s+(?:what|which|when|where|how|describe|explain|list|qual|quais|quando|onde|como|descreva|explique|enumere)\b|[?.!]\s*(?:what|which|who|when|where|why|how|qual|quais|quem|quando|onde|porque|como)\b|\b(?:provide|share|give|indicate|specify|forneca|partilhe|indique)\s+(?:(?:the|your|an?|exact|any|the exact)\s+)*(?:details?|dates?|examples?|url|information|context|details?|detalhes|datas|exemplos|informacao|contexto)\b|\b(?:describe|explain|list|provide details|give details|specify|share details|explique|descreva|enumere|indique os detalhes)\b/i;

function normalizeQuestionText(text) {
  return text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
}

function cleanOption(option) {
  return option
    .replace(/^[\s\-\u2013\u2014\u2022\d.()]+/, '')
    .replace(/[\s?.!);()]+$/, '')
    .trim();
}

function extractQuestionOptions(question) {
  const singleChoice = /\b(?:choose|select)\s+one\s+(?:of|from)|\b(?:choose|select)\s+between|\b(?:escolha|escolhe|selecione|seleciona)\s+(?:um|uma|entre)\b/i.test(question);
  const introduced = question.match(/(?:choose (?:any|one|all) of (?:the following )?|select (?:any|one|all) of (?:the following )?|select all that apply|check all that apply|choose from (?:the following )?|select from (?:the following )?|choose between|select between|options? (?:are|include)|the following options|among (?:the following )?|entre (?:as )?(?:seguintes )?(?:op\u00e7\u00f5es? )?|escolha entre|escolhe entre|selecione entre|seleciona entre|escolha (?:um|uma) das (?:seguintes )?op\u00e7\u00f5es|selecione (?:um|uma) das (?:seguintes )?op\u00e7\u00f5es|op\u00e7\u00f5es? (?:s\u00e3o|incluem))\s*:?\s*([^?.]+)/i);
  const source = introduced?.[1].replace(/\s+(?:and|e)\s+(?:please\s+)?(?:describe|explain|list|provide|share|specify|tell|explique|descreva|liste|indique|diga|forneca)\b.*$/i, '');
  if (!source) return null;

  const options = source
    .replace(/\s+(?:and|or|e|ou)\s+/gi, ',')
    .split(/[,;|/]/)
    .map(cleanOption)
    .filter((option) => option.length > 0 && option.length < 45);

  const uniqueOptions = [...new Set(options)].slice(0, 8);
  return uniqueOptions.length > 1 ? { type: singleChoice ? 'single' : 'multiple', options: uniqueOptions } : null;
}

function getQuestionConfig(question) {
  if (question && typeof question === 'object') {
    const text = question.text || question.prompt || question.question || '';
    const options = Array.isArray(question.options) ? question.options.map(String).map(cleanOption).filter(Boolean) : [];
    const type = question.type;
    if (type === 'yes_no') return { text, type: 'single', options: ['Yes', 'No'] };
    if (type === 'single_choice') return { text, type: 'single', options };
    if (type === 'enumeration') return { text, type: 'multiple', options };
    if (type === 'open') return { text, type: 'open', options: [] };
    return classifyQuestionText(text);
  }

  return classifyQuestionText(String(question || ''));
}

function classifyQuestionText(text) {
  const optionConfig = extractQuestionOptions(text);
  if (optionConfig) return { text, ...optionConfig };
  const trimmed = normalizeQuestionText(text.trim());
  if (openQuestionPattern.test(trimmed)) return { text, type: 'multiple', options: [] };
  if (yesNoQuestionPattern.test(trimmed)) {
    return { text, type: 'single', options: ['Yes', 'No'] };
  }
  return { text, type: 'multiple', options: [] };
}

function renderQuickAnswers(config) {
  const fieldset = byId('quick-answer-fieldset');
  const container = byId('quick-answer-options');
  container.replaceChildren();
  fieldset.hidden = config.options.length === 0;
  byId('answer-label').classList.toggle('has-quick-answers', config.options.length > 0);
  byId('answer-label').textContent = config.options.length > 0 ? 'ADD A NOTE (OPTIONAL)' : 'YOUR ANSWER';
  byId('answer').placeholder = config.options.length > 0
    ? 'Add any useful context here…'
    : '';
  if (!config.options.length) return;

  byId('quick-answer-legend').textContent = config.type === 'single' ? 'CHOOSE AN ANSWER' : 'SELECT ALL THAT APPLY';
  config.options.forEach((option, index) => {
    const label = document.createElement('label');
    label.className = 'quick-answer-option';
    const input = document.createElement('input');
    input.type = config.type === 'single' ? 'radio' : 'checkbox';
    input.name = 'quick-answer';
    input.value = option;
    input.id = `quick-answer-${index}`;
    const mark = document.createElement('span');
    mark.className = 'quick-answer-option-mark';
    mark.setAttribute('aria-hidden', 'true');
    const text = document.createElement('span');
    text.textContent = option;
    label.append(input, mark, text);
    container.append(label);
  });
}

function getCurrentAnswer() {
  const selections = [...document.querySelectorAll('#quick-answer-options input:checked')].map((input) => input.value);
  const note = byId('answer').value.trim();
  if (!selections.length) return note;
  if (!note) return selections.join(', ');
  return `${selections.join(', ')} — ${note}`;
}

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
  const config = getQuestionConfig(question);
  state.questionId = questionId;
  byId('current-question').textContent = config.text;
  byId('answer').value = '';
  renderQuickAnswers(config);
  byId('question-answer-error').hidden = true;
  byId('question-next').disabled = false;
  byId('answer').disabled = false;
  showScreen('questions');
}

function submitCurrentAnswer(answer) {
  if (!answer.trim()) {
    byId('question-answer-error').hidden = false;
    const firstQuickAnswer = byId('quick-answer-options').querySelector('input');
    (firstQuickAnswer || byId('answer')).focus();
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
byId('question-next').addEventListener('click', () => submitCurrentAnswer(getCurrentAnswer()));
byId('question-skip').addEventListener('click', () => submitCurrentAnswer('I do not know or have information to answer this question.'));
byId('quick-answer-options').addEventListener('change', () => {
  byId('question-answer-error').hidden = true;
});
byId('answer').addEventListener('input', () => {
  byId('question-answer-error').hidden = true;
});
byId('answer').addEventListener('keydown', (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') submitCurrentAnswer(getCurrentAnswer());
});
byId('restart-button').addEventListener('click', reset);
