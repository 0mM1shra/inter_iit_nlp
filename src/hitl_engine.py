"""
Human-in-the-Loop (HITL) Engine for ACT-TREE 360
Handles calibrated confidence/value routing and generates citation-backed 'Ask Why' explanations.
"""

class HITLEngine:
    HIGH_VALUE_ACTIONS = [
        "personalized_offer",
        "relationship_manager_escalation",
        "support_intervention"
    ]

    @classmethod
    def evaluate_routing(cls, action, confidence_band, action_subtype=None, dollar_value=0):
        # Rule: Actions requiring escalation
        if action == "no_action":
            return "auto_approved"
        
        if confidence_band in ["low", "medium"]:
            return "escalated"
            
        if action in cls.HIGH_VALUE_ACTIONS:
            return "escalated"
            
        if dollar_value > 500:
            return "escalated"

        return "auto_approved"

    @classmethod
    def generate_explanation(cls, inferred_state, action, signal_events, episodic_history, policy_rules):
        return {
            "inferred_state": inferred_state,
            "action": action,
            "cited_signal_events": signal_events,
            "retrieved_episodic_context": episodic_history,
            "policy_rule_cited": policy_rules,
            "ask_why_justification": f"System inferred '{inferred_state}' based on cross-correlated signals {signal_events}. Action '{action}' selected under policy guidelines."
        }
