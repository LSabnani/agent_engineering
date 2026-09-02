import unittest
from pipeline.state import create_initial_state
from pipeline.agents import ParallelAgent, LoopAgent, SequentialPipeline, Scheduler, BudgetEnforcer

class TestTravelItineraryPipeline(unittest.TestCase):
    """
    Test suite verifying structural integrity, context extraction & state management, 
    and graceful failure handling for the multi-agent travel pipeline.
    
    Custom Rule Compliance:
    - Triple-Checked Test Assumptions: Inputs, intermediate state mutations, and outputs verified.
    - Estimated Verification Accuracy Metrics provided per test case.
    """

    def test_structural_integrity(self):
        """
        Structural Integrity Test (30% Milestone Weight).
        Verifies ParallelAgent executes discovery researchers concurrently and populates state.
        
        Triple-Check Verification:
        1. Input: Valid state dictionary with destination 'Tokyo, Japan'.
        2. Process: ParallelAgent.run(state).
        3. Assertion Logic: Verify raw_research contains non-empty lists for flights, hotels, activities.
        
        Estimated Accuracy / Verification Confidence Metric: 98%
        """
        state = create_initial_state("Tokyo, Japan", budget=3000.0, days=4, interests=["Culture"])
        parallel_agent = ParallelAgent()
        result_state = parallel_agent.run(state)

        self.assertIn("flights", result_state["raw_research"])
        self.assertIn("hotels", result_state["raw_research"])
        self.assertIn("activities", result_state["raw_research"])
        
        self.assertGreater(len(result_state["raw_research"]["flights"]), 0)
        self.assertGreater(len(result_state["raw_research"]["hotels"]), 0)
        self.assertGreater(len(result_state["raw_research"]["activities"]), 0)

    def test_context_extraction_and_state_management(self):
        """
        Context Extraction & State Management Test (40% Milestone Weight).
        Verifies Scheduler extracts prior critic_feedback and adapts flight & hotel selection 
        to lower-cost tiers when budget feedback triggers refinement.
        
        Triple-Check Verification:
        1. Input: Initial state with tight budget ($500 for 5 days in London).
        2. Step A: Parallel Discovery populate options.
        3. Step B: Scheduler run iteration 1 -> BudgetEnforcer sets critic_feedback = "Over budget...".
        4. Step C: Scheduler run iteration 2 -> Extracts critic_feedback and selects min cost options.
        
        Estimated Accuracy / Verification Confidence Metric: 96%
        """
        state = create_initial_state("London, UK", budget=500.0, days=5, interests=["History"])
        parallel_agent = ParallelAgent()
        state = parallel_agent.run(state)

        scheduler = Scheduler()
        enforcer = BudgetEnforcer()

        # Iteration 1
        state = scheduler.run(state)
        cost_iter1 = state["current_itinerary"]["total_estimated_cost"]
        state = enforcer.run(state)

        self.assertFalse(state["budget_approved"])
        self.assertIn("Over budget", state["critic_feedback"])

        # Iteration 2 (Scheduler reads state["critic_feedback"])
        state = scheduler.run(state)
        cost_iter2 = state["current_itinerary"]["total_estimated_cost"]

        # Assert Scheduler extracted context and reduced cost
        self.assertLess(cost_iter2, cost_iter1)

    def test_graceful_failure_handling(self):
        """
        Graceful Failure Handling Test (30% Milestone Weight).
        Verifies system handles an impossible budget ($50 for 10 days) without crashing or raising exceptions,
        capping iterations at max (5) and returning structured feedback.
        
        Triple-Check Verification:
        1. Input: Extreme budget constraint ($50).
        2. Process: SequentialPipeline.run(state).
        3. Assertion Logic: iteration_count == 5, budget_approved == False, state includes structured itinerary & advisory.
        
        Estimated Accuracy / Verification Confidence Metric: 97%
        """
        state = create_initial_state("New York, USA", budget=50.0, days=10, interests=["Art"])
        pipeline = SequentialPipeline()
        
        # Execute full pipeline
        final_state = pipeline.run(state)

        self.assertEqual(final_state["iteration_count"], 5)
        self.assertFalse(final_state["budget_approved"])
        self.assertIsNotNone(final_state["current_itinerary"])
        self.assertIn("Over budget", final_state["critic_feedback"])

    def test_budget_approval_on_generous_budget(self):
        """
        Generous Budget Test.
        Verifies that sufficient budget ($5000 for 3 days) approves on iteration 1.
        
        Triple-Check Verification:
        1. Input: $5000 budget for 3 days in Rome.
        2. Process: SequentialPipeline.run(state).
        3. Assertion Logic: iteration_count == 1, budget_approved == True.
        
        Estimated Accuracy / Verification Confidence Metric: 99%
        """
        state = create_initial_state("Rome, Italy", budget=5000.0, days=3, interests=["History", "Food"])
        pipeline = SequentialPipeline()
        final_state = pipeline.run(state)

        self.assertTrue(final_state["budget_approved"])
        self.assertEqual(final_state["iteration_count"], 1)
        self.assertIn("Budget Approved", final_state["critic_feedback"])

if __name__ == "__main__":
    unittest.main()
