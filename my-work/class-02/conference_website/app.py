import os
from flask import Flask, jsonify, render_template

app = Flask(__name__)

# Mock Data for Google Cloud Conference
CONFERENCE_INFO = {
    "title": "GCP Next-Gen Summit 2026",
    "date": "October 15, 2026",
    "location": "Google Community Space, San Francisco, CA & Virtual",
    "timezone": "PDT"
}

# Speakers Data
SPEAKERS = {
    "spk1": {
        "first_name": "Priya",
        "last_name": "Sharma",
        "linkedin_url": "https://www.linkedin.com/in/priyasharma-gcp"
    },
    "spk2": {
        "first_name": "Marcus",
        "last_name": "Aurelius",
        "linkedin_url": "https://www.linkedin.com/in/marcus-k8s"
    },
    "spk3": {
        "first_name": "Elena",
        "last_name": "Rostova",
        "linkedin_url": "https://www.linkedin.com/in/elena-serverless"
    },
    "spk4": {
        "first_name": "Amit",
        "last_name": "Patel",
        "linkedin_url": "https://www.linkedin.com/in/amit-patel-vertexai"
    },
    "spk5": {
        "first_name": "Jordan",
        "last_name": "Vance",
        "linkedin_url": "https://www.linkedin.com/in/jordan-vance-data"
    },
    "spk6": {
        "first_name": "Chen",
        "last_name": "Wei",
        "linkedin_url": "https://www.linkedin.com/in/chen-wei-dataflow"
    },
    "spk7": {
        "first_name": "Sarah",
        "last_name": "Jenkins",
        "linkedin_url": "https://www.linkedin.com/in/sarah-jenkins-iam"
    },
    "spk8": {
        "first_name": "David",
        "last_name": "Miller",
        "linkedin_url": "https://www.linkedin.com/in/david-miller-spanner"
    }
}

# Talks Data (8 talks total + 1 Lunch break)
TALKS = [
    {
        "id": "TALK-01",
        "title": "Keynote: The Horizon of Generative AI & Google Cloud Core Services",
        "speakers": [SPEAKERS["spk1"], SPEAKERS["spk4"]],
        "category": "Data & Artificial Intelligence",
        "description": "An inspiring look into how Google Cloud is integration-testing Gemini models into core infrastructure, paving the way for next-generation developer productivity and system automation.",
        "start_time": "09:00 AM",
        "end_time": "09:45 AM",
        "type": "talk"
    },
    {
        "id": "TALK-02",
        "title": "Scaling to Millions: GKE Autopilot Best Practices",
        "speakers": [SPEAKERS["spk2"]],
        "category": "Infrastructure & Architecture",
        "description": "Learn the underlying mechanisms of GKE Autopilot's resource provisioning, scaling speed, cost optimization strategies, and multi-tenant security structures.",
        "start_time": "09:45 AM",
        "end_time": "10:30 AM",
        "type": "talk"
    },
    {
        "id": "TALK-03",
        "title": "Serverless Deep Dive: Building Resilient Microservices with Cloud Run",
        "speakers": [SPEAKERS["spk3"]],
        "category": "Infrastructure & Architecture",
        "description": "Explore custom domains, ingress controls, global load balancing, and sidecar support on Google Cloud Run to deploy secure and highly scalable containerized apps.",
        "start_time": "10:30 AM",
        "end_time": "11:15 AM",
        "type": "talk"
    },
    {
        "id": "TALK-04",
        "title": "Vertex AI Agent Builder: Constructing Autonomous Enterprise Agents",
        "speakers": [SPEAKERS["spk4"]],
        "category": "Data & Artificial Intelligence",
        "description": "A practical guide to building conversational AI agents that use Retrieval-Augmented Generation (RAG) and tool-calling on live enterprise data sources.",
        "start_time": "11:15 AM",
        "end_time": "12:00 PM",
        "type": "talk"
    },
    {
        "id": "LUNCH-01",
        "title": "Networking Lunch Break",
        "speakers": [],
        "category": "General",
        "description": "Enjoy a curated lunch buffet, meet with Google developers and partners, and explore the interactive sandbox demo booths.",
        "start_time": "12:00 PM",
        "end_time": "01:00 PM",
        "type": "break"
    },
    {
        "id": "TALK-05",
        "title": "Modern Data Warehousing: SQL and Beyond in BigQuery",
        "speakers": [SPEAKERS["spk5"]],
        "category": "Data & Artificial Intelligence",
        "description": "Unlocking real-time analytics and predictive ML models directly inside BigQuery using standard SQL queries and BigQuery ML integration.",
        "start_time": "01:00 PM",
        "end_time": "01:45 PM",
        "type": "talk"
    },
    {
        "id": "TALK-06",
        "title": "Real-Time Event Processing: Apache Beam on Dataflow",
        "speakers": [SPEAKERS["spk6"], SPEAKERS["spk5"]],
        "category": "Data & Artificial Intelligence",
        "description": "Constructing zero-loss, auto-scaling real-time streaming pipelines with Cloud Pub/Sub and Cloud Dataflow for dynamic web activity monitoring.",
        "start_time": "01:45 PM",
        "end_time": "02:30 PM",
        "type": "talk"
    },
    {
        "id": "TALK-07",
        "title": "Zero Trust Architectures using GCP IAM and BeyondCorp Enterprise",
        "speakers": [SPEAKERS["spk7"]],
        "category": "Infrastructure & Architecture",
        "description": "Implementing least-privilege principles, context-aware access control rules, and workload identity federation to secure complex cloud workloads.",
        "start_time": "02:30 PM",
        "end_time": "03:15 PM",
        "type": "talk"
    },
    {
        "id": "TALK-08",
        "title": "Global Databases: Deploying High-Availability Systems with Cloud Spanner",
        "speakers": [SPEAKERS["spk8"], SPEAKERS["spk1"]],
        "category": "Infrastructure & Architecture",
        "description": "Under the hood of Google Cloud Spanner's TrueTime API, showing how it guarantees strong consistency globally while maintaining 99.999% availability.",
        "start_time": "03:15 PM",
        "end_time": "04:00 PM",
        "type": "talk"
    },
    {
        "id": "TALK-09",
        "title": "Evening talk",
        "speakers": [SPEAKERS["spk2"], SPEAKERS["spk3"]],
        "category": "Infrastructure & Architecture",
        "description": "An open discussion and panel on the future of GCP architectures, GKE, and serverless integration, concluding the main summit tracks.",
        "start_time": "04:00 PM",
        "end_time": "04:45 PM",
        "type": "talk"
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/schedule')
def get_schedule():
    return jsonify({
        "conference": CONFERENCE_INFO,
        "schedule": TALKS
    })

if __name__ == '__main__':
    # Run the Flask app on localhost, port 5001 to avoid port collisions
    app.run(host='127.0.0.1', port=5001, debug=True)
