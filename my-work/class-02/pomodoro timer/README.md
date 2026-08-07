# ZenSpace - Aesthetic Pomodoro Timer

A calm, aesthetic, and minimal glassmorphic Pomodoro timer and productivity application.

## Key Features

- **Pomo Cycles**: Switch between Focus (25m), Short Break (5m), and Long Break (15m).
- **Progress Tracking**: Features a smooth SVG circular progress ring that counts down visually.
- **Intention List**: Add, complete, and delete focus items to organize your sessions. Progress counts are tracked automatically.
- **Zen Chime Alert**: Plays a synthesized, beautiful chime upon completion using the browser's native **Web Audio API** (completely self-contained, no external audio downloads required).
- **Persistent State**: Completed cycles and intentions list are automatically synced and persisted via `localStorage`.

## Setup and Running

1. Simply open `index.html` directly in your browser.
2. Alternatively, serve it locally using Python from this directory:
   ```bash
   python -m http.server 8081
   ```
   Then open **[http://localhost:8081](http://localhost:8081)** in your browser.
