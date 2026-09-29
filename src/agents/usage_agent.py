"""
Usage / Engagement Agent for ACT-TREE 360
Monitors app/web session frequency, login trends, search query intent, and feature drop-offs.
"""

class UsageAgent:
    def __init__(self, state_board):
        self.state_board = state_board

    def process_features(self, features, as_of_time_str):
        logins = features.get("login_count", 0)
        searches = features.get("searches", [])
        
        # Analyze search query intent
        search_texts = [s.get("payload", {}).get("search_text", "").lower() for s in searches]
        
        hardship_intent = any("hardship" in t or "payment plan" in t or "financial relief" in t for t in search_texts)
        childcare_intent = any("education savings" in t or "529 plan" in t or "daycare" in t or "baby" in t for t in search_texts)
        home_loan_intent = any("mortgage" in t or "home loan" in t for t in search_texts)

        # Publish structured reads to State Board
        if logins == 0:
            self.state_board.publish_assertion("login_frequency_trend", -1.0, 0.90, as_of_time_str, half_life_days=14)
        elif logins < 3:
            self.state_board.publish_assertion("login_frequency_trend", -0.50, 0.75, as_of_time_str, half_life_days=14)
        else:
            self.state_board.publish_assertion("login_frequency_trend", 0.0, 0.50, as_of_time_str, half_life_days=14)

        if hardship_intent:
            self.state_board.publish_assertion("search_intent_hardship", True, 0.95, as_of_time_str, half_life_days=30)
        if childcare_intent:
            self.state_board.publish_assertion("search_intent_childcare", True, 0.95, as_of_time_str, half_life_days=30)
        if home_loan_intent:
            self.state_board.publish_assertion("search_intent_homeloan", True, 0.90, as_of_time_str, half_life_days=30)
