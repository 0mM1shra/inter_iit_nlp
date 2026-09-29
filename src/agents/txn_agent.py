"""
Transaction / Billing Agent for ACT-TREE 360
Monitors spending patterns, income dips, standing instruction cancellations, and identifies red-herring transfers.
"""

class TransactionAgent:
    def __init__(self, state_board):
        self.state_board = state_board

    def process_features(self, features, as_of_time_str):
        txns = features.get("transactions", [])
        
        income_dip = False
        disability_income = False
        hospital_spend = False
        daycare_instruction = False
        cancelled_instruction = False
        large_savings_sweep = False
        baby_store_spend = False
        tax_refund = False
        tuition_transfer = False

        for t in txns:
            payload = t.get("payload", {})
            amount = payload.get("amount", 0)
            merchant = (payload.get("merchant_name") or payload.get("counterparty_name") or "").lower()
            mcc = (payload.get("mcc_category") or "").lower()
            txn_type = (t.get("event_type") or payload.get("transaction_type") or "").lower()

            if "disability" in merchant or "short-term disability" in merchant or "maternity" in merchant:
                disability_income = True
                income_dip = True
            elif ("salary" in merchant or "payroll" in merchant) and amount > 0 and amount < 3500:
                income_dip = True

            if "hospital" in merchant or "er visit" in merchant or "emergency" in merchant or "medical" in merchant or "pharmacy" in merchant or "clinic" in merchant:
                hospital_spend = True

            if "daycare" in merchant or "preschool" in merchant or ("standing_instruction" in txn_type and "daycare" in merchant):
                if "cancel" not in txn_type:
                    daycare_instruction = True

            if "standing_instruction" in txn_type and ("cancel" in txn_type or "cancelled" in txn_type or "deletion" in txn_type or amount == 0):
                cancelled_instruction = True

            if ("outbound_transfer" in txn_type or "withdrawal" in txn_type or "wire" in txn_type) and amount >= 3000:
                large_savings_sweep = True
                if "university" in merchant or "tuition" in merchant or "college" in merchant:
                    tuition_transfer = True

            if "baby" in merchant or "infant" in merchant or "nursery" in merchant or "maternity" in mcc or "stroller" in merchant:
                baby_store_spend = True

            if "tax refund" in merchant or "irs" in merchant or "treasury" in merchant:
                tax_refund = True

        # Publish structured reads to State Board
        if income_dip or disability_income:
            self.state_board.publish_assertion("income_disruption_flag", True, 0.95, as_of_time_str, half_life_days=90)
        if hospital_spend:
            self.state_board.publish_assertion("hospital_bill_posted", True, 0.95, as_of_time_str, half_life_days=90)
        if daycare_instruction:
            self.state_board.publish_assertion("daycare_standing_instruction", True, 0.95, as_of_time_str, half_life_days=180)
        if cancelled_instruction:
            self.state_board.publish_assertion("cancelled_standing_instruction", True, 0.98, as_of_time_str, half_life_days=180)
        if large_savings_sweep and not tuition_transfer:
            self.state_board.publish_assertion("large_savings_sweep", True, 0.95, as_of_time_str, half_life_days=90)
        if baby_store_spend:
            self.state_board.publish_assertion("baby_retail_spend", True, 0.90, as_of_time_str, half_life_days=180)
        if tax_refund:
            self.state_board.publish_assertion("red_herring_tax_refund", True, 0.90, as_of_time_str, half_life_days=60)
        if tuition_transfer:
            self.state_board.publish_assertion("red_herring_tuition_wire", True, 0.90, as_of_time_str, half_life_days=60)
