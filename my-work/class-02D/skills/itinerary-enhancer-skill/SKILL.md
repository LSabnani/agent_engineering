---
name: itinerary-enhancer-skill
description: Skill for clustering daily travel activities geographically, optimizing schedules, and applying budget sensitivity.
---

# Itinerary Enhancer Skill

This skill provides guidelines and patterns for generating optimized, enjoyable, and cost-effective travel itineraries.

## Core Rules

1. **Geographic Clustering**:
   - Always group daily activities within the same district/neighborhood to minimize travel time and transit costs.
   - Example (Kyoto): Group Gion + Kiyomizu-dera on Day 1; Arashiyama Bamboo Grove + Tenryu-ji on Day 2.

2. **Pacing & Timing**:
   - Provide 3-4 activities per day max (Morning landmark, Lunch/Cultural experience, Afternoon highlight, Dinner).
   - Time slots should be standard formatted strings (e.g., "09:00 AM", "01:00 PM", "04:30 PM", "07:30 PM").

3. **Budget Adaptation**:
   - When receiving `critic_feedback` warning about over-budget status:
     - Priority 1: Swap luxury/paid activities for high-rated free/budget cultural sites (e.g., public parks, free temples, scenic viewpoints).
     - Priority 2: Select mid-range or budget lodging options from raw research.
     - Priority 3: Swap private tours for self-guided walking tours or public transport.

4. **Interest Matching**:
   - Align themes of days directly with user interests (e.g., "Food & Dining" day with local market tours; "Culture" day with historical heritage sites).
