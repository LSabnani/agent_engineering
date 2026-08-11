# Class-02 Project Workspace

Welcome to the `class-02` project workspace. This folder aggregates four distinct web applications, services, and educational projects demonstrating frontend aesthetic design, backend service architecture, unit testing patterns, and state-of-the-art UI/UX integrations.

---

## Workspace Directory Structure

```text
class-02/
├── README.md               # Main workspace documentation (This file)
├── pomodoro timer/         # Glassmorphic focus timer & breathing space (Static Web App)
├── mock-tests/             # Isolated unit testing & mock verification (Python Service)
├── conference-website/     # GCP NextGen Summit Flask web app (Python Web App)
└── news-highlights/        # Daily curated news highlights pages (Static Web Pages)
```

---

## Project Outlines

### 1. ⏱️ ZenSpace - Aesthetic Pomodoro Timer
A minimal, premium, glassmorphic Pomodoro focus timer and task list designed for mindful productivity.

* **Technology**: Vanilla HTML5, CSS3, JavaScript (Web Audio API sound synthesis).
* **Key Features**:
  * **8 Curated Themes**: Toggle between Midnight Serene, Forest Mist, Warm Autumn, Ocean Deep, Nordic Lake (with animated light rays), Ethereal Nebula, Sunset Warmth, and Aurora Borealis.
  * **Mindful Breathing**: A dedicated 4-7-8 breathing spacer with smooth transitions (4s inhale circle expansion, 7s hold pulsation, 8s exhale circle contraction).
  * **Web Audio Synthesis**: Fully self-contained sound generator offering 4 testable alert tones: Zen Chime, Tibetan Singing Bowl, Minimal Digital, and Nature Forest Chirp.
  * **Persistence**: Synchronizes completed pomos and to-do intentions list to browser `localStorage`.
* **How to Run**:
  * Simply open `index.html` directly in your browser, or run a local server:
    ```bash
    python -m http.server 8081
    ```
    Visit **[http://localhost:8081](http://localhost:8081)**.

---

### 2. 🧪 Mock Tests - Order Checkout Service
An educational sandbox project demonstrating Python unit testing, Dependency Injection, and mocking using `unittest.mock`.

* **Technology**: Python 3.x, `unittest`, `unittest.mock`.
* **Key Features**:
  * **Order Service**: Models a realistic e-commerce workflow verifying empty carts, inventory limits, custom VIP discount calculations, and payment gateway charge APIs.
  * **Mock Assertions**: Swaps real database and credit card API calls with Mock objects to verify order outcomes and transactional safety (inventory decrement only triggers on successful charge).
  * **15-Test Suite**: Ensures 100% path coverage for exception raising, input validations, edge discount conditions, and mock call counts.
* **How to Run**:
  ```bash
  cd mock-tests
  python -m unittest test_order_service.py
  ```

---

### 3. 🌐 GCP NextGen Summit 2026 Website
A modern, dark-themed technical conference website highlighting schedule events and filtering talks.

* **Technology**: Python, Flask, HTML5, CSS3, JavaScript.
* **Key Features**:
  * **Dynamic Schedule Lookup**: Responsive client-side category filtering (AI, Security, Infra) and search queries.
  * **Glassmorphism Design**: Blur backdrop filters, modern gradients, and micro-hover animations.
* **How to Run**:
  ```bash
  cd conference-website
  python -m venv .venv
  # Activate (.venv\Scripts\activate on Windows or source .venv/bin/activate on Mac)
  pip install -r requirements.txt
  python app.py
  ```
  Visit **[http://localhost:5001](http://localhost:5001)**.

---

### 4. 📰 Daily News Highlights
A responsive grid layout displaying daily curated tech and stock market news.

* **Technology**: HTML5, CSS3.
* **Key Features**:
  * Curated sub-dashboards: Magnificent 7 tech summaries (`mag7.html`) and stock market updates (`stocks.html`).
  * Minimalist CSS variables layout.
* **How to Run**:
  * Open `index.html` directly inside the browser.
