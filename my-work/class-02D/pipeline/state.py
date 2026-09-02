from typing import Dict, Any, List

def create_initial_state(destination: str, budget: float, days: int, interests: List[str]) -> Dict[str, Any]:
    """Initializes the centralized state dictionary for the multi-agent pipeline."""
    return {
        "user_input": {
            "destination": destination,
            "budget": float(budget),
            "days": int(days),
            "interests": interests if isinstance(interests, list) else [interests]
        },
        "raw_research": {
            "flights": [],
            "hotels": [],
            "activities": []
        },
        "current_itinerary": {
            "total_estimated_cost": 0.0,
            "schedule": [],
            "selected_flight": None,
            "selected_hotel": None
        },
        "critic_feedback": "",
        "budget_approved": False,
        "iteration_count": 0
    }
