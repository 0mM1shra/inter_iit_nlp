"""
Support / Sentiment Agent for ACT-TREE 360
Monitors support tickets, call transcripts, sentiment scores, and unresolved complaint flags.
"""

class SupportAgent:
    def __init__(self, state_board):
        self.state_board = state_board

    def process_features(self, features, as_of_time_str):
        support_logs = features.get("support_logs", [])
        
        has_unresolved_complaint = False
        has_medical_ticket = False
        has_fee_dispute = False
        sentiment_score = 0.0

        for log in support_logs:
            payload = log.get("payload", {})
            raw_text = (payload.get("raw_text") or payload.get("summary") or "").lower()
            status = payload.get("resolution_status", "").lower()
            
            if "fee" in raw_text or "denied" in raw_text or "refund" in raw_text:
                has_fee_dispute = True
                sentiment_score -= 0.6
                if "resolved" not in status:
                    has_unresolved_complaint = True

            if "hospital" in raw_text or "medical" in raw_text or "hardship" in raw_text or "er visit" in raw_text:
                has_medical_ticket = True
                sentiment_score -= 0.5

        if has_unresolved_complaint:
            self.state_board.publish_assertion("unresolved_complaint_flag", True, 0.95, as_of_time_str, half_life_days=30)
        if has_fee_dispute:
            self.state_board.publish_assertion("fee_dispute_flag", True, 0.85, as_of_time_str, half_life_days=30)
        if has_medical_ticket:
            self.state_board.publish_assertion("medical_support_ticket", True, 0.98, as_of_time_str, half_life_days=45)
        
        self.state_board.publish_assertion("support_sentiment_score", round(sentiment_score, 2), 0.80, as_of_time_str, half_life_days=14)
