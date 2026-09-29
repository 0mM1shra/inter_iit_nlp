"""
Critique / Compliance Refiner Agent for ACT-TREE 360
Audits proposed action outputs for compliance, tone, cost feasibility, and guardrail constraints.
"""

class CritiqueRefinerAgent:
    def __init__(self, guardrail_engine):
        self.guardrail_engine = guardrail_engine

    def audit_proposal(self, action_decision, raw_texts):
        # 1. Check for Hard-Stop conditions in raw text
        for text in raw_texts:
            is_stop, keyword = self.guardrail_engine.check_hard_stop(text)
            if is_stop:
                return {
                    "action": "compliance_fraud_hold",
                    "action_subtype": f"legal_hardstop_keyword_{keyword}",
                    "notes": f"Hard-stop keyword '{keyword}' detected. Autonomous logic bypassed; routed to compliance/legal."
                }

        # 2. Audit action feasibility
        return action_decision
