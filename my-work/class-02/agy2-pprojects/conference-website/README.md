# GCP NextGen Summit 2026 Website

A modern, glassmorphic technical conference informational website built with Python/Flask, featuring dynamic schedule searching and filtering of Google Cloud talks.

## Project Structure

```text
conference-website/
├── app.py                # Flask server storing schedule data and routing
├── requirements.txt      # Python dependencies
├── README.md             # Setup guide
├── templates/
│   └── index.html        # Main HTML page template
└── static/
    ├── styles.css        # Premium dark glassmorphic CSS rules
    └── main.js           # Client-side search and category filtering
```

## Setup Instructions

### 1. Initialize Virtual Environment

From this directory, run:

```bash
python -m venv .venv
```

Activate the environment:

- **Windows:**
  ```powershell
  .venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 2. Install Dependencies

Install the requirements using pip:

```bash
pip install -r requirements.txt
```

### 3. Run the Server

Start the Flask development server:

```bash
python app.py
```

The application will launch on **[http://localhost:5001](http://localhost:5001)**.

## How to Customize

- **Change Date/Location**: Edit `CONFERENCE_INFO` in `app.py`.
- **Add/Modify Talks**: Edit the `SCHEDULE` list in `app.py`. Each talk supports categories (like `Cloud Infrastructure`, `AI & Data`, `App Development`, `Security & Governance`) and speaker details (with first name, last name, and LinkedIn URL).
