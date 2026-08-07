# 🌌 AURA — Aesthetic Pomodoro & Mindfulness Space

AURA is a calm, premium Pomodoro timer and mindfulness dashboard designed to help you align your focus and soothe your mind. Built with vanilla HTML, CSS, and JavaScript, it features a glassmorphism interface, real-time synthesized ambient soundscapes using the Web Audio API, a mindful task list, and interactive breathing guides.

---

## ✨ Features

### ⏱️ Adaptive Pomodoro Timer
* **Multiple Modes**: Switch seamlessly between **Focus**, **Short Break**, **Long Break**, and a standalone **4-7-8 Breathing** exercise.
* **Progress Ring**: High-precision circular visual dial mapping the exact percentage of time remaining.
* **Flow Preferences**: Auto-start next sessions or configure guided breathing during breaks.

### 🌬️ Mindful Breathing Guide (4-7-8 Technique)
* Features a built-in guide for the popular 4-7-8 relaxing breath technique:
  1. **Inhale** quietly through your nose for **4 seconds**.
  2. **Hold** your breath for **7 seconds**.
  3. **Exhale** audibly through your mouth for **8 seconds**.
* Displays a pulsating breathing indicator synced with current phase instructions.

### 🎛️ Ambient Soundscapes (Synthesized via Web Audio API)
Unlike standard apps using large audio files, AURA synthesizes nature sounds on-the-fly using the **Web Audio API** for lightweight, endless loops:
* 🌧️ **Summer Rain**: Synthesized pink noise with random droplet impulses.
* 🌲 **Nature Forest**: Synthetic wind hums combined with generated bird chirps.
* 🌊 **Deep Ocean**: Periodic low-frequency wave swells.
* 🎹 **Cosmic Chords**: A multi-oscillator synthesizer drone creating rich, soothing chords.
* *Includes individual mute toggles and volume sliders.*

### 📝 Focus Intentions (Task Manager)
* Keep track of your mindfulness goals with a minimalist task manager.
* Set your active intention and see it highlighted at the bottom of the focus container.

### 🎨 Theme Customization
Choose from seven premium, fluid animated background mesh gradients:
* 🌲 **Misty Forest & Dawn** (Default)
* 🌅 **Sunset Amber**
* 🍃 **Emerald Mint**
* 🌌 **Midnight Cyberpunk**
* 🌑 **Dark Obsidian**
* ❄️ **Aurora Cyan**
* 🌸 **Rose Quartz**

### ⚙️ Extended Settings
* **Custom Durations**: Adjust Focus, Short Break, and Long Break lengths in minutes.
* **Notification Chimes**: Choose between a *Tibetan Singing Bowl*, *Cozy Velvet Bell*, *Gentle Digital Ping*, or silent transitions. Includes a sound testing option.
* **Local Statistics**: Keep track of your flows completed today and total focus time.

---

## 📂 File Structure

* `index.html`: Main interface markup and layout structures, optimized with SEO metadata.
* `style.css`: Premium glassmorphism design system, grid layout, animations, and custom theme properties.
* `app.js`: Application logic including the Web Audio synthesizer engines, timer state machine, task manager, and settings.

---

## 🚀 Getting Started

Simply open `index.html` in your modern web browser (Chrome, Edge, Safari, or Firefox).

1. Write a focus intention in the **Focus Intentions** panel.
2. Select your desired time interval or start the **Focus** timer.
3. Use the **Ambient Space** mixer to blend sounds together and find your optimal focus atmosphere.
4. Customize your experience in the **Settings** menu.
