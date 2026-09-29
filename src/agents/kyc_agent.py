"""
KYC / Compliance Agent for ACT-TREE 360
Monitors demographic updates, dependents changes (e.g. 1 to 2), address relocations, and watchlist matches.
"""

class KYCAgent:
    def __init__(self, state_board):
        self.state_board = state_board

    def process_features(self, features, as_of_time_str):
        kyc_updates = features.get("kyc_updates", [])
        
        for k in kyc_updates:
            payload = k.get("payload", {})
            subtype = payload.get("event_subtype", "")
            old_val = payload.get("old_value")
            new_val = payload.get("new_value")

            if subtype == "dependents_change" or "dependent" in str(payload):
                self.state_board.publish_assertion("dependents_changed_flag", True, 1.0, as_of_time_str, half_life_days=365)
                self.state_board.publish_assertion("dependents_count_new", new_val, 1.0, as_of_time_str, half_life_days=365)

            if subtype == "address_change":
                self.state_board.publish_assertion("relocation_address_changed", True, 0.95, as_of_time_str, half_life_days=180)

            if subtype == "marital_status_change":
                self.state_board.publish_assertion("marital_status_changed", True, 0.95, as_of_time_str, half_life_days=180)
