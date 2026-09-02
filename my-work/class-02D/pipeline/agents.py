import json
import os
import concurrent.futures
from typing import Dict, Any, List
import config
from pipeline.logger import logger

# Try importing google.genai or google.generativeai if available
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class FlightResearcher:
    def execute(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        dest = state["user_input"]["destination"]
        logger.log("FlightResearcher", "Discovery Phase", "RESEARCH_STARTED", {"destination": dest})
        
        # Synthetic / Gemini-enhanced realistic flight options
        flights = [
            {
                "airline": "Express Airways",
                "flight_number": "EX-402",
                "route": f"Origin -> {dest}",
                "round_trip_cost": 450.0,
                "tier": "economy",
                "duration": "8h 15m"
            },
            {
                "airline": "Skyline Deluxe",
                "flight_number": "SD-109",
                "route": f"Origin -> {dest}",
                "round_trip_cost": 850.0,
                "tier": "premium_economy",
                "duration": "7h 45m"
            },
            {
                "airline": "BudgetJet",
                "flight_number": "BJ-88",
                "route": f"Origin -> {dest}",
                "round_trip_cost": 280.0,
                "tier": "budget",
                "duration": "9h 30m"
            }
        ]
        logger.log("FlightResearcher", "Discovery Phase", "RESEARCH_COMPLETED", {"options_found": len(flights)})
        return flights

class HotelResearcher:
    def execute(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        dest = state["user_input"]["destination"]
        logger.log("HotelResearcher", "Discovery Phase", "RESEARCH_STARTED", {"destination": dest})
        
        hotels = [
            {
                "name": f"Grand Central Hotel {dest.split(',')[0]}",
                "nightly_rate": 180.0,
                "tier": "mid-range",
                "rating": 4.6,
                "amenities": ["Wi-Fi", "Breakfast", "Central Location"]
            },
            {
                "name": f"Serenity Boutique Inn {dest.split(',')[0]}",
                "nightly_rate": 260.0,
                "tier": "luxury",
                "rating": 4.9,
                "amenities": ["Spa", "Rooftop Pool", "Gourmet Dining"]
            },
            {
                "name": f"Backpackers Heritage Hostel {dest.split(',')[0]}",
                "nightly_rate": 65.0,
                "tier": "budget",
                "rating": 4.2,
                "amenities": ["Wi-Fi", "Shared Kitchen", "Social Lounge"]
            }
        ]
        logger.log("HotelResearcher", "Discovery Phase", "RESEARCH_COMPLETED", {"options_found": len(hotels)})
        return hotels

class ActivityPlanner:
    def execute(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        dest = state["user_input"]["destination"]
        interests = state["user_input"]["interests"]
        logger.log("ActivityPlanner", "Discovery Phase", "RESEARCH_STARTED", {"destination": dest, "interests": interests})
        
        city = dest.split(',')[0].strip()
        activities = [
            {
                "title": f"Historic {city} Heritage Walk & Temple Tour",
                "category": "culture",
                "neighborhood": "Old Town",
                "estimated_cost": 35.0,
                "description": "Guided walking tour of ancient monuments, shrines, and traditional architecture."
            },
            {
                "title": f"Local {city} Food Market & Street Eat Crawl",
                "category": "food",
                "neighborhood": "Central Market",
                "estimated_cost": 45.0,
                "description": "Sample iconic local street delicacies, tea tasting, and artisan sweets."
            },
            {
                "title": f"{city} Panoramic Viewpoint & Botanical Gardens",
                "category": "sightseeing",
                "neighborhood": "North Hills",
                "estimated_cost": 15.0,
                "description": "Breathtaking scenic overlook with lush natural gardens and photographic spots."
            },
            {
                "title": f"Traditional {city} Craft & Pottery Workshop",
                "category": "culture",
                "neighborhood": "Artisan Quarter",
                "estimated_cost": 60.0,
                "description": "Hands-on masterclass creating authentic local craft items."
            },
            {
                "title": f"{city} River Cruise & Sunset Experience",
                "category": "relaxation",
                "neighborhood": "Riverside",
                "estimated_cost": 50.0,
                "description": "Relaxing evening boat cruise with live local acoustic music."
            },
            {
                "title": f"Self-Guided Scenic District Explorer",
                "category": "free",
                "neighborhood": "Old Town",
                "estimated_cost": 0.0,
                "description": "Wander charm-filled alleyways, scenic parks, and open photo spots."
            }
        ]
        logger.log("ActivityPlanner", "Discovery Phase", "RESEARCH_COMPLETED", {"options_found": len(activities)})
        return activities

class ParallelAgent:
    def __init__(self):
        self.flight_researcher = FlightResearcher()
        self.hotel_researcher = HotelResearcher()
        self.activity_planner = ActivityPlanner()

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.log("ParallelAgent", "Discovery Phase", "PARALLEL_EXECUTION_START", {})
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_flights = executor.submit(self.flight_researcher.execute, state)
            future_hotels = executor.submit(self.hotel_researcher.execute, state)
            future_activities = executor.submit(self.activity_planner.execute, state)

            state["raw_research"]["flights"] = future_flights.result()
            state["raw_research"]["hotels"] = future_hotels.result()
            state["raw_research"]["activities"] = future_activities.result()

        logger.log("ParallelAgent", "Discovery Phase", "PARALLEL_EXECUTION_END", {
            "flights_count": len(state["raw_research"]["flights"]),
            "hotels_count": len(state["raw_research"]["hotels"]),
            "activities_count": len(state["raw_research"]["activities"])
        })
        return state

class Scheduler:
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        iteration = state.get("iteration_count", 0) + 1
        state["iteration_count"] = iteration
        feedback = state.get("critic_feedback", "")
        
        logger.log("Scheduler", "Optimization Room", "SCHEDULING_START", {
            "iteration": iteration,
            "prior_feedback": feedback
        })
        
        user_input = state["user_input"]
        budget = user_input["budget"]
        days = user_input["days"]
        raw = state["raw_research"]
        
        # Selection logic based on feedback / budget sensitivity
        flights = raw.get("flights", [])
        hotels = raw.get("hotels", [])
        activities = raw.get("activities", [])
        
        # If over budget feedback received in prior loop, select cheaper options
        if "over budget" in feedback.lower() or iteration > 1:
            selected_flight = min(flights, key=lambda f: f["round_trip_cost"]) if flights else None
            selected_hotel = min(hotels, key=lambda h: h["nightly_rate"]) if hotels else None
        else:
            # Pick mid-range default
            selected_flight = flights[0] if flights else None
            selected_hotel = hotels[0] if hotels else None
            
        flight_cost = selected_flight["round_trip_cost"] if selected_flight else 0.0
        hotel_cost = (selected_hotel["nightly_rate"] * days) if selected_hotel else 0.0

        # Construct daily schedule using geographic clustering
        schedule = []
        neighborhoods = ["Old Town", "Central Market", "North Hills", "Artisan Quarter", "Riverside"]
        
        for d in range(1, days + 1):
            neigh = neighborhoods[(d - 1) % len(neighborhoods)]
            # Filter activities matching neighborhood or low cost if iteration > 1
            day_acts = [a for a in activities if a.get("neighborhood") == neigh]
            if not day_acts:
                day_acts = activities[:2]
                
            if "over budget" in feedback.lower() and iteration > 1:
                # Include lower cost activities
                day_acts = sorted(day_acts, key=lambda x: x["estimated_cost"])[:2]
            else:
                day_acts = day_acts[:2]
                
            events = [
                {
                    "time": "09:00 AM",
                    "title": day_acts[0]["title"] if day_acts else "Morning Landmark Walk",
                    "category": day_acts[0]["category"] if day_acts else "culture",
                    "estimated_cost": day_acts[0]["estimated_cost"] if day_acts else 0.0,
                    "neighborhood": neigh,
                    "description": day_acts[0]["description"] if day_acts else "Explore morning sights."
                },
                {
                    "time": "01:00 PM",
                    "title": f"Lunch in {neigh} District",
                    "category": "dining",
                    "estimated_cost": 20.0 if ("over budget" in feedback.lower()) else 35.0,
                    "neighborhood": neigh,
                    "description": "Authentic regional lunch at curated local eatery."
                },
                {
                    "time": "03:30 PM",
                    "title": day_acts[1]["title"] if len(day_acts) > 1 else "Afternoon Exploration",
                    "category": day_acts[1]["category"] if len(day_acts) > 1 else "sightseeing",
                    "estimated_cost": day_acts[1]["estimated_cost"] if len(day_acts) > 1 else 10.0,
                    "neighborhood": neigh,
                    "description": day_acts[1]["description"] if len(day_acts) > 1 else "Discover neighborhood culture."
                }
            ]
            schedule.append({
                "day": d,
                "theme": f"Exploring {neigh} District",
                "neighborhood": neigh,
                "events": events
            })
            
        activities_total = sum(
            event["estimated_cost"]
            for day in schedule
            for event in day["events"]
        )
        
        total_estimated_cost = flight_cost + hotel_cost + activities_total
        
        state["current_itinerary"] = {
            "selected_flight": selected_flight,
            "selected_hotel": selected_hotel,
            "flight_cost": flight_cost,
            "hotel_cost_total": hotel_cost,
            "activities_cost_total": activities_total,
            "total_estimated_cost": round(total_estimated_cost, 2),
            "schedule": schedule
        }
        
        logger.log("Scheduler", "Optimization Room", "SCHEDULING_COMPLETED", {
            "iteration": iteration,
            "total_estimated_cost": total_estimated_cost
        })
        return state

class BudgetEnforcer:
    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        budget = state["user_input"]["budget"]
        total_cost = state["current_itinerary"]["total_estimated_cost"]
        iteration = state.get("iteration_count", 1)
        
        logger.log("BudgetEnforcer", "Optimization Room", "EVALUATION_START", {
            "iteration": iteration,
            "total_cost": total_cost,
            "budget": budget
        })
        
        if total_cost <= budget:
            state["budget_approved"] = True
            state["critic_feedback"] = f"Budget Approved: Total cost ${total_cost:.2f} is within budget of ${budget:.2f}."
            logger.log("BudgetEnforcer", "Optimization Room", "BUDGET_APPROVED", {
                "total_cost": total_cost,
                "budget": budget
            })
        else:
            state["budget_approved"] = False
            excess = total_cost - budget
            state["critic_feedback"] = f"Over budget by ${excess:.2f}! Total cost (${total_cost:.2f}) exceeds allocated budget (${budget:.2f}). Requesting budget flight/hotel options and lower-cost activities."
            logger.log("BudgetEnforcer", "Optimization Room", "BUDGET_REJECTED", {
                "excess": excess,
                "critic_feedback": state["critic_feedback"]
            })
            
        return state

class LoopAgent:
    def __init__(self, max_iterations: int = 5):
        self.scheduler = Scheduler()
        self.budget_enforcer = BudgetEnforcer()
        self.max_iterations = max_iterations

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.log("LoopAgent", "Optimization Room", "LOOP_START", {"max_iterations": self.max_iterations})
        
        while not state.get("budget_approved", False) and state.get("iteration_count", 0) < self.max_iterations:
            state = self.scheduler.run(state)
            state = self.budget_enforcer.run(state)
            if state.get("budget_approved"):
                break
                
        if not state.get("budget_approved"):
            logger.log("LoopAgent", "Optimization Room", "LOOP_CAP_REACHED", {
                "iterations": state.get("iteration_count"),
                "final_feedback": state.get("critic_feedback")
            })
        else:
            logger.log("LoopAgent", "Optimization Room", "LOOP_SUCCESS", {
                "iterations": state.get("iteration_count")
            })
            
        return state

class SequentialPipeline:
    def __init__(self):
        self.parallel_discovery = ParallelAgent()
        self.loop_optimization = LoopAgent(max_iterations=5)

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.log("SequentialPipeline", "Pipeline Execution", "PIPELINE_START", {"destination": state["user_input"]["destination"]})
        
        # Step 1: Parallel Discovery Phase
        state = self.parallel_discovery.run(state)
        
        # Step 2: Loop Optimization Phase
        state = self.loop_optimization.run(state)
        
        logger.log("SequentialPipeline", "Pipeline Execution", "PIPELINE_COMPLETE", {
            "budget_approved": state.get("budget_approved"),
            "total_iterations": state.get("iteration_count"),
            "total_cost": state["current_itinerary"].get("total_estimated_cost")
        })
        return state
