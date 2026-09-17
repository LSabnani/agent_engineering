import { getStorySummary, CURATED_STORIES } from './database.js';
import { runRedVsGreenSimulation, generateFinancialProjections } from './gtmPipeline.js';

// Application State
let currentStory = null;
let currentDepth = 'executive'; // 'quick' | 'executive' | 'deep'
let savedSummaries = JSON.parse(localStorage.getItem('story_summarizer_saved') || '[]');
let speechSynth = window.speechSynthesis || null;
let currentUtterance = null;
let isPlayingAudio = false;

// GTM Pipeline State
let activeGTMCompanyKey = 'apple-vs-samsung';
let currentGTMResult = null;

// DOM Elements
const titleInput = document.getElementById('title-input');
const authorInput = document.getElementById('author-input');
const summarizeBtn = document.getElementById('summarize-btn');
const quickPillsContainer = document.getElementById('quick-pills');

const resultsSection = document.getElementById('results-section');
const storyTitleEl = document.getElementById('story-title');
const storyAuthorEl = document.getElementById('story-author');
const storyGenreEl = document.getElementById('story-genre');
const storyYearEl = document.getElementById('story-year');
const storyLoglineEl = document.getElementById('story-logline');

const statReadTimeEl = document.getElementById('stat-read-time');
const statSavedTimeEl = document.getElementById('stat-saved-time');
const statSourceEl = document.getElementById('stat-source');

const summaryBodyText = document.getElementById('summary-body-text');
const themesList = document.getElementById('themes-list');
const charactersList = document.getElementById('characters-list');
const quotesList = document.getElementById('quotes-list');

const depthTabs = document.querySelectorAll('.depth-tab');
const saveBtn = document.getElementById('save-btn');
const exportBtn = document.getElementById('export-btn');
const viewTraceBtn = document.getElementById('view-trace-btn');

const playAudioBtn = document.getElementById('play-audio-btn');
const audioIcon = document.getElementById('audio-icon');
const audioBtnText = document.getElementById('audio-btn-text');

const themeToggleBtn = document.getElementById('theme-toggle-btn');
const themeIcon = document.getElementById('theme-icon');

const viewSavedBtn = document.getElementById('view-saved-btn');
const modalOverlay = document.getElementById('modal-overlay');
const closeModalBtn = document.getElementById('close-modal-btn');
const savedListContainer = document.getElementById('saved-list-container');

const traceModalOverlay = document.getElementById('trace-modal-overlay');
const closeTraceModalBtn = document.getElementById('close-trace-modal-btn');
const traceTimelineContainer = document.getElementById('trace-timeline-container');
const traceConfidenceScore = document.getElementById('trace-confidence-score');

const toastEl = document.getElementById('toast');

// Initialization
document.addEventListener('DOMContentLoaded', () => {
  renderQuickPills();
  initTheme();
  bindEvents();
  
  // Default load first story (1984) to show instant wowed experience
  handleSummarize('1984', 'George Orwell');
});

function initTheme() {
  const savedTheme = localStorage.getItem('story_summarizer_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);
}

function updateThemeIcon(theme) {
  themeIcon.textContent = theme === 'dark' ? '🌙' : '☀️';
}

function bindEvents() {
  themeToggleBtn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('story_summarizer_theme', next);
    updateThemeIcon(next);
  });

  summarizeBtn.addEventListener('click', () => {
    handleSummarize(titleInput.value, authorInput.value);
  });

  titleInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSummarize(titleInput.value, authorInput.value);
  });

  authorInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSummarize(titleInput.value, authorInput.value);
  });

  depthTabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      depthTabs.forEach(t => t.classList.remove('active'));
      e.target.classList.add('active');
      currentDepth = e.target.dataset.depth;
      if (currentStory) {
        renderSummaryContent(currentStory);
      }
    });
  });

  saveBtn.addEventListener('click', toggleSaveCurrentStory);
  exportBtn.addEventListener('click', exportSummary);
  playAudioBtn.addEventListener('click', toggleAudioPlayback);

  viewSavedBtn.addEventListener('click', openSavedModal);
  closeModalBtn.addEventListener('click', closeSavedModal);
  modalOverlay.addEventListener('click', (e) => {
    if (e.target === modalOverlay) closeSavedModal();
  });

  viewTraceBtn.addEventListener('click', openTraceModal);
  closeTraceModalBtn.addEventListener('click', closeTraceModal);
  traceModalOverlay.addEventListener('click', (e) => {
    if (e.target === traceModalOverlay) closeTraceModal();
  });
}

function renderQuickPills() {
  quickPillsContainer.innerHTML = '';
  CURATED_STORIES.slice(0, 5).forEach(story => {
    const chip = document.createElement('button');
    chip.className = 'chip-btn';
    chip.textContent = `${story.title} (${story.author})`;
    chip.addEventListener('click', () => {
      titleInput.value = story.title;
      authorInput.value = story.author;
      handleSummarize(story.title, story.author);
    });
    quickPillsContainer.appendChild(chip);
  });
}

export function handleSummarize(title, author) {
  if (!title.trim()) {
    showToast('Please enter a book or story title.');
    titleInput.focus();
    return;
  }

  stopAudio();
  currentStory = getStorySummary(title, author, currentDepth);
  renderStoryResults(currentStory);
  
  // Smooth scroll to results
  resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function renderStoryResults(story) {
  resultsSection.style.display = 'block';

  storyTitleEl.textContent = story.title;
  storyAuthorEl.textContent = `By ${story.author}`;
  storyGenreEl.textContent = story.genre;
  storyYearEl.textContent = story.year !== 'N/A' ? `Est. ${story.year}` : 'Custom Synthesis';
  storyLoglineEl.textContent = `"${story.logline}"`;

  statReadTimeEl.textContent = `${story.readTimeMinutes} min`;
  statSavedTimeEl.textContent = `${story.savedTimeMinutes} min`;
  statSourceEl.textContent = story.isCurated ? 'Curated Master' : 'AI Synthesized';

  renderSummaryContent(story);
  renderThemes(story.themes);
  renderCharacters(story.characters);
  renderQuotes(story.quotes);

  updateSaveButtonState();
}

function renderSummaryContent(story) {
  const summaryText = story.isCurated 
    ? (currentDepth === 'quick' ? story.quickBrief : currentDepth === 'deep' ? story.deepDive : story.executiveSummary)
    : story.activeSummary;

  summaryBodyText.innerHTML = summaryText.replace(/\n\n/g, '<br><br>');
}

function renderThemes(themes = []) {
  themesList.innerHTML = themes.map(t => `
    <div class="theme-card">
      <div class="theme-name">${t.name}</div>
      <div class="theme-desc">${t.desc}</div>
    </div>
  `).join('');
}

function renderCharacters(characters = []) {
  charactersList.innerHTML = characters.map(c => `
    <div class="character-card">
      <div class="character-name">${c.name}</div>
      <div class="character-role">${c.role}</div>
      <div class="theme-desc">${c.desc}</div>
    </div>
  `).join('');
}

function renderQuotes(quotes = []) {
  quotesList.innerHTML = quotes.map(q => `
    <div class="quote-card">
      <div class="quote-text">"${q.text}"</div>
      <div class="quote-context">— ${q.context}</div>
    </div>
  `).join('');
}

/* Audio Speech Synthesis */
function toggleAudioPlayback() {
  if (!speechSynth) {
    showToast('Speech synthesis is not supported in this browser.');
    return;
  }

  if (isPlayingAudio) {
    stopAudio();
    return;
  }

  const textToRead = `${currentStory.title} by ${currentStory.author}. ${summaryBodyText.textContent}`;
  currentUtterance = new SpeechSynthesisUtterance(textToRead);
  currentUtterance.rate = 1.0;
  
  currentUtterance.onend = () => {
    stopAudio();
  };

  currentUtterance.onerror = () => {
    stopAudio();
    showToast('Audio playback error.');
  };

  speechSynth.speak(currentUtterance);
  isPlayingAudio = true;
  audioIcon.textContent = '⏹️';
  audioBtnText.textContent = 'Stop Audio';
}

function stopAudio() {
  if (speechSynth && speechSynth.speaking) {
    speechSynth.cancel();
  }
  isPlayingAudio = false;
  audioIcon.textContent = '🔊';
  audioBtnText.textContent = 'Listen';
}

/* Save / Library System */
function toggleSaveCurrentStory() {
  if (!currentStory) return;

  const existingIndex = savedSummaries.findIndex(s => s.title.toLowerCase() === currentStory.title.toLowerCase());
  if (existingIndex >= 0) {
    savedSummaries.splice(existingIndex, 1);
    showToast(`Removed "${currentStory.title}" from saved library.`);
  } else {
    savedSummaries.push(currentStory);
    showToast(`Saved "${currentStory.title}" to library!`);
  }

  localStorage.setItem('story_summarizer_saved', JSON.stringify(savedSummaries));
  updateSaveButtonState();
}

function updateSaveButtonState() {
  if (!currentStory) return;
  const isSaved = savedSummaries.some(s => s.title.toLowerCase() === currentStory.title.toLowerCase());
  saveBtn.innerHTML = isSaved ? '<span>❤️</span> Saved' : '<span>🤍</span> Save Summary';
}

function openSavedModal() {
  renderSavedList();
  modalOverlay.classList.add('active');
}

function closeSavedModal() {
  modalOverlay.classList.remove('active');
}

/* Traceability Drawer Handlers */
function openTraceModal() {
  if (!currentStory || !currentStory.traceLog) return;
  renderTraceTimeline(currentStory);
  traceModalOverlay.classList.add('active');
}

function closeTraceModal() {
  traceModalOverlay.classList.remove('active');
}

function renderTraceTimeline(story) {
  traceConfidenceScore.textContent = `${story.traceConfidence || 100}% Confidence`;
  
  traceTimelineContainer.innerHTML = story.traceLog.map(item => `
    <div class="trace-step" data-step="${item.step}">
      <div class="trace-step-name">${item.name}</div>
      <div class="trace-step-detail">${item.detail}</div>
    </div>
  `).join('');
}

function renderSavedList() {
  if (savedSummaries.length === 0) {
    savedListContainer.innerHTML = '<p style="color:var(--text-muted); text-align:center; padding:2rem 0;">No saved summaries yet.</p>';
    return;
  }

  savedListContainer.innerHTML = savedSummaries.map((s, idx) => `
    <div class="saved-item" data-idx="${idx}">
      <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div>
          <h4 style="font-family:var(--font-heading); font-size:1.1rem; font-weight:700;">${s.title}</h4>
          <p style="font-size:0.85rem; color:var(--accent-secondary);">${s.author}</p>
        </div>
        <button class="btn btn-sm remove-save-btn" data-idx="${idx}" style="color:#ef4444;">🗑️</button>
      </div>
      <p style="font-size:0.8rem; color:var(--text-secondary); margin-top:0.5rem; line-clamp:2;">${s.logline}</p>
    </div>
  `).join('');

  document.querySelectorAll('.saved-item').forEach(item => {
    item.addEventListener('click', (e) => {
      if (e.target.classList.contains('remove-save-btn')) {
        e.stopPropagation();
        const idx = parseInt(e.target.dataset.idx);
        savedSummaries.splice(idx, 1);
        localStorage.setItem('story_summarizer_saved', JSON.stringify(savedSummaries));
        renderSavedList();
        updateSaveButtonState();
        showToast('Item removed.');
        return;
      }

      const idx = parseInt(item.dataset.idx);
      const selected = savedSummaries[idx];
      titleInput.value = selected.title;
      authorInput.value = selected.author;
      handleSummarize(selected.title, selected.author);
      closeSavedModal();
    });
  });
}

/* Export Engine */
function exportSummary() {
  if (!currentStory) return;

  const content = `
====================================================
STORY SUMMARY: ${currentStory.title.toUpperCase()}
Author: ${currentStory.author}
Genre: ${currentStory.genre}
Provenance: ${currentStory.isCurated ? 'Curated Master Repository' : 'AI Synthesized'}
Trace Confidence: ${currentStory.traceConfidence || 100}%
====================================================

LOGLINE:
${currentStory.logline}

EXECUTIVE SUMMARY (${currentDepth.toUpperCase()} DEPTH):
${summaryBodyText.textContent}

KEY THEMES:
${currentStory.themes.map(t => `- ${t.name}: ${t.desc}`).join('\n')}

MAIN CHARACTERS:
${currentStory.characters.map(c => `- ${c.name} (${c.role}): ${c.desc}`).join('\n')}

MEMORABLE QUOTES:
${currentStory.quotes.map(q => `"${q.text}" (${q.context})`).join('\n')}

EXECUTION TRACE LOG:
${currentStory.traceLog ? currentStory.traceLog.map(t => `[Step ${t.step}] ${t.name}: ${t.detail}`).join('\n') : 'N/A'}

----------------------------------------------------
Generated via Story Summarizer App with Traceability Engine
`;

  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${currentStory.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}_summary.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast('Summary exported with trace log to file!');
}

function showToast(msg) {
  toastEl.textContent = msg;
  toastEl.classList.add('show');
  setTimeout(() => {
    toastEl.classList.remove('show');
  }, 3000);
}

/* ==========================================================================
   GTM Red Team vs. Green Team Controller & UI Renderer
   ========================================================================== */

const navStoryModeBtn = document.getElementById('nav-story-mode');
const navGtmModeBtn = document.getElementById('nav-gtm-mode');
const heroSection = document.querySelector('.hero-section');
const gtmSection = document.getElementById('gtm-section');
const runGtmBtn = document.getElementById('run-gtm-btn');
const gtmPresetPills = document.querySelectorAll('#gtm-preset-pills .depth-tab');

if (navStoryModeBtn && navGtmModeBtn) {
  navStoryModeBtn.addEventListener('click', () => {
    navStoryModeBtn.classList.add('active');
    navGtmModeBtn.classList.remove('active');
    if (heroSection) heroSection.style.display = 'block';
    if (resultsSection && currentStory) resultsSection.style.display = 'block';
    if (gtmSection) gtmSection.style.display = 'none';
  });

  navGtmModeBtn.addEventListener('click', () => {
    navGtmModeBtn.classList.add('active');
    navStoryModeBtn.classList.remove('active');
    if (heroSection) heroSection.style.display = 'none';
    if (resultsSection) resultsSection.style.display = 'none';
    if (gtmSection) {
      gtmSection.style.display = 'block';
      if (!currentGTMResult) {
        handleGTMSimulation('apple-vs-samsung');
      }
    }
  });
}

if (gtmPresetPills) {
  gtmPresetPills.forEach(pill => {
    pill.addEventListener('click', () => {
      gtmPresetPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      activeGTMCompanyKey = pill.getAttribute('data-company');
      handleGTMSimulation(activeGTMCompanyKey);
    });
  });
}

if (runGtmBtn) {
  runGtmBtn.addEventListener('click', () => {
    handleGTMSimulation(activeGTMCompanyKey);
  });
}

const viewGtmTraceBtn = document.getElementById('view-gtm-trace-btn');
const exportGtmBtn = document.getElementById('export-gtm-btn');

if (viewGtmTraceBtn) {
  viewGtmTraceBtn.addEventListener('click', () => {
    if (!currentGTMResult) return;
    renderGTMTraceLog(currentGTMResult.traceLog, currentGTMResult.overallMetrics.confidenceScore);
  });
}

if (exportGtmBtn) {
  exportGtmBtn.addEventListener('click', () => {
    exportGTMReport();
  });
}

function handleGTMSimulation(companyKey = 'apple-vs-samsung') {
  currentGTMResult = runRedVsGreenSimulation(companyKey);
  renderGTMResults(currentGTMResult);
  showToast(`Ran Red vs Green GTM Simulation for ${currentGTMResult.greenCompany} vs ${currentGTMResult.redCompany}!`);
}

function renderGTMResults(res) {
  document.getElementById('gtm-green-title').textContent = res.greenCompany;
  document.getElementById('gtm-green-overview').textContent = `Dominant high-margin market position in ${res.sector}.`;
  document.getElementById('gtm-red-title').textContent = res.redCompany;
  document.getElementById('gtm-red-overview').textContent = `Aggressive challenger deploying full-information attack vectors.`;

  document.getElementById('gtm-verdict-title').textContent = res.overallMetrics.winLikelihood;
  document.getElementById('gtm-defensibility-score').textContent = `${res.overallMetrics.greenDefensibilityScore}%`;
  document.getElementById('gtm-attack-score').textContent = `${res.overallMetrics.avgRedSuccessProbability}%`;

  // Financial War Chest & FCF Body
  const war = res.gtmAnalysis.financialWarChest;
  document.getElementById('gtm-warchest-body').innerHTML = `
    <p><strong>${res.greenCompany} Cash War Chest:</strong> <span style="color:#10b981; font-weight:700;">$${war.greenWarChest}B</span> (FCF: $${war.greenFCF}B)</p>
    <p><strong>${res.redCompany} Cash War Chest:</strong> <span style="color:#ef4444; font-weight:700;">$${war.redWarChest}B</span> (FCF: $${war.redFCF}B)</p>
    <p style="margin-top:0.5rem; color:var(--text-secondary);">${war.analysis}</p>
  `;

  // Product Head-to-Head Body
  const h2h = res.gtmAnalysis.headToHead;
  let specsHtml = '';
  if (h2h.greenSpecs && h2h.redSpecs) {
    specsHtml = `
      <div style="margin-top:0.75rem; background:rgba(0,0,0,0.25); border:1px solid var(--border-color); border-radius:10px; padding:0.75rem;">
        <div style="font-weight:700; font-size:0.85rem; color:var(--accent-secondary); margin-bottom:0.5rem;">📱 Detailed Hardware Specs Comparison</div>
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:0.5rem; font-size:0.8rem;">
          <div style="border-right:1px solid var(--border-color); padding-right:0.5rem;">
            <div style="color:#10b981; font-weight:700; margin-bottom:0.2rem;">${h2h.greenProduct}</div>
            <div><strong>Display:</strong> ${h2h.greenSpecs.display}</div>
            <div><strong>Chipset:</strong> ${h2h.greenSpecs.chipset}</div>
            <div><strong>Memory:</strong> ${h2h.greenSpecs.memoryStorage}</div>
            <div><strong>Camera:</strong> ${h2h.greenSpecs.cameraSystem}</div>
            <div><strong>Battery:</strong> ${h2h.greenSpecs.batteryCharging}</div>
          </div>
          <div style="padding-left:0.5rem;">
            <div style="color:#ef4444; font-weight:700; margin-bottom:0.2rem;">${h2h.redProduct}</div>
            <div><strong>Display:</strong> ${h2h.redSpecs.display}</div>
            <div><strong>Chipset:</strong> ${h2h.redSpecs.chipset}</div>
            <div><strong>Memory:</strong> ${h2h.redSpecs.memoryStorage}</div>
            <div><strong>Camera:</strong> ${h2h.redSpecs.cameraSystem}</div>
            <div><strong>Battery:</strong> ${h2h.redSpecs.batteryCharging}</div>
          </div>
        </div>
      </div>
    `;
  }

  document.getElementById('gtm-headtohead-body').innerHTML = `
    <p><strong>Green Flagship Product:</strong> ${h2h.greenProduct} (${h2h.greenProductRevenue})</p>
    <p><strong>Red Flagship Product:</strong> ${h2h.redProduct} (${h2h.redProductRevenue})</p>
    <p><strong>Comparison Category:</strong> ${h2h.customerComparisonPair}</p>
    ${specsHtml}
    <p style="margin-top:0.5rem; color:var(--text-secondary);">${h2h.verdict}</p>
  `;

  // IP Portfolio Body
  const ip = res.gtmAnalysis.ipPortfolio;
  document.getElementById('gtm-ip-body').innerHTML = `
    <p><strong>Green Vetted IP:</strong> ${ip.greenStrengths.join(', ')}</p>
    <p><strong>Red Vetted IP:</strong> ${ip.redStrengths.join(', ')}</p>
    <p style="color:#f59e0b; margin-top:0.5rem;"><strong>Unvetted / Vulnerable IP Frontiers:</strong> ${ip.unvettedAreas.join('; ')}</p>
  `;

  // Loyalty Body
  const loy = res.gtmAnalysis.loyalty;
  document.getElementById('gtm-loyalty-body').innerHTML = `
    <p><strong>Green Retention Rate:</strong> <span style="color:#10b981; font-weight:700;">${loy.greenRetentionRate}</span></p>
    <p><strong>Red Retention Rate:</strong> <span style="color:#ef4444; font-weight:700;">${loy.redRetentionRate}</span></p>
    <p style="margin-top:0.5rem; color:var(--text-secondary);">${loy.greenBrandSentiment}</p>
  `;

  // Render Red Team Strategy Table
  const tbody = document.getElementById('gtm-strategies-table-body');
  tbody.innerHTML = res.redTeamStrategies.map(strat => {
    let probClass = strat.probabilityOfSuccess >= 80 ? 'high' : (strat.probabilityOfSuccess >= 70 ? 'med' : 'low');
    return `
      <tr>
        <td>
          <strong style="color:var(--text-primary);">${strat.title}</strong>
          <div style="font-size:0.8rem; color:var(--text-muted); margin-top:0.2rem;">${strat.summary}</div>
        </td>
        <td><span class="badge">${strat.feasibilityScore}/10</span></td>
        <td><strong>$${strat.costBillions}B</strong></td>
        <td>${strat.executionTimeMonths} mos</td>
        <td><span class="prob-badge ${probClass}">${strat.probabilityOfSuccess}%</span></td>
        <td style="font-size:0.82rem; color:#34d399;">${strat.greenCountermeasure}</td>
      </tr>
    `;
  }).join('');

  // Render Projections Table
  const proj = generateFinancialProjections(activeGTMCompanyKey);
  const projTbody = document.getElementById('gtm-projections-table-body');
  projTbody.innerHTML = `
    <tr>
      <td><strong>${res.greenCompany} Revenue ($B)</strong></td>
      <td>${proj.greenHistRev[0]}</td>
      <td>${proj.greenHistRev[1]}</td>
      <td>${proj.greenHistRev[2]}</td>
      <td style="color:#10b981;"><strong>${proj.greenFwdRev[0]}</strong></td>
      <td style="color:#10b981;"><strong>${proj.greenFwdRev[1]}</strong></td>
      <td style="color:#10b981;"><strong>${proj.greenFwdRev[2]}</strong></td>
    </tr>
    <tr>
      <td><strong>${res.redCompany} Revenue ($B)</strong></td>
      <td>${proj.redHistRev[0]}</td>
      <td>${proj.redHistRev[1]}</td>
      <td>${proj.redHistRev[2]}</td>
      <td style="color:#ef4444;"><strong>${proj.redFwdRev[0]}</strong></td>
      <td style="color:#ef4444;"><strong>${proj.redFwdRev[1]}</strong></td>
      <td style="color:#ef4444;"><strong>${proj.redFwdRev[2]}</strong></td>
    </tr>
    <tr>
      <td><strong>${res.greenCompany} Gross Margin %</strong></td>
      <td>${proj.greenHistGM[0]}%</td>
      <td>${proj.greenHistGM[1]}%</td>
      <td>${proj.greenHistGM[2]}%</td>
      <td style="color:#10b981;"><strong>${proj.greenFwdGM[0]}%</strong></td>
      <td style="color:#10b981;"><strong>${proj.greenFwdGM[1]}%</strong></td>
      <td style="color:#10b981;"><strong>${proj.greenFwdGM[2]}%</strong></td>
    </tr>
    <tr>
      <td><strong>${res.redCompany} Gross Margin %</strong></td>
      <td>${proj.redHistGM[0]}%</td>
      <td>${proj.redHistGM[1]}%</td>
      <td>${proj.redHistGM[2]}%</td>
      <td style="color:#ef4444;"><strong>${proj.redFwdGM[0]}%</strong></td>
      <td style="color:#ef4444;"><strong>${proj.redFwdGM[1]}%</strong></td>
      <td style="color:#ef4444;"><strong>${proj.redFwdGM[2]}%</strong></td>
    </tr>
  `;
}

function renderGTMTraceLog(traceLog, confidenceScore) {
  traceConfidenceScore.textContent = `${confidenceScore}%`;
  traceTimelineContainer.innerHTML = traceLog.map(item => `
    <div class="trace-step">
      <div class="trace-step-number">${item.step}</div>
      <div style="flex:1;">
        <div class="trace-step-name">${item.name}</div>
        <div class="trace-step-detail">${item.detail}</div>
      </div>
    </div>
  `).join('');
  traceModalOverlay.style.display = 'flex';
}

function exportGTMReport() {
  if (!currentGTMResult) return;
  const res = currentGTMResult;
  const content = `
====================================================
RED TEAM VS GREEN TEAM GO-TO-MARKET READINESS REPORT
Green Team (Defender): ${res.greenCompany}
Red Team (Attacker): ${res.redCompany}
Sector: ${res.sector}
Engine Confidence: ${res.overallMetrics.confidenceScore}%
====================================================

EXECUTIVE VERDICT:
${res.overallMetrics.winLikelihood}
Green Defensibility Score: ${res.overallMetrics.greenDefensibilityScore}%
Average Red Attack Probability: ${res.overallMetrics.avgRedSuccessProbability}%

FINANCIAL WAR CHEST:
- ${res.greenCompany} Cash War Chest: $${res.gtmAnalysis.financialWarChest.greenWarChest}B (FCF: $${res.gtmAnalysis.financialWarChest.greenFCF}B)
- ${res.redCompany} Cash War Chest: $${res.gtmAnalysis.financialWarChest.redWarChest}B (FCF: $${res.gtmAnalysis.financialWarChest.redFCF}B)
Analysis: ${res.gtmAnalysis.financialWarChest.analysis}

PRODUCT HEAD-TO-HEAD MATRIX:
- Green Flagship: ${res.gtmAnalysis.headToHead.greenProduct} (${res.gtmAnalysis.headToHead.greenProductRevenue})
- Red Flagship: ${res.gtmAnalysis.headToHead.redProduct} (${res.gtmAnalysis.headToHead.redProductRevenue})
- Comparison Pair: ${res.gtmAnalysis.headToHead.customerComparisonPair}
- Verdict: ${res.gtmAnalysis.headToHead.verdict}

IP & PATENT PORTFOLIO VETTING:
- Green Vetted IP: ${res.gtmAnalysis.ipPortfolio.greenStrengths.join(', ')}
- Red Vetted IP: ${res.gtmAnalysis.ipPortfolio.redStrengths.join(', ')}
- Vulnerable / Unvetted Frontiers: ${res.gtmAnalysis.ipPortfolio.unvettedAreas.join('; ')}

RED TEAM OFFENSIVE ATTACK VECTORS:
${res.redTeamStrategies.map(s => `
* Strategy: ${s.title}
  Summary: ${s.summary}
  Feasibility: ${s.feasibilityScore}/10 | Cost: $${s.costBillions}B | Time: ${s.executionTimeMonths} months | Probability: ${s.probabilityOfSuccess}%
  Green Countermeasure: ${s.greenCountermeasure}
`).join('')}

EXECUTION PROVENANCE LOG:
${res.traceLog.map(t => `[Step ${t.step}] ${t.name}: ${t.detail}`).join('\n')}

----------------------------------------------------
Generated via GTM & Story AI Suite
`;

  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `gtm_report_${res.greenCompany.toLowerCase()}_vs_${res.redCompany.toLowerCase()}.txt`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast('Exported GTM Report text file!');
}

