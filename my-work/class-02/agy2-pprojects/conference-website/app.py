from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Conference Metadata
CONFERENCE_INFO = {
    "title": "GCP NextGen Summit 2026",
    "description": "A 1-Day Technical Deep Dive into Google Cloud Technologies",
    "date": "Friday, October 9, 2026",
    "location": "Google Community Space, San Francisco, CA & Virtual",
    "timezone": "PDT"
}

# Speakers list (reused across talks)
SPEAKERS = {
    "sarah_devlin": {
        "first_name": "Sarah",
        "last_name": "Devlin",
        "linkedin": "https://www.linkedin.com/in/sarah-devlin-demo"
    },
    "rajesh_kumar": {
        "first_name": "Rajesh",
        "last_name": "Kumar",
        "linkedin": "https://www.linkedin.com/in/rajesh-kumar-demo"
    },
    "amy_chen": {
        "first_name": "Amy",
        "last_name": "Chen",
        "linkedin": "https://www.linkedin.com/in/amy-chen-demo"
    },
    "marcus_vance": {
        "first_name": "Marcus",
        "last_name": "Vance",
        "linkedin": "https://www.linkedin.com/in/marcus-vance-demo"
    },
    "elena_rostova": {
        "first_name": "Elena",
        "last_name": "Rostova",
        "linkedin": "https://www.linkedin.com/in/elena-rostova-demo"
    },
    "david_miller": {
        "first_name": "David",
        "last_name": "Miller",
        "linkedin": "https://www.linkedin.com/in/david-miller-demo"
    },
    "chloe_dupont": {
        "first_name": "Chloe",
        "last_name": "DuPont",
        "linkedin": "https://www.linkedin.com/in/chloe-dupont-demo"
    },
    "simon_peter": {
        "first_name": "Simon",
        "last_name": "Peter",
        "linkedin": "https://www.linkedin.com/in/simon-peter-demo"
    },
    "jack_warner": {
        "first_name": "Jack",
        "last_name": "Warner",
        "linkedin": "https://www.linkedin.com/in/jack-warner-demo"
    },
    "luka_modric": {
        "first_name": "Luka",
        "last_name": "Modric",
        "linkedin": "https://www.linkedin.com/in/luka-modric-demo"
    }
}

# Complete event schedule including 10 talks and 60 minutes lunch break
SCHEDULE = [
    {
        "id": "talk-01",
        "type": "talk",
        "time": "09:00 AM - 09:40 AM",
        "title": "Keynote: Google Cloud in 2026 & Beyond",
        "description": "A visionary overview of GKE ecosystem updates, serverless scaling, and advanced machine learning integrations shaping enterprise system designs.",
        "categories": ["Cloud Infrastructure"],
        "speakers": [SPEAKERS["sarah_devlin"]]
    },
    {
        "id": "talk-02",
        "type": "talk",
        "time": "09:40 AM - 10:20 AM",
        "title": "Vertex AI: Scaling GenAI and Agentic Applications",
        "description": "A technical deep-dive into building and orchestrating enterprise-ready AI agents using Vertex AI, Gemini models, and real-time Vector Search.",
        "categories": ["AI & Data"],
        "speakers": [SPEAKERS["rajesh_kumar"], SPEAKERS["amy_chen"]]
    },
    {
        "id": "talk-03",
        "type": "talk",
        "time": "10:20 AM - 11:00 AM",
        "title": "GKE Autopilot: Advanced Scaling & Cloud Operations",
        "description": "How to optimize multi-cluster environments, setup robust scheduling controls, and monitor massive container deployments cost-effectively.",
        "categories": ["Cloud Infrastructure"],
        "speakers": [SPEAKERS["marcus_vance"]]
    },
    {
        "id": "talk-04",
        "type": "talk",
        "time": "11:00 AM - 11:40 AM",
        "title": "Cloud Run: Microservices Redefined",
        "description": "An interactive session demonstrating how developers can deploy containerized APIs and web applications at near-zero idle cost with instant auto-scaling.",
        "categories": ["App Development"],
        "speakers": [SPEAKERS["elena_rostova"]]
    },
    {
        "id": "talk-05",
        "type": "talk",
        "time": "11:40 AM - 12:20 PM",
        "title": "Google Cloud Spanner: Globally Distributed SQL at Scale",
        "description": "Understanding how Cloud Spanner provides global scale, infinite horizontal compute write-capacity, and strong ACID transaction consistency.",
        "categories": ["AI & Data"],
        "speakers": [SPEAKERS["david_miller"]]
    },
    {
        "id": "lunch-break",
        "type": "break",
        "time": "12:20 PM - 01:20 PM",
        "title": "Lunch Break & Networking",
        "description": "60 minutes to refuel, connect with other delegates, and visit the Google Cloud Solutions Sandbox.",
        "categories": [],
        "speakers": []
    },
    {
        "id": "talk-06",
        "type": "talk",
        "time": "01:20 PM - 02:00 PM",
        "title": "BigQuery: Real-time Analytics & Data Clean Rooms",
        "description": "Querying petabytes in seconds, sharing secure datasets with clean rooms, and building sql-based machine learning models inside BigQuery.",
        "categories": ["AI & Data"],
        "speakers": [SPEAKERS["rajesh_kumar"]]
    },
    {
        "id": "talk-07",
        "type": "talk",
        "time": "02:00 PM - 02:40 PM",
        "title": "Securing Cloud Workloads with SCC Enterprise",
        "description": "Leveraging Security Command Center Enterprise to proactively identify posture risks, detect active runtime threats, and auto-remediate vulnerabilities.",
        "categories": ["Security & Governance"],
        "speakers": [SPEAKERS["chloe_dupont"]]
    },
    {
        "id": "talk-08",
        "type": "talk",
        "time": "02:40 PM - 03:20 PM",
        "title": "AlloyDB: Postgres-Compatible Enterprise DB Performance",
        "description": "Exploring AlloyDB's analytical engine, memory-tier caching systems, and benchmarking performance against self-managed databases.",
        "categories": ["AI & Data"],
        "speakers": [SPEAKERS["simon_peter"]]
    },
    {
        "id": "talk-09",
        "type": "talk",
        "time": "03:20 PM - 04:00 PM",
        "title": "FinOps: Cloud Cost Minimization Strategies",
        "description": "Practical patterns and practices for cost visualization, sizing workloads, and automating committed-use discount optimizations.",
        "categories": ["Security & Governance"],
        "speakers": [SPEAKERS["sarah_devlin"], SPEAKERS["jack_warner"]]
    },
    {
        "id": "talk-10",
        "type": "talk",
        "time": "04:00 PM - 04:40 PM",
        "title": "Apigee: Managing API Ecosystems at Enterprise Scale",
        "description": "Securing, monitoring, and monetizing transactional API endpoints across hybrid and multi-cloud environments using Apigee.",
        "categories": ["App Development"],
        "speakers": [SPEAKERS["luka_modric"]]
    }
]


@app.route("/")
def home():
    """Render the conference homepage."""
    return render_template("index.html", config=CONFERENCE_INFO, schedule=SCHEDULE)


@app.route("/api/schedule")
def get_schedule():
    """Return schedule as JSON for any advanced API client integrations."""
    return jsonify({
        "info": CONFERENCE_INFO,
        "schedule": SCHEDULE
    })


if __name__ == "__main__":
    # Start the server on port 5001 (centralized config)
    app.run(host="0.0.0.0", port=5001, debug=True)
