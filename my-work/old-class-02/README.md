# Class 2 Assignment

## Student Information
- **Name**: Lalit Sabnani  
- **GitHub Username**: LSabnani
- **Date Completed**: 8/6/2026

## Workspace Setup
This workspace folder (`my-work/class-02/`) contains four core sub-projects:

1. **`conference_website`**
   - High-fidelity single-page Flask application representing a 1-day GCP Next-Gen Summit.
   - Includes real-time search, category track filter chips, dynamic countdown timer, and schedule bookmarking persisted in `localStorage`.

2. **`pomodoro` (Aura Aesthetic Pomodoro & Mindfulness Space)**
   - Premium mindfulness dashboard featuring glassmorphism design.
   - Includes auto-timed Pomodoro states, a 4-7-8 breathing practice guide, and real-time synthesized ambient sounds (Summer Rain, Nature Forest, Deep Ocean, Cosmic Chords).

3. **`mock_test`**
   - Unit tests covering the online order service checkout lifecycle.
   - Asserts price discount logic, stock validation boundaries, inventory updates, and credit card payments.

4. **`news_highlights`**
   - Premium dashboard aggregating news headers.
   - Expanded with real-time **Financial Highlights** including the Magnificent 7 performance matrix and day's top winners/losers from Finviz.

---

## What I Learned
- **Web Audio API Sound Synthesis**: Learned to generate nature sounds on-the-fly inside the browser using pink noise, multi-oscillator synthesizer drones, and periodic swells instead of loading static audio assets.
- **BeautifulSoup Financial Scraping**: Built Python scrapers to query Finviz screener URLs, parse HTML data tables, and extract structured metrics like stock ticker, company, change, volume, and sector.
- **Robust DOM Extraction**: Dealt with complex and crowded markup layouts (e.g. parsing clean stock symbols when links contain overlapping logo span tags).
- **Refining Unit Tests**: Wrote comprehensive unit tests using Python's testing framework to mock third-party services and validate calculations.

---

## Challenges
- **Playwright Driver Failure**: Playwright failed to download/install due to Playwright host driver ZIP version issues in the browser subagent. Successfully pivoted to BeautifulSoup scraping via Python request sessions to bypass the dependency block.
- **Overlapping Markup parsing**: Extracted tickers from Finviz had doubled letters (like `AAAPL` for `AAPL`) due to logo span text concatenation. Resolved by targeting the specific class attributes and anchors (`class="tab-link"`).
