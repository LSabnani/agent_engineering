from flask import Flask, render_template, request, jsonify
import config
from pipeline.state import create_initial_state
from pipeline.agents import SequentialPipeline
from pipeline.logger import logger

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/plan", methods=["POST"])
def plan_trip():
    data = request.get_json() or {}
    destination = data.get("destination", "Kyoto, Japan")
    days = int(data.get("days", 5))
    budget = float(data.get("budget", 2000.0))
    interests = data.get("interests", ["Culture", "Food"])

    # Clear logs for new session
    logger.clear()

    # Create state and execute pipeline
    state = create_initial_state(destination, budget, days, interests)
    pipeline = SequentialPipeline()
    final_state = pipeline.run(state)

    return jsonify(final_state)

@app.route("/api/events", methods=["GET"])
def get_events():
    events = logger.get_events()
    return jsonify(events)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=True)
