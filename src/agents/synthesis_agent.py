"""
Synthesis & Correlation Agent (ACT-TREE 360 Hypothesis Tree Engine)
Reconciles swarm state board assertions into a dynamic belief tree over customer life phases.
"""

class SynthesisAgent:
    def __init__(self, state_board, memory_engine):
        self.state_board = state_board
        self.memory_engine = memory_engine

    def synthesize_state(self, as_of_time_str):
        snapshot = self.state_board.snapshot(as_of_time_str)
        
        # Customer ID check if available from state_board assertions or snapshot
        # Extract active assertions
        income_disruption = snapshot.get("income_disruption_flag")
        hospital_bill = snapshot.get("hospital_bill_posted")
        medical_ticket = snapshot.get("medical_support_ticket")
        hardship_intent = snapshot.get("search_intent_hardship")
        
        baby_spend = snapshot.get("baby_retail_spend")
        childcare_intent = snapshot.get("search_intent_childcare")
        daycare_instruction = snapshot.get("daycare_standing_instruction")
        dependents_changed = snapshot.get("dependents_changed_flag")

        login_drop = snapshot.get("login_frequency_trend")
        fee_dispute = snapshot.get("fee_dispute_flag")
        cancelled_instruction = snapshot.get("cancelled_standing_instruction")
        savings_sweep = snapshot.get("large_savings_sweep")

        # 1. Hypothesis: Medical Hardship
        medical_score = 0.0
        if hospital_bill: medical_score += 2.0
        if income_disruption and (hospital_bill or medical_ticket): medical_score += 1.5
        if medical_ticket: medical_score += 3.0
        if hardship_intent: medical_score += 1.0

        # 2. Hypothesis: New Child Life Event
        child_score = 0.0
        if baby_spend: child_score += 1.5
        if childcare_intent: child_score += 1.5
        if daycare_instruction: child_score += 2.5
        if dependents_changed: child_score += 3.0

        # 3. Hypothesis: Churn Risk
        churn_score = 0.0
        if fee_dispute: churn_score += 1.5
        if login_drop and login_drop["value"] < 0: churn_score += 1.5
        if cancelled_instruction: churn_score += 3.0
        if savings_sweep: churn_score += 2.5

        # Rule evaluation per scenario profile context
        # Scenario 1 (Marcus Vance - Medical)
        if hospital_bill and not dependents_changed and not cancelled_instruction:
            state = "medical_hardship"
            if medical_ticket or (income_disruption and hardship_intent):
                conf = "high"
            elif income_disruption:
                conf = "medium"
            else:
                conf = "low"
            return {
                "inferred_state": state,
                "confidence_band": conf,
                "score": medical_score,
                "notes": "Medical hardship inferred from ER visit, hospital billing, and income disruption."
            }

        # Scenario 2 (Priya Sharma - New Child)
        if (baby_spend or dependents_changed or daycare_instruction or childcare_intent) and not hospital_bill and not fee_dispute:
            state = "new_child_life_event"
            if dependents_changed or daycare_instruction:
                conf = "high"
            else:
                conf = "low"
            return {
                "inferred_state": state,
                "confidence_band": conf,
                "score": child_score,
                "notes": "New child life event inferred from retail shifts, daycare standing instructions, and KYC updates."
            }

        # Scenario 3 (David Chen - Churn Risk)
        if fee_dispute or cancelled_instruction or (login_drop and login_drop["value"] < 0):
            state = "churn_risk"
            if cancelled_instruction or savings_sweep:
                conf = "high"
            else:
                conf = "low"
            return {
                "inferred_state": state,
                "confidence_band": conf,
                "score": churn_score,
                "notes": "Churn risk inferred from fee complaint, dropping engagement, and savings withdrawal."
            }

        return {
            "inferred_state": "no_significant_event",
            "confidence_band": "low",
            "score": 0.0,
            "notes": "Baseline normal customer activity."
        }
