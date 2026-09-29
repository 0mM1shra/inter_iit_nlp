"""
Stream Processor for ACT-TREE 360
Handles event-time watermarking, out-of-order queueing, and sliding-window aggregations.
"""

import json
import os
from datetime import datetime, timedelta

def parse_iso(ts_str):
    if not ts_str:
        return None
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))

class StreamProcessor:
    def __init__(self, scenario_dir):
        self.scenario_dir = scenario_dir
        self.entities = self._load_json(os.path.join(scenario_dir, "entities.json"))
        self.history = self._load_jsonl(os.path.join(scenario_dir, "history_seed.jsonl"))
        self.live_stream = self._load_jsonl(os.path.join(scenario_dir, "live_stream.jsonl"))
        
        # Sort live stream by event_time to guarantee event-time ordering
        self.live_stream.sort(key=lambda x: parse_iso(x.get("event_time", "1970-01-01T00:00:00Z")))
        
        # State tracking for feature aggregations
        self.all_events = self.history + self.live_stream
        self.all_events.sort(key=lambda x: parse_iso(x.get("event_time", "1970-01-01T00:00:00Z")))

    def _load_json(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _load_jsonl(self, path):
        events = []
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        events.append(json.loads(line))
        return events

    def get_events_up_to(self, as_of_time_str):
        as_of_dt = parse_iso(as_of_time_str)
        return [e for e in self.all_events if parse_iso(e.get("event_time")) <= as_of_dt]

    def compute_sliding_window_features(self, as_of_time_str, window_days=30):
        as_of_dt = parse_iso(as_of_time_str)
        start_dt = as_of_dt - timedelta(days=window_days)
        
        events_in_window = [
            e for e in self.all_events 
            if start_dt <= parse_iso(e.get("event_time")) <= as_of_dt
        ]
        
        # Feature extraction across source systems
        logins = [e for e in events_in_window if e.get("source_system") == "web_app_events" and e.get("event_type") == "login"]
        searches = [e for e in events_in_window if e.get("source_system") == "web_app_events" and e.get("event_type") == "search_query"]
        txns = [e for e in events_in_window if e.get("source_system") in ["card_payments", "instant_payments", "ach_wire", "core_banking_ledger"]]
        support = [e for e in events_in_window if e.get("source_system") == "support_logs"]
        kyc_updates = [e for e in events_in_window if e.get("source_system") == "loan_kyc"]

        return {
            "window_days": window_days,
            "login_count": len(logins),
            "search_count": len(searches),
            "searches": searches,
            "transaction_count": len(txns),
            "transactions": txns,
            "support_count": len(support),
            "support_logs": support,
            "kyc_updates": kyc_updates,
            "as_of_time": as_of_time_str
        }
