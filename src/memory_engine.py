"""
3-Tiered Memory Architecture for ACT-TREE 360
Manages Working Memory, Episodic Memory (decay-weighted RAG), and Semantic Memory (Policy Base).
"""

from datetime import datetime

def parse_iso(ts_str):
    if not ts_str:
        return None
    return datetime.fromisoformat(ts_str.replace("Z", "+00:00"))

class MemoryEngine:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.working_memory = []
        self.episodic_memory = []
        self.semantic_policy_base = {
            "medical_hardship_payment_plan": {
                "min_income_disruption": 0.30,
                "eligibility_terms": "High-value or tenured customers with verifiable medical income disruption or hospitalization.",
                "max_duration_months": 6
            },
            "childcare_savings_or_insurance_offer": {
                "eligibility_terms": "Customers with dependents update (e.g. 1 to 2) or sustained healthcare/retail child spend.",
                "product_type": "Child Savings 529 / Premium Family Insurance"
            },
            "premium_retention_offer_and_fee_waiver": {
                "eligibility_terms": "High-value tenured customers exhibiting churn risk (login drop + standing instruction cancellation).",
                "max_fee_waiver_usd": 250
            }
        }

    def add_working_memory(self, item):
        self.working_memory.append(item)

    def add_episodic_memory(self, event_id, event_time, event_type, summary, outcome=None):
        self.episodic_memory.append({
            "event_id": event_id,
            "event_time": event_time,
            "event_type": event_type,
            "summary": summary,
            "outcome": outcome
        })

    def query_episodic_memory(self, query_topic, as_of_time_str, top_k=5):
        # Decay-weighted relevance scoring
        as_of_dt = parse_iso(as_of_time_str)
        scored_memories = []
        for mem in self.episodic_memory:
            mem_dt = parse_iso(mem["event_time"])
            days_ago = max(0, (as_of_dt - mem_dt).total_seconds() / 86400.0) if as_of_dt and mem_dt else 0
            decay = 1.0 / (1.0 + 0.01 * days_ago)
            
            # Simple keyword relevance match
            relevance = 1.0 if any(term in mem["summary"].lower() for term in query_topic.lower().split()) else 0.5
            final_score = decay * relevance
            scored_memories.append((final_score, mem))

        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [m[1] for m in scored_memories[:top_k]]
