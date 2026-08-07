// ZenSpace - Timer and Task Manager Logic

document.addEventListener("DOMContentLoaded", () => {
  // --- DOM Elements ---
  const timerClock = document.getElementById("timer-clock");
  const timerLabel = document.getElementById("timer-label");
  const playBtn = document.getElementById("play-btn");
  const playIcon = document.getElementById("play-icon");
  const pauseIcon = document.getElementById("pause-icon");
  const resetBtn = document.getElementById("reset-btn");
  const skipBtn = document.getElementById("skip-btn");
  const pomoCountDisplay = document.getElementById("pomo-count");
  const timerDisplayWrap = document.querySelector(".timer-display-wrap");

  // Mode Selection
  const modeBtns = document.querySelectorAll(".mode-btn");

  // Circular Progress Ring
  const circle = document.querySelector(".progress-ring__circle");
  const radius = circle.r.baseVal.value;
  const circumference = 2 * Math.PI * radius;

  // Task List
  const taskForm = document.getElementById("add-task-form");
  const taskInput = document.getElementById("task-input");
  const taskList = document.getElementById("task-list");
  const taskProgress = document.getElementById("task-progress");
  const emptyState = document.getElementById("tasks-empty-state");
  const testAudioBtn = document.getElementById("test-audio-btn");
  const soundSelect = document.getElementById("sound-select");

  // --- Configuration & State ---
  const CONFIG = {
    work: 25 * 60,       // 25 minutes
    short: 5 * 60,       // 5 minutes
    long: 15 * 60        // 15 minutes
  };

  let currentMode = "work"; // work, short, long
  let timeLeft = CONFIG[currentMode];
  let timerId = null;
  let isRunning = false;
  let completedPomos = parseInt(localStorage.getItem("completedPomos") || "0", 10);
  let tasks = JSON.parse(localStorage.getItem("tasks") || "[]");

  // Initialize Circular SVG Dasharray
  circle.style.strokeDasharray = `${circumference} ${circumference}`;
  circle.style.strokeDashoffset = circumference;

  // Initialize UI
  updateClockDisplay();
  updateProgressRing();
  pomoCountDisplay.textContent = completedPomos;
  renderTasks();

  // --- Web Audio Alert Synthesizer ---
  function playAlertSound() {
    const selectedSound = soundSelect.value;
    
    try {
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      
      if (selectedSound === "bowl") {
        // --- Tibetan Singing Bowl (Deep resonant gong with complex harmonics) ---
        const playTone = (freq, volume, duration) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
          
          gain.gain.setValueAtTime(0, audioCtx.currentTime);
          gain.gain.linearRampToValueAtTime(volume, audioCtx.currentTime + 0.1);
          gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration);
          
          osc.start(audioCtx.currentTime);
          osc.stop(audioCtx.currentTime + duration + 0.5);
        };
        
        playTone(220.00, 0.35, 3.5); // A3 Fundamental
        playTone(440.00, 0.12, 3.0); // A4 Octave
        playTone(660.00, 0.08, 2.5); // E5 Perfect 5th
        playTone(968.00, 0.05, 2.0); // Inharmonic overtone
        playTone(1320.00, 0.03, 1.5); // Higher resonance
        
      } else if (selectedSound === "digital") {
        // --- Minimal Digital (Clean modern staccato arpeggio) ---
        const playBeep = (freq, delay, duration) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, audioCtx.currentTime + delay);
          
          gain.gain.setValueAtTime(0, audioCtx.currentTime + delay);
          gain.gain.linearRampToValueAtTime(0.15, audioCtx.currentTime + delay + 0.01);
          gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + delay + duration);
          
          osc.start(audioCtx.currentTime + delay);
          osc.stop(audioCtx.currentTime + delay + duration + 0.1);
        };
        
        playBeep(1046.50, 0.0, 0.1);   // C6
        playBeep(1318.51, 0.12, 0.1);  // E6
        playBeep(1567.98, 0.24, 0.2);  // G6
        
      } else if (selectedSound === "chirp") {
        // --- Nature Forest Chirp (Double avian frequency sweep) ---
        const playSweep = (startFreq, endFreq, delay, duration) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          
          osc.type = 'sine';
          osc.frequency.setValueAtTime(startFreq, audioCtx.currentTime + delay);
          osc.frequency.exponentialRampToValueAtTime(endFreq, audioCtx.currentTime + delay + duration);
          
          gain.gain.setValueAtTime(0, audioCtx.currentTime + delay);
          gain.gain.linearRampToValueAtTime(0.12, audioCtx.currentTime + delay + 0.02);
          gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + delay + duration);
          
          osc.start(audioCtx.currentTime + delay);
          osc.stop(audioCtx.currentTime + delay + duration + 0.1);
        };
        
        playSweep(1800, 2800, 0.0, 0.12);
        playSweep(2000, 3000, 0.18, 0.15);
        
      } else {
        // --- Zen Chime (Default calm dual-tone bell chime) ---
        const osc1 = audioCtx.createOscillator();
        const gain1 = audioCtx.createGain();
        osc1.connect(gain1);
        gain1.connect(audioCtx.destination);
        osc1.type = 'sine';
        osc1.frequency.setValueAtTime(523.25, audioCtx.currentTime); // C5
        
        gain1.gain.setValueAtTime(0, audioCtx.currentTime);
        gain1.gain.linearRampToValueAtTime(0.25, audioCtx.currentTime + 0.05);
        gain1.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 1.2);
        
        const osc2 = audioCtx.createOscillator();
        const gain2 = audioCtx.createGain();
        osc2.connect(gain2);
        gain2.connect(audioCtx.destination);
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(783.99, audioCtx.currentTime); // G5
        
        gain2.gain.setValueAtTime(0, audioCtx.currentTime);
        gain2.gain.linearRampToValueAtTime(0.12, audioCtx.currentTime + 0.08);
        gain2.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + 1.6);
  
        osc1.start(audioCtx.currentTime);
        osc2.start(audioCtx.currentTime);
        osc1.stop(audioCtx.currentTime + 1.5);
        osc2.stop(audioCtx.currentTime + 2.0);
      }
    } catch (e) {
      console.warn("Web Audio API is not supported or blocked: ", e);
    }
  }

  // --- Timer Operations ---

  function updateClockDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    const formattedTime = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    
    timerClock.textContent = formattedTime;

    // Update document title with remaining time for convenience
    const modeLabel = currentMode === "work" ? "Focus" : "Break";
    document.title = isRunning ? `(${formattedTime}) ZenSpace - ${modeLabel}` : "ZenSpace - Pomodoro Timer";
  }

  function updateProgressRing() {
    const totalDuration = CONFIG[currentMode];
    const elapsed = totalDuration - timeLeft;
    const percent = elapsed / totalDuration;
    const offset = circumference - (percent * circumference);
    
    circle.style.strokeDashoffset = offset;
  }

  function startTimer() {
    if (isRunning) return;

    isRunning = true;
    playIcon.classList.add("hidden");
    pauseIcon.classList.remove("hidden");
    timerDisplayWrap.classList.add("running");

    timerId = setInterval(() => {
      if (timeLeft > 0) {
        timeLeft--;
        updateClockDisplay();
        updateProgressRing();
      } else {
        handleTimerCompletion();
      }
    }, 1000);
  }

  function pauseTimer() {
    if (!isRunning) return;

    isRunning = false;
    clearInterval(timerId);
    playIcon.classList.remove("hidden");
    pauseIcon.classList.add("hidden");
    timerDisplayWrap.classList.remove("running");
  }

  function resetTimer() {
    pauseTimer();
    timeLeft = CONFIG[currentMode];
    updateClockDisplay();
    updateProgressRing();
  }

  function skipMode() {
    pauseTimer();
    // Auto-advance mode in sequence: Focus -> Break -> Focus...
    if (currentMode === "work") {
      switchMode(completedPomos > 0 && completedPomos % 4 === 0 ? "long" : "short");
    } else {
      switchMode("work");
    }
  }

  function switchMode(mode) {
    currentMode = mode;
    
    // Update theme accents in document
    const root = document.documentElement;

    if (mode === "work") {
      root.style.setProperty("--accent", "var(--accent-work)");
      root.style.setProperty("--accent-glow", "var(--accent-work-glow)");
      timerLabel.textContent = "Work Session";
    } else if (mode === "short") {
      root.style.setProperty("--accent", "var(--accent-break)");
      root.style.setProperty("--accent-glow", "var(--accent-break-glow)");
      timerLabel.textContent = "Short Break";
    } else {
      root.style.setProperty("--accent", "var(--accent-long)");
      root.style.setProperty("--accent-glow", "var(--accent-long-glow)");
      timerLabel.textContent = "Long Break";
    }

    // Toggle active pill button
    modeBtns.forEach((btn) => {
      if (btn.getAttribute("data-mode") === mode) {
        btn.classList.add("active");
      } else {
        btn.classList.remove("active");
      }
    });

    resetTimer();
  }

  function handleTimerCompletion() {
    pauseTimer();
    playAlertSound();

    if (currentMode === "work") {
      completedPomos++;
      localStorage.setItem("completedPomos", completedPomos);
      pomoCountDisplay.textContent = completedPomos;
      
      // Auto toggle to break
      const isLongBreak = completedPomos % 4 === 0;
      switchMode(isLongBreak ? "long" : "short");
    } else {
      // Auto toggle back to work
      switchMode("work");
    }
  }

  // --- Task Manager Operations ---

  function renderTasks() {
    taskList.innerHTML = "";
    
    if (tasks.length === 0) {
      emptyState.classList.remove("hidden");
    } else {
      emptyState.classList.add("hidden");
      
      tasks.forEach((task) => {
        const item = document.createElement("li");
        item.className = `task-item ${task.completed ? 'completed' : ''}`;
        item.setAttribute("data-id", task.id);

        item.innerHTML = `
          <div class="task-left">
            <div class="checkbox-custom">
              <svg viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>
            </div>
            <span class="task-text">${escapeHTML(task.text)}</span>
          </div>
          <button class="delete-task-btn" title="Delete intention">
            <svg viewBox="0 0 24 24"><path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/></svg>
          </button>
        `;

        taskList.appendChild(item);
      });
    }

    updateTaskProgress();
  }

  function updateTaskProgress() {
    const completedCount = tasks.filter(t => t.completed).length;
    taskProgress.textContent = `${completedCount}/${tasks.length} Tasks`;
  }

  function addTask(text) {
    const newTask = {
      id: Date.now().toString(),
      text: text,
      completed: false
    };

    tasks.push(newTask);
    saveTasks();
    renderTasks();
  }

  function toggleTaskComplete(id) {
    tasks = tasks.map(t => {
      if (t.id === id) {
        return { ...t, completed: !t.completed };
      }
      return t;
    });
    saveTasks();
    renderTasks();
  }

  function deleteTask(id) {
    tasks = tasks.filter(t => t.id !== id);
    saveTasks();
    renderTasks();
  }

  function saveTasks() {
    localStorage.setItem("tasks", JSON.stringify(tasks));
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

  // --- Event Listeners ---

  playBtn.addEventListener("click", () => {
    if (isRunning) {
      pauseTimer();
    } else {
      startTimer();
    }
  });

  resetBtn.addEventListener("click", resetTimer);
  skipBtn.addEventListener("click", skipMode);

  modeBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const mode = e.target.getAttribute("data-mode");
      switchMode(mode);
    });
  });

  // Task form submission
  taskForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = taskInput.value.trim();
    if (text) {
      addTask(text);
      taskInput.value = "";
    }
  });

  // Handle click on list to toggle complete or delete
  taskList.addEventListener("click", (e) => {
    const taskItem = e.target.closest(".task-item");
    if (!taskItem) return;

    const id = taskItem.getAttribute("data-id");

    // Check if delete button clicked
    if (e.target.closest(".delete-task-btn")) {
      deleteTask(id);
    } 
    // Check if checkbox or left side clicked to toggle completed
    else if (e.target.closest(".task-left") || e.target.closest(".checkbox-custom")) {
      toggleTaskComplete(id);
    }
  });

  // Audio test button
  testAudioBtn.addEventListener("click", playAlertSound);

  // Load and save sound choice
  const savedSound = localStorage.getItem("selectedSound") || "zen";
  soundSelect.value = savedSound;
  
  soundSelect.addEventListener("change", (e) => {
    localStorage.setItem("selectedSound", e.target.value);
  });

  // --- Theme Swapper ---
  const themeDots = document.querySelectorAll(".theme-dot");
  
  // Load saved theme from localStorage, defaulting to 'nordic'
  const savedTheme = localStorage.getItem("selectedTheme") || "nordic";
  applyTheme(savedTheme);

  themeDots.forEach((dot) => {
    dot.addEventListener("click", (e) => {
      const selected = e.target.getAttribute("data-theme");
      applyTheme(selected);
    });
  });

  function applyTheme(theme) {
    // Remove existing themes
    document.body.classList.remove(
      "theme-midnight", 
      "theme-forest", 
      "theme-autumn", 
      "theme-ocean", 
      "theme-nordic",
      "theme-nebula",
      "theme-sunset",
      "theme-aurora"
    );
    
    // Apply selected theme
    document.body.classList.add(`theme-${theme}`);
    localStorage.setItem("selectedTheme", theme);

    // Refresh accents based on new theme
    if (typeof currentMode !== 'undefined') {
      switchMode(currentMode);
    }

    // Update active dot in UI
    themeDots.forEach((dot) => {
      if (dot.getAttribute("data-theme") === theme) {
        dot.classList.add("active");
      } else {
        dot.classList.remove("active");
      }
    });
  }

  // --- Mindful Breathing Space ---
  const focusSpace = document.querySelector(".focus-space");
  const breathingSpace = document.querySelector(".breathing-space");
  const spaceNavBtns = document.querySelectorAll(".space-nav-btn");
  
  const breathingCircle = document.getElementById("breathing-circle");
  const breathingPhase = document.getElementById("breathing-phase");
  const breathingTimerDisplay = document.getElementById("breathing-timer");
  const startBreathingBtn = document.getElementById("start-breathing-btn");
  const stopBreathingBtn = document.getElementById("stop-breathing-btn");
  const breathingHint = document.getElementById("breathing-hint");

  // Space toggle event listener
  spaceNavBtns.forEach((btn) => {
    btn.addEventListener("click", (e) => {
      const space = e.target.getAttribute("data-space");
      
      // Update active nav button
      spaceNavBtns.forEach((b) => b.classList.remove("active"));
      e.target.classList.add("active");
      
      if (space === "focus") {
        focusSpace.classList.remove("hidden");
        breathingSpace.classList.add("hidden");
        stopBreathing();
      } else {
        focusSpace.classList.add("hidden");
        breathingSpace.classList.remove("hidden");
        pauseTimer();
      }
    });
  });

  // 4-7-8 Breathing Engine State
  const BREATH_CONFIG = [
    { phase: "inhale", duration: 4, hint: "Breathe in through your nose quietly.", color: "var(--accent)" },
    { phase: "hold", duration: 7, hint: "Hold your breath.", color: "#ffffff" },
    { phase: "exhale", duration: 8, hint: "Exhale slowly through your mouth, releasing all tension.", color: "var(--accent)" }
  ];
  
  let breathTimeoutId = null;
  let breathCountdownId = null;
  let currentBreathPhaseIdx = 0;
  let breathTimeLeft = 0;
  let isBreathingRunning = false;

  // Synthesize soft calming tones for breath transitions
  function playBreathTone(pitch, duration) {
    try {
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator();
      const gainNode = audioCtx.createGain();
      
      osc.connect(gainNode);
      gainNode.connect(audioCtx.destination);
      
      osc.type = 'sine';
      osc.frequency.setValueAtTime(pitch, audioCtx.currentTime);
      
      // Soft fading envelope
      gainNode.gain.setValueAtTime(0, audioCtx.currentTime);
      gainNode.gain.linearRampToValueAtTime(0.08, audioCtx.currentTime + 0.15);
      gainNode.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + duration - 0.1);
      
      osc.start(audioCtx.currentTime);
      osc.stop(audioCtx.currentTime + duration);
    } catch(e) {
      console.warn("Audio Context blocked: ", e);
    }
  }

  function startBreathing() {
    if (isBreathingRunning) return;
    isBreathingRunning = true;
    
    startBreathingBtn.textContent = "Breathing...";
    startBreathingBtn.disabled = true;
    startBreathingBtn.style.opacity = "0.7";
    stopBreathingBtn.classList.remove("hidden");
    
    currentBreathPhaseIdx = 0;
    runBreathPhase();
  }
  
  function stopBreathing() {
    isBreathingRunning = false;
    
    // Clear timeouts and intervals
    if (breathTimeoutId) clearTimeout(breathTimeoutId);
    if (breathCountdownId) clearInterval(breathCountdownId);
    
    // Reset controls UI
    startBreathingBtn.textContent = "Start Breathing";
    startBreathingBtn.disabled = false;
    startBreathingBtn.style.opacity = "1";
    stopBreathingBtn.classList.add("hidden");
    
    // Reset visual circle scale
    breathingCircle.className = "breathing-circle";
    breathingCircle.style.transitionDuration = "1s";
    
    breathingPhase.textContent = "Ready";
    breathingTimerDisplay.textContent = "";
    breathingHint.textContent = "Click Start to begin your breathing cycle.";
  }
  
  function runBreathPhase() {
    if (!isBreathingRunning) return;
    
    const config = BREATH_CONFIG[currentBreathPhaseIdx];
    breathTimeLeft = config.duration;
    
    // Update UI elements
    breathingPhase.textContent = config.phase;
    breathingHint.textContent = config.hint;
    breathingTimerDisplay.textContent = breathTimeLeft;
    
    // Play phase audio tone
    if (config.phase === "inhale") {
      playBreathTone(329.63, 1.5); // E4
    } else if (config.phase === "hold") {
      playBreathTone(392.00, 1.5); // G4
    } else {
      playBreathTone(261.63, 2.0); // C4
    }
    
    // Apply visual classes and animate matching the durations
    breathingCircle.className = "breathing-circle";
    void breathingCircle.offsetWidth; // force reflow
    
    breathingCircle.style.transitionDuration = `${config.duration}s`;
    breathingCircle.classList.add(config.phase);
    
    // Clear countdown interval
    if (breathCountdownId) clearInterval(breathCountdownId);
    
    // Countdown counter
    breathCountdownId = setInterval(() => {
      if (!isBreathingRunning) {
        clearInterval(breathCountdownId);
        return;
      }
      
      breathTimeLeft--;
      if (breathTimeLeft > 0) {
        breathingTimerDisplay.textContent = breathTimeLeft;
      } else {
        clearInterval(breathCountdownId);
      }
    }, 1000);
    
    // Clear next phase timeout
    if (breathTimeoutId) clearTimeout(breathTimeoutId);
    
    // Schedule transition
    breathTimeoutId = setTimeout(() => {
      if (!isBreathingRunning) return;
      
      currentBreathPhaseIdx = (currentBreathPhaseIdx + 1) % BREATH_CONFIG.length;
      runBreathPhase();
    }, config.duration * 1000);
  }
  
  startBreathingBtn.addEventListener("click", startBreathing);
  stopBreathingBtn.addEventListener("click", stopBreathing);
});
