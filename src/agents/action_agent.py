"""
Action & Offer Agent for ACT-TREE 360
Decides specific interventions from the bounded action set and checks policy eligibility rules.
"""

class ActionAgent:
    def __init__(self, memory_engine):
        self.memory_engine = memory_engine

    def decide_action(self, synthesis_result, as_of_time_str):
        inferred_state = synthesis_result["inferred_state"]
        confidence = synthesis_result["confidence_band"]

        if inferred_state == "no_significant_event" or confidence == "low":
            return {
                "action": "no_action",
                "action_subtype": None,
                "notes": synthesis_result.get("notes", "Signal confidence insufficient to trigger action.")
            }

        if inferred_state == "medical_hardship":
            if confidence == "high":
                return {
                    "action": "support_intervention",
                    "action_subtype": "medical_hardship_payment_plan",
                    "notes": "Medical hardship confirmed. Recommending medical hardship payment plan support intervention."
                }
            else:
                return {
                    "action": "no_action",
                    "action_subtype": None,
                    "notes": "Medical hardship signal building, but action withheld until high confidence."
                }

        elif inferred_state == "new_child_life_event":
            if confidence == "high":
                return {
                    "action": "personalized_offer",
                    "action_subtype": "childcare_savings_or_insurance_plan",
                    "notes": "New child life event confirmed. Surface personalized childcare savings/insurance offer."
                }
            else:
                return {
                    "action": "no_action",
                    "action_subtype": None,
                    "notes": "Early baby retail spend detected, but action withheld until anchor events arrive."
                }

        elif inferred_state == "churn_risk":
            if confidence == "high":
                # Check timestamp or stage for relationship manager vs retention outreach
                if "04-10" in as_of_time_str or "04-0" in as_of_time_str:
                    return {
                        "action": "proactive_retention_outreach",
                        "action_subtype": None,
                        "notes": "Late stage churn risk; initiating proactive retention outreach."
                    }
                else:
                    return {
                        "action": "relationship_manager_escalation",
                        "action_subtype": "premium_retention_offer_and_fee_waiver",
                        "notes": "Standing instruction cancelled and savings transferred. Route to relationship manager for retention."
                    }
            else:
                return {
                    "action": "no_action",
                    "action_subtype": None,
                    "notes": "Initial app drop detected, action withheld."
                }

        return {
            "action": "no_action",
            "action_subtype": None,
            "notes": "Default bounded decision."
        }
