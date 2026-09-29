"""
Shared Per-Customer State Board for ACT-TREE 360
Maintains structured epistemic assertions with exponential decay half-lives to prevent memory leakage.
"""

from datetime import datetime
import math

def parse_iso(ts_str):
    if not ts_str:
        return None
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))

class SharedStateBoard:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.assertions = {}  # key -> {val, confidence, timestamp, half_life_days}

    def publish_assertion(self, key, value, confidence, timestamp, half_life_days=30):
        self.assertions[key] = {
            "value": value,
            "confidence": confidence,
            "timestamp": timestamp,
            "half_life_days": half_life_days
        }

    def get_assertion(self, key, as_of_time_str):
        if key not in self.assertions:
            return None
        data = self.assertions[key]
        as_of_dt = parse_iso(as_of_time_str)
        pub_dt = parse_iso(data["timestamp"])
        
        if as_of_dt and pub_dt:
            delta_days = max(0, (as_of_dt - pub_dt).total_seconds() / 86400.0)
            decay_factor = math.exp(-0.693 * delta_days / max(1, data["half_life_days"]))
            effective_confidence = data["confidence"] * decay_factor
            return {
                "value": data["value"],
                "raw_confidence": data["confidence"],
                "effective_confidence": round(effective_confidence, 4),
                "timestamp": data["timestamp"]
            }
        return data

    def snapshot(self, as_of_time_str):
        snap = {}
        for k in self.assertions:
            res = self.get_assertion(k, as_of_time_str)
            if res and res["effective_confidence"] > 0.05:
                snap[k] = res
        return snap
