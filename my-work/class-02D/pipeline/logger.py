import json
import os
import time
from typing import Dict, Any, List

EVENT_LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "artifacts", "events.json")

class EventLogger:
    def __init__(self, log_file: str = EVENT_LOG_PATH):
        self.log_file = log_file
        self.ensure_dir()
        self.events: List[Dict[str, Any]] = []
        self.clear()

    def ensure_dir(self):
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)

    def clear(self):
        self.events = []
        self.ensure_dir()
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

    def log(self, agent_name: str, stage: str, event_type: str, details: Dict[str, Any]):
        entry = {
            "timestamp": time.time(),
            "formatted_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "agent": agent_name,
            "stage": stage,
            "event_type": event_type,
            "details": details
        }
        self.events.append(entry)
        self.save()
        return entry

    def save(self):
        self.ensure_dir()
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=2)

    def get_events(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return self.events
        return self.events

logger = EventLogger()
