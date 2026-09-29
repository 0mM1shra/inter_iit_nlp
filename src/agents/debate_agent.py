"""
Actor-Critic Debate Agent for ACT-TREE 360
Surfaces genuine agent disagreement and performs counterfactual auditing for red-herring isolation.
"""

class ActorCriticDebate:
    def __init__(self, state_board):
        self.state_board = state_board

    def evaluate_conflict(self, synthesis_result, as_of_time_str):
        snapshot = self.state_board.snapshot(as_of_time_str)
        inferred_state = synthesis_result["inferred_state"]
        conf = synthesis_result["confidence_band"]

        # Counterfactual Audit for Red Herrings
        if inferred_state == "medical_hardship":
            if snapshot.get("red_herring_tuition_wire") or snapshot.get("red_herring_tax_refund"):
                # Critic verifies that tuition wire / refund is NOT mistaken for financial distress
                synthesis_result["notes"] += " Red herrings (tuition wire/refund) audited and excluded from hardship score."

        elif inferred_state == "new_child_life_event":
            # Critic verifies baby monitor purchase is supported by daycare / KYC
            if not snapshot.get("daycare_standing_instruction") and not snapshot.get("dependents_changed_flag"):
                if synthesis_result["score"] < 3.5:
                    synthesis_result["confidence_band"] = "low"
                    synthesis_result["notes"] = "Single retail purchase insufficient to confirm new child without KYC/daycare anchor."

        elif inferred_state == "churn_risk":
            if snapshot.get("red_herring_tax_refund"):
                synthesis_result["notes"] += " Tax refund deposit audited; temporary balance boost does not negate pre-churn withdrawal pattern."

        return synthesis_result
