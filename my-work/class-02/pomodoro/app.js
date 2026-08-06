/* ==========================================================================
   AURA APPLICATION LOGIC — JAVASCRIPT
   ========================================================================== */

// Mindfulness Quotes
const MINDFUL_QUOTES = [
    { text: "Within you, there is a stillness and a sanctuary to which you can retreat at any time.", author: "Hermann Hesse" },
    { text: "Feelings come and go like clouds in a windy sky. Conscious breathing is my anchor.", author: "Thich Nhat Hanh" },
    { text: "Do not dwell in the past, do not dream of the future, concentrate the mind on the present moment.", author: "Buddha" },
    { text: "Simplicity, patience, compassion. These three are your greatest treasures.", author: "Lao Tzu" },
    { text: "The present moment is filled with joy and happiness. If you are attentive, you will see it.", author: "Thich Nhat Hanh" },
    { text: "Muddy water is best cleared by leaving it alone.", author: "Alan Watts" },
    { text: "Quiet the mind and the soul will speak.", author: "Ma Jaya Sati Bhagavati" },
    { text: "He who is contented is rich.", author: "Lao Tzu" },
    { text: "Almost everything will work again if you unplug it for a few minutes, including you.", author: "Anne Lamott" }
];

// App Configurations & Default State
const DEFAULT_SETTINGS = {
    durationFocus: 25,     // in minutes
    durationShort: 5,      // in minutes
    durationLong: 15,      // in minutes
    autoStartFocus: false,
    autoStartBreaks: false,
    guideBreakBreathe: true,
    chimeStyle: 'singing-bowl'
};

let settings = { ...DEFAULT_SETTINGS };
let tasks = [];
let activeTaskId = null;
let stats = {
    pomodorosCompleted: 0,
    totalFocusMinutes: 0
};

// Timer State
let timerInterval = null;
let timeLeft = 25 * 60; // default 25 minutes in seconds
let totalDuration = 25 * 60;
let isRunning = false;
let currentMode = 'focus'; // 'focus', 'short', 'long', 'breathe'

// 4-7-8 Breathing Technique Engine State
let breathePhase = 'inhale'; // 'inhale', 'hold', 'exhale'
let breatheSecondsLeft = 4;
let breatheCycle = 1;
let isBreakBreatheActive = true;
const BREATHE_PHASES = {
    inhale: { duration: 4, label: '🫁 INHALE', status: 'Breathe in quietly through nose...', badgeClass: 'phase-inhale' },
    hold: { duration: 7, label: '⏸️ HOLD', status: 'Hold your breath gently...', badgeClass: 'phase-hold' },
    exhale: { duration: 8, label: '💨 EXHALE', status: 'Exhale completely through mouth...', badgeClass: 'phase-exhale' }
};

// Audio Engine State
let audioCtx = null;
let ambientNodes = {
    rain: null,
    forest: null,
    ocean: null,
    drone: null
};
let isAudioInitialized = false;

// DOM Elements
const bodyEl = document.body;
const timerCountdownEl = document.getElementById('timerCountdown');
const timerStatusEl = document.getElementById('timerStatus');
const breathePhaseBadge = document.getElementById('breathePhaseBadge');
const breatheCycleCount = document.getElementById('breatheCycleCount');
const timerDialContainer = document.getElementById('timerDialContainer');
const breakBreatheContainer = document.getElementById('breakBreatheContainer');
const btnToggleBreakBreathe = document.getElementById('btnToggleBreakBreathe');
const breakBreatheLabel = document.getElementById('breakBreatheLabel');

const btnPlayPause = document.getElementById('btnPlayPause');
const btnReset = document.getElementById('btnReset');
const btnSkip = document.getElementById('btnSkip');
const btnSettings = document.getElementById('btnSettings');
const btnSettingsClose = document.getElementById('btnSettingsClose');
const settingsModal = document.getElementById('settingsModal');
const btnSaveSettings = document.getElementById('btnSaveSettings');
const btnResetSettings = document.getElementById('btnResetSettings');
const btnFullscreen = document.getElementById('btnFullscreen');
const btnThemePicker = document.getElementById('btnThemePicker');
const themeDropdown = document.getElementById('themeDropdown');
const currentTimeEl = document.getElementById('currentTime');

const inputFocus = document.getElementById('inputFocus');
const inputShort = document.getElementById('inputShort');
const inputLong = document.getElementById('inputLong');
const selectChime = document.getElementById('selectChime');
const btnTestChime = document.getElementById('btnTestChime');
const toggleAutoFocus = document.getElementById('toggleAutoFocus');
const toggleAutoBreaks = document.getElementById('toggleAutoBreaks');
const toggleBreakBreathe = document.getElementById('toggleBreakBreathe');

const taskInput = document.getElementById('taskInput');
const btnAddTask = document.getElementById('btnAddTask');
const tasksList = document.getElementById('tasksList');
const currentFocusTaskName = document.getElementById('currentFocusTaskName');

const statPomodoros = document.getElementById('statPomodoros');
const statTime = document.getElementById('statTime');

const quoteText = document.getElementById('quoteText');
const quoteAuthor = document.getElementById('quoteAuthor');

const progressRing = document.getElementById('progressRing');
const ringCircumference = 2 * Math.PI * 95; // 596.90

/* ==========================================================================
   INITIALIZATION
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    loadTheme();
    loadTasks();
    loadStats();
    initClock();
    randomizeQuote();
    switchMode('focus');
    updateProgressRing();
    setupEventListeners();
});

// Setup Clock
function initClock() {
    const updateClock = () => {
        const now = new Date();
        let hours = now.getHours();
        let minutes = now.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // 0 should be 12
        minutes = minutes < 10 ? '0' + minutes : minutes;
        currentTimeEl.textContent = `${hours}:${minutes} ${ampm}`;
    };
    updateClock();
    setInterval(updateClock, 60000);
}

// Setup Quote
function randomizeQuote() {
    const randomIndex = Math.floor(Math.random() * MINDFUL_QUOTES.length);
    const quote = MINDFUL_QUOTES[randomIndex];
    quoteText.textContent = `"${quote.text}"`;
    quoteAuthor.textContent = `— ${quote.author}`;
}

/* ==========================================================================
   AUDIO SYNTHESIZER ENGINE (Web Audio API)
   ========================================================================== */

function initAudio() {
    if (isAudioInitialized) return;
    
    // Create AudioContext
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    audioCtx = new AudioContextClass();
    
    // Start Ambient Synthesizers
    setupRainSynth();
    setupOceanSynth();
    setupForestSynth();
    setupDroneSynth();
    
    isAudioInitialized = true;
}

// Helper: Generate Noise Buffer
function generateNoiseBuffer(type) {
    const sampleRate = audioCtx.sampleRate;
    const bufferSize = 2 * sampleRate; // 2 seconds loop buffer
    const buffer = audioCtx.createBuffer(1, bufferSize, sampleRate);
    const data = buffer.getChannelData(0);
    
    let lastOut = 0.0;
    for (let i = 0; i < bufferSize; i++) {
        const white = Math.random() * 2 - 1;
        if (type === 'white') {
            data[i] = white;
        } else if (type === 'brown') {
            // Filtered brown noise
            data[i] = (lastOut + (0.02 * white)) / 1.02;
            lastOut = data[i];
            data[i] *= 3.5; // Compensate for filter attenuation
        }
    }
    return buffer;
}

// Rain Synth: Filtered White Noise with occasional low-pass droplets
function setupRainSynth() {
    // Generate white noise buffer
    const rainBuffer = generateNoiseBuffer('white');
    const rainSource = audioCtx.createBufferSource();
    rainSource.buffer = rainBuffer;
    rainSource.loop = true;

    // Filters to shape white noise into rain
    const bandpass = audioCtx.createBiquadFilter();
    bandpass.type = 'bandpass';
    bandpass.frequency.value = 1000;
    bandpass.Q.value = 0.8;

    const lowpass = audioCtx.createBiquadFilter();
    lowpass.type = 'lowpass';
    lowpass.frequency.value = 1500;

    const gainNode = audioCtx.createGain();
    gainNode.gain.value = 0; // Default off

    // Connect nodes
    rainSource.connect(bandpass);
    bandpass.connect(lowpass);
    lowpass.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    rainSource.start(0);

    ambientNodes.rain = {
        source: rainSource,
        gain: gainNode
    };
}

// Ocean Synth: Modulated Brown Noise
function setupOceanSynth() {
    const oceanBuffer = generateNoiseBuffer('brown');
    const oceanSource = audioCtx.createBufferSource();
    oceanSource.buffer = oceanBuffer;
    oceanSource.loop = true;

    const lowpass = audioCtx.createBiquadFilter();
    lowpass.type = 'lowpass';
    lowpass.frequency.value = 350;

    const gainNode = audioCtx.createGain();
    gainNode.gain.value = 0; // Default off

    oceanSource.connect(lowpass);
    lowpass.connect(gainNode);
    gainNode.connect(audioCtx.destination);

    oceanSource.start(0);

    // Dynamic wave modulation using JavaScript automation (simulates LFO)
    let time = 0;
    setInterval(() => {
        if (gainNode.gain.value > 0) {
            time += 0.05;
            // Wave cycle: ~8 seconds
            const cycle = Math.sin(time * 2 * Math.PI / 8); 
            // Normalize cycle from -1..1 to 0..1
            const normalized = (cycle + 1) / 2; 
            
            // Modulate lowpass frequency and sub-volume
            const targetFreq = 150 + (normalized * 250); // sweeps from 150Hz to 400Hz
            const targetVolume = (0.3 + (normalized * 0.7)) * document.getElementById('sliderOcean').value / 100 * 0.15;

            lowpass.frequency.setTargetAtTime(targetFreq, audioCtx.currentTime, 0.5);
            gainNode.gain.setTargetAtTime(targetVolume, audioCtx.currentTime, 0.5);
        }
    }, 50);

    ambientNodes.ocean = {
        source: oceanSource,
        gain: gainNode
    };
}

// Forest Synth: Low wind rustle + random bird chirps
function setupForestSynth() {
    // 1. Rustle wind source (low filtered brown noise)
    const forestBuffer = generateNoiseBuffer('brown');
    const forestSource = audioCtx.createBufferSource();
    forestSource.buffer = forestBuffer;
    forestSource.loop = true;

    const lowpass = audioCtx.createBiquadFilter();
    lowpass.type = 'lowpass';
    lowpass.frequency.value = 200;

    const windGain = audioCtx.createGain();
    windGain.gain.value = 0;

    forestSource.connect(lowpass);
    lowpass.connect(windGain);
    windGain.connect(audioCtx.destination);
    forestSource.start(0);

    // 2. Bird generator
    const masterGainNode = audioCtx.createGain();
    masterGainNode.gain.value = 0; // Main controller for mixer row
    masterGainNode.connect(audioCtx.destination);
    
    // Connect wind gain to master
    windGain.disconnect(audioCtx.destination);
    windGain.connect(masterGainNode);

    // Trigger bird chirps periodically
    const triggerBirdChirp = () => {
        if (masterGainNode.gain.value > 0 && isRunning) {
            // Check if timer is running (birds chirp only when working/relaxing)
            playBirdChirp(masterGainNode);
        }
        // Next chirp in 6 to 14 seconds
        const nextDelay = 6000 + Math.random() * 8000;
        setTimeout(triggerBirdChirp, nextDelay);
    };
    setTimeout(triggerBirdChirp, 4000);

    ambientNodes.forest = {
        source: forestSource,
        gain: masterGainNode,
        windGain: windGain
    };
}

function playBirdChirp(destinationNode) {
    const now = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    
    osc.type = 'sine';
    osc.connect(gain);
    gain.connect(destinationNode);
    
    // Quick bird chirp sweep
    const duration = 0.12 + Math.random() * 0.08;
    const startFreq = 2200 + Math.random() * 400;
    const endFreq = startFreq + 1200 + Math.random() * 600;
    
    osc.frequency.setValueAtTime(startFreq, now);
    osc.frequency.exponentialRampToValueAtTime(endFreq, now + duration);
    
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.linearRampToValueAtTime(0.04, now + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);
    
    osc.start(now);
    osc.stop(now + duration + 0.05);

    // Maybe a second chirp right after
    if (Math.random() > 0.4) {
        setTimeout(() => {
            if (destinationNode.gain.value > 0) {
                const now2 = audioCtx.currentTime;
                const osc2 = audioCtx.createOscillator();
                const gain2 = audioCtx.createGain();
                
                osc2.type = 'sine';
                osc2.connect(gain2);
                gain2.connect(destinationNode);
                
                const dur2 = 0.1;
                osc2.frequency.setValueAtTime(startFreq - 200, now2);
                osc2.frequency.exponentialRampToValueAtTime(endFreq - 100, now2 + dur2);
                
                gain2.gain.setValueAtTime(0.0001, now2);
                gain2.gain.linearRampToValueAtTime(0.03, now2 + 0.02);
                gain2.gain.exponentialRampToValueAtTime(0.0001, now2 + dur2);
                
                osc2.start(now2);
                osc2.stop(now2 + dur2 + 0.05);
            }
        }, 180);
    }
}

// Ambient Cozy Drone: 4-oscillator minor seventh drone pad
function setupDroneSynth() {
    const frequencies = [87.31, 130.81, 155.56, 196.00, 233.08]; // F2, C3, Eb3, G3, Bb3 (Fmin7)
    const oscillators = [];
    const droneGainNode = audioCtx.createGain();
    droneGainNode.gain.value = 0; // Default off

    const filter = audioCtx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 320;
    
    filter.connect(droneGainNode);
    droneGainNode.connect(audioCtx.destination);

    frequencies.forEach((freq, idx) => {
        const osc = audioCtx.createOscillator();
        osc.type = 'triangle'; // Warm, soft texture
        osc.frequency.value = freq;
        
        const oscGain = audioCtx.createGain();
        oscGain.gain.value = 0.05; // low individual gain to prevent clipping

        osc.connect(oscGain);
        oscGain.connect(filter);
        osc.start(0);

        oscillators.push({ osc, gain: oscGain });

        // Slow independent volume swells
        let lfoTime = Math.random() * 100;
        setInterval(() => {
            if (droneGainNode.gain.value > 0) {
                lfoTime += 0.02;
                const swell = (Math.sin(lfoTime * (0.05 + idx * 0.01)) + 1) / 2; // slow slow swells
                oscGain.gain.setTargetAtTime(0.02 + (swell * 0.05), audioCtx.currentTime, 1.0);
            }
        }, 100);
    });

    ambientNodes.drone = {
        oscillators,
        gain: droneGainNode
    };
}

// Adjust Ambient Volume
function setAmbientVolume(soundName, volumeVal) {
    if (!isAudioInitialized) initAudio();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const gainValue = volumeVal / 100;

    if (soundName === 'rain') {
        ambientNodes.rain.gain.gain.setTargetAtTime(gainValue * 0.12, audioCtx.currentTime, 0.2);
    } else if (soundName === 'ocean') {
        // Ocean runs custom interval volume modulation, set standard volume benchmark
        ambientNodes.ocean.gain.gain.setTargetAtTime(gainValue * 0.15, audioCtx.currentTime, 0.2);
    } else if (soundName === 'forest') {
        ambientNodes.forest.gain.gain.setTargetAtTime(gainValue, audioCtx.currentTime, 0.2);
        ambientNodes.forest.windGain.gain.setTargetAtTime(gainValue * 0.2, audioCtx.currentTime, 0.2);
    } else if (soundName === 'drone') {
        ambientNodes.drone.gain.gain.setTargetAtTime(gainValue * 0.5, audioCtx.currentTime, 0.2);
    }
}

// Synthesize Custom Notification Chimes
function playNotificationChime(style) {
    if (!isAudioInitialized) initAudio();
    if (audioCtx.state === 'suspended') audioCtx.resume();

    const now = audioCtx.currentTime;

    if (style === 'singing-bowl') {
        // Synthesizes a deep Tibetan singing bowl bell (zen vibe)
        const fundamental = 180; // F3
        const partials = [1, 1.52, 2.22, 2.78, 3.42]; // non-harmonic resonance ratios
        const gains = [0.4, 0.25, 0.15, 0.1, 0.05];
        
        partials.forEach((ratio, index) => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            
            osc.type = 'sine';
            osc.frequency.value = fundamental * ratio;
            
            // Singing Bowls decay extremely slowly
            gain.gain.setValueAtTime(0, now);
            gain.gain.linearRampToValueAtTime(gains[index] * 0.4, now + 0.08);
            
            // Tremolo / Beating effect
            const tremolo = audioCtx.createGain();
            const lfo = audioCtx.createOscillator();
            lfo.frequency.value = 2.5; // 2.5Hz amplitude beating
            
            const lfoGain = audioCtx.createGain();
            lfoGain.gain.value = 0.15; // Tremolo depth
            
            lfo.connect(lfoGain);
            lfoGain.connect(tremolo.gain);
            tremolo.gain.setValueAtTime(0.85, now);
            
            osc.connect(tremolo);
            tremolo.connect(gain);
            gain.connect(audioCtx.destination);
            
            lfo.start(now);
            osc.start(now);
            
            // Exponential decay
            gain.gain.exponentialRampToValueAtTime(0.0001, now + 6);
            
            osc.stop(now + 6.2);
            lfo.stop(now + 6.2);
        });
    } else if (style === 'warm-chime') {
        // High-pitched soothing bar chime
        const fundamental = 523.25; // C5
        const partials = [1, 1.5, 2, 2.5];
        const gains = [0.3, 0.15, 0.1, 0.05];

        partials.forEach((ratio, index) => {
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            
            osc.type = 'sine';
            osc.frequency.value = fundamental * ratio;
            
            gain.gain.setValueAtTime(0, now);
            gain.gain.linearRampToValueAtTime(gains[index] * 0.35, now + 0.02);
            gain.gain.exponentialRampToValueAtTime(0.0001, now + 2);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.start(now);
            osc.stop(now + 2.1);
        });
    } else if (style === 'digital-pip') {
        // Soft short digital beep
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        
        osc.type = 'sine';
        osc.frequency.value = 880; // A5
        
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(0.2, now + 0.01);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.15);
        
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        
        osc.start(now);
        osc.stop(now + 0.2);
    }
}

/* ==========================================================================
   TIMER CORE ENGINE
   ========================================================================== */

function updateTimerDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    const formattedSeconds = seconds < 10 ? '0' + seconds : seconds;
    const formattedMinutes = minutes < 10 ? '0' + minutes : minutes;
    
    const displayStr = `${formattedMinutes}:${formattedSeconds}`;
    timerCountdownEl.textContent = displayStr;
    
    // Update Page Title with Timer state
    const modeLabel = currentMode === 'focus' ? 'Focus' : 'Break';
    document.title = `${displayStr} | ${modeLabel} — AURA`;
}

function updateProgressRing() {
    const fraction = timeLeft / totalDuration;
    // Circular offset: 0 is full (dashoffset = 0), 1 is empty (dashoffset = ringCircumference)
    const offset = ringCircumference - (fraction * ringCircumference);
    progressRing.style.strokeDashoffset = offset;
}

function tick() {
    if (timeLeft > 0) {
        timeLeft--;
        updateTimerDisplay();
        updateProgressRing();
        if ((currentMode === 'short' || currentMode === 'long') && isBreakBreatheActive && isRunning) {
            tickBreakBreatheCycle();
        }
    } else {
        // Session Complete!
        handleSessionEnd();
    }
}

function tickBreakBreatheCycle() {
    if (breatheSecondsLeft > 1) {
        breatheSecondsLeft--;
    } else {
        if (breathePhase === 'inhale') {
            breathePhase = 'hold';
            breatheSecondsLeft = 7;
        } else if (breathePhase === 'hold') {
            breathePhase = 'exhale';
            breatheSecondsLeft = 8;
        } else if (breathePhase === 'exhale') {
            breathePhase = 'inhale';
            breatheSecondsLeft = 4;
        }
        playBreathingAudioTone(breathePhase);
    }
    updateBreakBreatheUI();
}

function updateBreakBreatheUI() {
    const config = BREATHE_PHASES[breathePhase];
    breathePhaseBadge.textContent = `${config.label} (${breatheSecondsLeft}s)`;
    breathePhaseBadge.className = `breathe-phase-badge ${config.badgeClass}`;
    timerDialContainer.className = `timer-dial-container breathe-${breathePhase}`;
}

function switchMode(mode) {
    currentMode = mode;
    
    // Clear active mode styles
    document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
    bodyEl.classList.remove('theme-focus', 'theme-short', 'theme-long', 'theme-breathe');
    
    if (mode === 'focus') {
        document.getElementById('modeFocus').classList.add('active');
        bodyEl.classList.add('theme-focus');
        totalDuration = settings.durationFocus * 60;
        timerStatusEl.textContent = isRunning ? 'Deep Flowing...' : "Let's Begin";
        breathePhaseBadge.style.display = 'none';
        breatheCycleCount.style.display = 'none';
        breakBreatheContainer.style.display = 'none';
        timerDialContainer.className = 'timer-dial-container';
        progressRing.style.transition = 'stroke var(--transition-slow), stroke-dashoffset 0.3s linear';
        timeLeft = totalDuration;
        updateTimerDisplay();
        updateProgressRing();
    } else if (mode === 'short' || mode === 'long') {
        const isShort = mode === 'short';
        document.getElementById(isShort ? 'modeShort' : 'modeLong').classList.add('active');
        bodyEl.classList.add(isShort ? 'theme-short' : 'theme-long');
        totalDuration = (isShort ? settings.durationShort : settings.durationLong) * 60;
        timerStatusEl.textContent = isRunning ? 'Rest & Breathe...' : (isShort ? 'Time to Breathe' : 'Extended Pause');
        
        breatheCycleCount.style.display = 'none';
        progressRing.style.transition = 'stroke var(--transition-slow), stroke-dashoffset 0.3s linear';
        timeLeft = totalDuration;
        updateTimerDisplay();
        updateProgressRing();

        if (settings.guideBreakBreathe !== false && isBreakBreatheActive) {
            breakBreatheContainer.style.display = 'flex';
            breathePhaseBadge.style.display = 'inline-block';
            breathePhase = 'inhale';
            breatheSecondsLeft = 4;
            updateBreakBreatheUI();
        } else {
            breakBreatheContainer.style.display = 'none';
            breathePhaseBadge.style.display = 'none';
            timerDialContainer.className = 'timer-dial-container';
        }
    } else if (mode === 'breathe') {
        document.getElementById('modeBreathe').classList.add('active');
        bodyEl.classList.add('theme-breathe');
        breathePhaseBadge.style.display = 'inline-block';
        breatheCycleCount.style.display = 'block';
        breakBreatheContainer.style.display = 'none';
        
        breatheCycle = 1;
        startBreathePhase('inhale');
    }
}

function handleSessionEnd() {
    clearInterval(timerInterval);
    timerInterval = null;
    isRunning = false;
    btnPlayPause.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="play-icon"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>';
    
    // Play Notification Bell
    playNotificationChime(settings.chimeStyle);

    // Update Stats & Active Tasks
    if (currentMode === 'focus') {
        stats.pomodorosCompleted++;
        stats.totalFocusMinutes += settings.durationFocus;
        saveStats();
        updateStatsUI();

        // Increment active task focus
        if (activeTaskId) {
            const activeTask = tasks.find(t => t.id === activeTaskId);
            if (activeTask) {
                activeTask.focusSessions = (activeTask.focusSessions || 0) + 1;
                saveTasks();
                renderTasks();
            }
        }
    }

    // Switch modes automatically or prepare next
    let nextMode = 'focus';
    if (currentMode === 'focus') {
        // Focus done -> short break unless 4 consecutive cycles are completed (then long break)
        if (stats.pomodorosCompleted % 4 === 0 && stats.pomodorosCompleted > 0) {
            nextMode = 'long';
        } else {
            nextMode = 'short';
        }
    } else {
        // Break done -> focus
        nextMode = 'focus';
    }

    switchMode(nextMode);
    randomizeQuote();

    // Handle Auto Start options
    const shouldAutoStart = (nextMode === 'focus' && settings.autoStartFocus) || 
                            (nextMode !== 'focus' && settings.autoStartBreaks);

    if (shouldAutoStart) {
        setTimeout(startTimer, 1000); // 1s buffer for chime
    }
}

function startTimer() {
    if (!isAudioInitialized) initAudio();
    
    isRunning = true;
    btnPlayPause.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="pause-icon"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>';
    
    if (currentMode === 'breathe') {
        startBreathePhase(breathePhase);
        timerInterval = setInterval(tickBreathe, 1000);
    } else {
        timerStatusEl.textContent = currentMode === 'focus' ? 'Deep Flowing...' : 'Rest Your Mind...';
        timerInterval = setInterval(tick, 1000);
    }
}

function pauseTimer() {
    isRunning = false;
    btnPlayPause.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="play-icon"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>';
    timerStatusEl.textContent = currentMode === 'breathe' ? 'Breathing Paused' : 'Flow Paused';
    
    clearInterval(timerInterval);
    timerInterval = null;
}

function resetTimer() {
    pauseTimer();
    if (currentMode === 'breathe') {
        breatheCycle = 1;
        breathePhase = 'inhale';
        breatheSecondsLeft = 4;
    }
    // Re-initialize time values
    switchMode(currentMode);
}

function skipTimer() {
    pauseTimer();
    if (currentMode === 'breathe') {
        advanceBreathePhase();
    } else {
        // Simulate natural timer expiration
        timeLeft = 0;
        handleSessionEnd();
    }
}

/* ==========================================================================
   4-7-8 BREATHING TECHNIQUE LOGIC
   ========================================================================== */

function startBreathePhase(phase) {
    breathePhase = phase;
    const config = BREATHE_PHASES[phase];
    breatheSecondsLeft = config.duration;
    
    // Update Badge
    breathePhaseBadge.textContent = config.label;
    breathePhaseBadge.className = `breathe-phase-badge ${config.badgeClass}`;
    timerStatusEl.textContent = config.status;
    breatheCycleCount.textContent = `Cycle ${breatheCycle} of 4`;
    
    timerCountdownEl.textContent = `${breatheSecondsLeft}s`;
    
    // Animate Dial progress ring
    timerDialContainer.className = `timer-dial-container breathe-${phase}`;
    if (phase === 'inhale') {
        progressRing.style.transition = 'stroke-dashoffset 4s linear';
        progressRing.style.strokeDashoffset = 0; // Fill ring fully over 4s
    } else if (phase === 'hold') {
        progressRing.style.transition = 'none';
        progressRing.style.strokeDashoffset = 0; // Keep full during 7s hold
    } else if (phase === 'exhale') {
        progressRing.style.transition = 'stroke-dashoffset 8s linear';
        progressRing.style.strokeDashoffset = ringCircumference; // Empty ring over 8s
    }
    
    playBreathingAudioTone(phase);
}

function tickBreathe() {
    if (breatheSecondsLeft > 1) {
        breatheSecondsLeft--;
        timerCountdownEl.textContent = `${breatheSecondsLeft}s`;
    } else {
        advanceBreathePhase();
    }
}

function advanceBreathePhase() {
    if (breathePhase === 'inhale') {
        startBreathePhase('hold');
    } else if (breathePhase === 'hold') {
        startBreathePhase('exhale');
    } else if (breathePhase === 'exhale') {
        if (breatheCycle < 4) {
            breatheCycle++;
            startBreathePhase('inhale');
        } else {
            // Completed 4 full cycles!
            pauseTimer();
            playNotificationChime('singing-bowl');
            timerStatusEl.textContent = '4-7-8 Session Complete 🧘';
            timerCountdownEl.textContent = 'Peace';
            breathePhaseBadge.textContent = 'COMPLETE';
            breathePhaseBadge.className = 'breathe-phase-badge phase-inhale';
            breatheCycleCount.textContent = '4 Cycles Completed';
        }
    }
}

function playBreathingAudioTone(phase) {
    if (!isAudioInitialized || !audioCtx) return;
    if (audioCtx.state === 'suspended') audioCtx.resume();
    
    const now = audioCtx.currentTime;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.connect(gain);
    gain.connect(audioCtx.destination);

    if (phase === 'inhale') {
        osc.frequency.setValueAtTime(220, now);
        osc.frequency.exponentialRampToValueAtTime(440, now + 4);
        gain.gain.setValueAtTime(0.001, now);
        gain.gain.linearRampToValueAtTime(0.08, now + 0.5);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 4);
        osc.start(now);
        osc.stop(now + 4.1);
    } else if (phase === 'hold') {
        osc.frequency.setValueAtTime(440, now);
        gain.gain.setValueAtTime(0.001, now);
        gain.gain.linearRampToValueAtTime(0.04, now + 0.3);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 7);
        osc.start(now);
        osc.stop(now + 7.1);
    } else if (phase === 'exhale') {
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(220, now + 8);
        gain.gain.setValueAtTime(0.001, now);
        gain.gain.linearRampToValueAtTime(0.07, now + 0.5);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 8);
        osc.start(now);
        osc.stop(now + 8.1);
    }
}

function switchMode(mode) {
    currentMode = mode;
    
    // Clear active mode styles
    document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
    bodyEl.classList.remove('theme-focus', 'theme-short', 'theme-long', 'theme-breathe');
    
    if (mode === 'focus') {
        document.getElementById('modeFocus').classList.add('active');
        bodyEl.classList.add('theme-focus');
        totalDuration = settings.durationFocus * 60;
        timerStatusEl.textContent = isRunning ? 'Deep Flowing...' : "Let's Begin";
        breathePhaseBadge.style.display = 'none';
        breatheCycleCount.style.display = 'none';
        progressRing.style.transition = 'stroke var(--transition-slow), stroke-dashoffset 0.3s linear';
        timeLeft = totalDuration;
        updateTimerDisplay();
        updateProgressRing();
    } else if (mode === 'short') {
        document.getElementById('modeShort').classList.add('active');
        bodyEl.classList.add('theme-short');
        totalDuration = settings.durationShort * 60;
        timerStatusEl.textContent = isRunning ? 'Rest Your Mind...' : 'Time to Breathe';
        breathePhaseBadge.style.display = 'none';
        breatheCycleCount.style.display = 'none';
        progressRing.style.transition = 'stroke var(--transition-slow), stroke-dashoffset 0.3s linear';
        timeLeft = totalDuration;
        updateTimerDisplay();
        updateProgressRing();
    } else if (mode === 'long') {
        document.getElementById('modeLong').classList.add('active');
        bodyEl.classList.add('theme-long');
        totalDuration = settings.durationLong * 60;
        timerStatusEl.textContent = isRunning ? 'Deeply Rest...' : 'Extended Pause';
        breathePhaseBadge.style.display = 'none';
        breatheCycleCount.style.display = 'none';
        progressRing.style.transition = 'stroke var(--transition-slow), stroke-dashoffset 0.3s linear';
        timeLeft = totalDuration;
        updateTimerDisplay();
        updateProgressRing();
    } else if (mode === 'breathe') {
        document.getElementById('modeBreathe').classList.add('active');
        bodyEl.classList.add('theme-breathe');
        breathePhaseBadge.style.display = 'inline-block';
        breatheCycleCount.style.display = 'block';
        
        breatheCycle = 1;
        startBreathePhase('inhale');
    }
}

/* ==========================================================================
   MINDFUL TASK MANAGER
   ========================================================================== */

function loadTasks() {
    const raw = localStorage.getItem('aura_tasks');
    tasks = raw ? JSON.parse(raw) : [];
    
    const savedActiveId = localStorage.getItem('aura_active_task_id');
    if (savedActiveId) activeTaskId = parseInt(savedActiveId, 10);
    
    renderTasks();
    updateActiveTaskUI();
}

function saveTasks() {
    localStorage.setItem('aura_tasks', JSON.stringify(tasks));
    if (activeTaskId) {
        localStorage.setItem('aura_active_task_id', activeTaskId);
    } else {
        localStorage.removeItem('aura_active_task_id');
    }
}

function renderTasks() {
    tasksList.innerHTML = '';
    
    if (tasks.length === 0) {
        tasksList.innerHTML = `<li class="panel-subtitle" style="text-align: center; margin-top: 1rem; list-style: none;">No intentions created yet.</li>`;
        return;
    }
    
    tasks.forEach(task => {
        const li = document.createElement('li');
        li.className = `task-item ${task.completed ? 'completed' : ''} ${task.id === activeTaskId ? 'active' : ''}`;
        li.dataset.id = task.id;
        
        const sessionsText = task.focusSessions ? `(${task.focusSessions} ⏱️)` : '';
        
        li.innerHTML = `
            <div class="task-item-left">
                <span class="task-checkbox" aria-label="Toggle task completed"></span>
                <span class="task-text">${escapeHTML(task.text)} ${sessionsText}</span>
            </div>
            <button class="task-btn-delete" aria-label="Delete intention">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
            </button>
        `;
        
        // Task interaction: checkbox click vs list item click (select) vs delete click
        li.querySelector('.task-checkbox').addEventListener('click', (e) => {
            e.stopPropagation();
            toggleTaskCompleted(task.id);
        });
        
        li.querySelector('.task-btn-delete').addEventListener('click', (e) => {
            e.stopPropagation();
            deleteTask(task.id);
        });
        
        li.addEventListener('click', () => {
            selectTask(task.id);
        });
        
        tasksList.appendChild(li);
    });
}

function selectTask(id) {
    if (activeTaskId === id) {
        // Toggle off
        activeTaskId = null;
    } else {
        // Set new active
        const task = tasks.find(t => t.id === id);
        if (task && !task.completed) {
            activeTaskId = id;
        }
    }
    saveTasks();
    renderTasks();
    updateActiveTaskUI();
}

function updateActiveTaskUI() {
    if (activeTaskId) {
        const task = tasks.find(t => t.id === activeTaskId);
        if (task) {
            currentFocusTaskName.textContent = task.text;
            return;
        }
    }
    currentFocusTaskName.textContent = "No active intention selected";
}

function addTask() {
    const text = taskInput.value.trim();
    if (!text) return;
    
    const newTask = {
        id: Date.now(),
        text: text,
        completed: false,
        focusSessions: 0
    };
    
    tasks.push(newTask);
    taskInput.value = '';
    
    // Auto select first task if nothing is selected
    if (!activeTaskId) {
        activeTaskId = newTask.id;
    }
    
    saveTasks();
    renderTasks();
    updateActiveTaskUI();
}

function toggleTaskCompleted(id) {
    const task = tasks.find(t => t.id === id);
    if (task) {
        task.completed = !task.completed;
        // If completed task was active focus, clear active focus
        if (task.completed && activeTaskId === id) {
            activeTaskId = null;
        }
        saveTasks();
        renderTasks();
        updateActiveTaskUI();
    }
}

function deleteTask(id) {
    tasks = tasks.filter(t => t.id !== id);
    if (activeTaskId === id) {
        activeTaskId = null;
    }
    saveTasks();
    renderTasks();
    updateActiveTaskUI();
}

function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}

/* ==========================================================================
   SETTINGS & STATISTICS
   ========================================================================== */

function loadSettings() {
    const raw = localStorage.getItem('aura_settings');
    if (raw) {
        settings = { ...DEFAULT_SETTINGS, ...JSON.parse(raw) };
    }
    
    // Populate form values
    inputFocus.value = settings.durationFocus;
    inputShort.value = settings.durationShort;
    inputLong.value = settings.durationLong;
    selectChime.value = settings.chimeStyle;
    toggleAutoFocus.checked = settings.autoStartFocus;
    toggleAutoBreaks.checked = settings.autoStartBreaks;
    if (toggleBreakBreathe) toggleBreakBreathe.checked = settings.guideBreakBreathe !== false;
}

function saveSettingsToStorage() {
    settings.durationFocus = parseInt(inputFocus.value, 10) || DEFAULT_SETTINGS.durationFocus;
    settings.durationShort = parseInt(inputShort.value, 10) || DEFAULT_SETTINGS.durationShort;
    settings.durationLong = parseInt(inputLong.value, 10) || DEFAULT_SETTINGS.durationLong;
    settings.chimeStyle = selectChime.value;
    settings.autoStartFocus = toggleAutoFocus.checked;
    settings.autoStartBreaks = toggleAutoBreaks.checked;
    if (toggleBreakBreathe) settings.guideBreakBreathe = toggleBreakBreathe.checked;
    
    localStorage.setItem('aura_settings', JSON.stringify(settings));
}

function loadStats() {
    const raw = localStorage.getItem('aura_stats');
    if (raw) stats = JSON.parse(raw);
    updateStatsUI();
}

function saveStats() {
    localStorage.setItem('aura_stats', JSON.stringify(stats));
}

function updateStatsUI() {
    statPomodoros.textContent = stats.pomodorosCompleted;
    statTime.textContent = `${stats.totalFocusMinutes}m`;
}

function resetStats() {
    stats = { pomodorosCompleted: 0, totalFocusMinutes: 0 };
    saveStats();
    updateStatsUI();
}

/* ==========================================================================
   EVENT LISTENERS & UI TRIGGERS
   ========================================================================== */

function setupEventListeners() {
    // 0. Break Breathing Toggle Listener
    if (btnToggleBreakBreathe) {
        btnToggleBreakBreathe.addEventListener('click', () => {
            isBreakBreatheActive = !isBreakBreatheActive;
            if (isBreakBreatheActive) {
                btnToggleBreakBreathe.classList.add('active');
                breakBreatheLabel.textContent = '🫁 4-7-8 Breathing Guide Active';
                breathePhaseBadge.style.display = 'inline-block';
                breathePhase = 'inhale';
                breatheSecondsLeft = 4;
                updateBreakBreatheUI();
            } else {
                btnToggleBreakBreathe.classList.remove('active');
                breakBreatheLabel.textContent = '🫁 4-7-8 Breathing Guide Off';
                breathePhaseBadge.style.display = 'none';
                timerDialContainer.className = 'timer-dial-container';
            }
        });
    }

    // 1. Timer Control Events
    btnPlayPause.addEventListener('click', () => {
        initAudio(); // Bind on interaction
        if (isRunning) {
            pauseTimer();
        } else {
            startTimer();
        }
    });

    btnReset.addEventListener('click', () => {
        initAudio();
        resetTimer();
    });

    btnSkip.addEventListener('click', () => {
        initAudio();
        if (confirm("Skip this active session?")) {
            skipTimer();
        }
    });

    // 2. Mode Change Buttons
    document.getElementById('timerModes').addEventListener('click', (e) => {
        if (e.target.classList.contains('mode-btn')) {
            initAudio();
            const mode = e.target.dataset.mode;
            if (isRunning) {
                if (confirm("Timer is active. Switch modes and discard current progress?")) {
                    switchMode(mode);
                }
            } else {
                switchMode(mode);
            }
        }
    });

    // 3. Ambient Mixer Volume Sliders
    document.querySelectorAll('.volume-slider').forEach(slider => {
        slider.addEventListener('input', (e) => {
            const sound = e.target.closest('.mixer-row').dataset.sound;
            const value = e.target.value;
            setAmbientVolume(sound, value);
            
            // Handle mute icon state
            const muteBtn = e.target.previousElementSibling;
            if (value == 0) {
                muteBtn.textContent = '🔇';
            } else {
                muteBtn.textContent = '🔊';
            }
        });
    });

    // Ambient Mixer Mute Toggles
    document.querySelectorAll('.mute-toggle').forEach(muteBtn => {
        muteBtn.addEventListener('click', (e) => {
            const row = e.target.closest('.mixer-row');
            const slider = row.querySelector('.volume-slider');
            const sound = row.dataset.sound;
            
            if (slider.value > 0) {
                // Save old value temporarily
                row.dataset.oldVal = slider.value;
                slider.value = 0;
                muteBtn.textContent = '🔇';
                setAmbientVolume(sound, 0);
            } else {
                const restoredVal = row.dataset.oldVal || 40;
                slider.value = restoredVal;
                muteBtn.textContent = '🔊';
                setAmbientVolume(sound, restoredVal);
            }
        });
    });

    // 4. Intention Task input
    btnAddTask.addEventListener('click', addTask);
    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') addTask();
    });

    // 5. Settings Modal triggers
    btnSettings.addEventListener('click', () => {
        initAudio();
        settingsModal.classList.add('open');
    });

    btnSettingsClose.addEventListener('click', () => {
        settingsModal.classList.remove('open');
        loadSettings(); // revert form inputs
    });

    settingsModal.addEventListener('click', (e) => {
        if (e.target === settingsModal) {
            settingsModal.classList.remove('open');
            loadSettings(); // revert form inputs
        }
    });

    btnTestChime.addEventListener('click', () => {
        playNotificationChime(selectChime.value);
    });

    btnSaveSettings.addEventListener('click', () => {
        saveSettingsToStorage();
        settingsModal.classList.remove('open');
        resetTimer(); // Apply new times immediately
    });

    btnResetSettings.addEventListener('click', () => {
        if (confirm("Restore default configurations?")) {
            settings = { ...DEFAULT_SETTINGS };
            localStorage.setItem('aura_settings', JSON.stringify(settings));
            loadSettings();
            resetTimer();
        }
    });

    // 6. Fullscreen / Focus Mode toggle
    btnFullscreen.addEventListener('click', () => {
        bodyEl.classList.toggle('fullscreen-mode');
        const isFullscreen = bodyEl.classList.contains('fullscreen-mode');
        
        if (isFullscreen) {
            btnFullscreen.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-minimize"><path d="M4 14h6v6m10-6h-6v6M4 10h6V4m10 6h-6V4"></path></svg>';
            btnFullscreen.title = "Exit Focus Mode";
        } else {
            btnFullscreen.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-maximize"><path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0 0 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"></path></svg>';
            btnFullscreen.title = "Toggle Focus Mode";
        }
    });

    // 7. Background Theme Picker toggle & selection
    if (btnThemePicker && themeDropdown) {
        btnThemePicker.addEventListener('click', (e) => {
            e.stopPropagation();
            themeDropdown.classList.toggle('open');
        });

        document.querySelectorAll('.theme-option').forEach(option => {
            option.addEventListener('click', (e) => {
                e.stopPropagation();
                const selectedTheme = option.dataset.theme;
                applyTheme(selectedTheme);
                themeDropdown.classList.remove('open');
            });
        });

        document.addEventListener('click', (e) => {
            if (!themeDropdown.contains(e.target) && e.target !== btnThemePicker) {
                themeDropdown.classList.remove('open');
            }
        });
    }
}

/* ==========================================================================
   THEME MANAGEMENT
   ========================================================================== */

function loadTheme() {
    const savedTheme = localStorage.getItem('aura_theme') || 'mistyforest';
    applyTheme(savedTheme);
}

function applyTheme(themeName) {
    const themeClasses = ['bg-mistyforest', 'bg-sunset', 'bg-emerald', 'bg-midnight', 'bg-obsidian', 'bg-aurora', 'bg-rosequartz'];
    bodyEl.classList.remove(...themeClasses);
    bodyEl.classList.add(`bg-${themeName}`);
    
    // Save to localStorage
    localStorage.setItem('aura_theme', themeName);

    // Update active dropdown item
    document.querySelectorAll('.theme-option').forEach(opt => {
        if (opt.dataset.theme === themeName) {
            opt.classList.add('active');
        } else {
            opt.classList.remove('active');
        }
    });
}

