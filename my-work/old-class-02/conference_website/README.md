# GCP Next-Gen Summit 2026 - Conference Website

A high-fidelity, single-page application (SPA) informational website for a 1-day technical conference on Google Cloud Technologies. The application is built using a Python Flask back-end and a responsive, premium HTML5/CSS3/Vanilla JS front-end.

---

## Features
- **Hero & Countdown**: Features an interactive countdown timer calculated dynamically in JavaScript based on the event timezone.
- **Dynamic 1-Day Schedule**: Chronologically maps out 8 expert-level GCP talks and a 60-minute networking lunch break.
- **Search Functionality**: Instantly filters the schedule as the user types, matching talk titles, descriptions, and speaker names.
- **Category Filter Chips**: Group and switch between the core conference tracks ("All", "Infrastructure & Architecture", and "Data & AI") with a single click.
- **Interactive Bookmarking**: Bookmark favorite talks to build a custom schedule, persisted locally inside the browser's `localStorage`.
- **Featured Speakers Gallery**: Showcases profile details, titles, initials, and direct LinkedIn profile links for all presenting speakers.
- **Responsive Web Design**: Fluid layout optimized for desktops, tablets, and mobile phone screens.

---

## File Structure
```text
Conference_Website/
│
├── app.py                # Flask server application serving routes & JSON APIs
├── requirements.txt      # Python dependencies (Flask)
├── run.ps1               # PowerShell setup & launch script
├── README.md             # Setup, running, and developer extension manual
│
├── templates/
│   └── index.html        # Main HTML layout using Semantic elements
│
└── static/
    ├── css/
    │   └── style.css     # Glassmorphic, modern CSS animations and styles
    ├── js/
    │   └── main.js       # App state, search/filter logic, countdown timer, and local storage bookmarks
    └── images/
        └── gcp_summit_banner.png # Generated header banner graphic
```

---

## Tech Stack
- **Server Side**: Python 3.x, Flask (v3.0.3)
- **Client Side**: Semantic HTML5, Vanilla CSS3 (Custom design, variables, and blur animations), Vanilla ES6 JavaScript

---

## Quick Setup & Start

### Option 1: Using PowerShell (Recommended)
We have provided a launcher script that handles setting up a Python virtual environment, installing dependencies, and running the server:
1. Open PowerShell in the project directory.
2. Run the script:
   ```powershell
   ./run.ps1
   ```
3. Open your browser and navigate to `http://127.0.0.1:5000`.

### Option 2: Manual Setup (Cross-Platform)
If you prefer setting it up manually:
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
2. Activate the virtual environment:
   - **Windows (CMD/PowerShell)**:
     ```powershell
     .venv\Scripts\activate
     ```
   - **Mac/Linux**:
     ```bash
     source .venv/bin/activate
     ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your web browser.

---

## Developer Guide: Customizing & Extending

### Adding or Modifying Talks
All mock talks are managed in-memory on the Flask server. To update a talk, edit the `TALKS` list in [app.py](file:///c:/Users/Lalit.MSI/Documents/Education/Agentic_Eng/agy2_pprojects/Conference_Website/app.py):
```python
{
    "id": "TALK-09",
    "title": "Your Awesome GCP Talk",
    "speakers": [SPEAKERS["spk1"]],
    "category": "Data & Artificial Intelligence", # Matches front-end filters
    "description": "Enter the description here...",
    "start_time": "04:00 PM",
    "end_time": "04:45 PM",
    "type": "talk" # Or "break"
}
```

### Adding or Modifying Speakers
To change speaker details, edit the `SPEAKERS` dictionary in [app.py](file:///c:/Users/Lalit.MSI/Documents/Education/Agentic_Eng/agy2_pprojects/Conference_Website/app.py):
```python
"spkX": {
    "first_name": "Jane",
    "last_name": "Doe",
    "linkedin_url": "https://www.linkedin.com/in/janedoe"
}
```

### Changing Conference Information (Date, Location)
Update the `CONFERENCE_INFO` dictionary in [app.py](file:///c:/Users/Lalit.MSI/Documents/Education/Agentic_Eng/agy2_pprojects/Conference_Website/app.py):
```python
CONFERENCE_INFO = {
    "title": "GCP Next-Gen Summit 2026",
    "date": "October 15, 2026",
    "location": "Google Community Space, San Francisco, CA & Virtual",
    "timezone": "PDT"
}
```

### Adjusting UI & Visual Styling
- To update colors, fonts, or responsive behaviors, adjust the CSS variables and classes inside [style.css](file:///c:/Users/Lalit.MSI/Documents/Education/Agentic_Eng/agy2_pprojects/Conference_Website/static/css/style.css).
- To tweak frontend interactions, search sensitivity, or timer settings, adapt [main.js](file:///c:/Users/Lalit.MSI/Documents/Education/Agentic_Eng/agy2_pprojects/Conference_Website/static/js/main.js).
