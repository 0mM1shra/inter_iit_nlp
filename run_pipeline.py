#!/usr/bin/env python3
"""
ACT-TREE 360 End-to-End Pipeline Entrypoint
Author: Om Mishra (Electronics Engineering 3rd Year, IIT BHU)
"""

import os
import sys
import json
from src.stream_processor import StreamProcessor
from src.state_board import SharedStateBoard
from src.memory_engine import MemoryEngine
from src.guardrails import GuardrailEngine
from src.hitl_engine import HITLEngine

from src.agents.usage_agent import UsageAgent
from src.agents.support_agent import SupportAgent
from src.agents.txn_agent import TransactionAgent
from src.agents.kyc_agent import KYCAgent
from src.agents.synthesis_agent import SynthesisAgent
from src.agents.debate_agent import ActorCriticDebate
from src.agents.action_agent import ActionAgent
from src.agents.refiner_agent import CritiqueRefinerAgent

def run_scenario_pipeline(scenario_dir, output_filename="inferred_events.json"):
    print(f"\n==================================================")
    print(f" Running ACT-TREE 360 Pipeline on: {scenario_dir}")
    print(f"==================================================")

    stream_proc = StreamProcessor(scenario_dir)
    customer_id = stream_proc.entities.get("customer", {}).get("customer_id", "CUST_UNKNOWN")
    
    # Initialize Core Engines
    state_board = SharedStateBoard(customer_id)
    memory_engine = MemoryEngine(customer_id)
    guardrail_engine = GuardrailEngine()

    # Initialize Swarm & Synthesis Agents
    usage_agent = UsageAgent(state_board)
    support_agent = SupportAgent(state_board)
    txn_agent = TransactionAgent(state_board)
    kyc_agent = KYCAgent(state_board)
    
    synthesis_agent = SynthesisAgent(state_board, memory_engine)
    debate_agent = ActorCriticDebate(state_board)
    action_agent = ActionAgent(memory_engine)
    refiner_agent = CritiqueRefinerAgent(guardrail_engine)

    # Determine Checkpoints to Evaluate from ground_truth or default timestamps
    gt_path = os.path.join(scenario_dir, "ground_truth.json")
    checkpoint_timestamps = []
    if os.path.exists(gt_path):
        with open(gt_path, 'r', encoding='utf-8') as f:
            gt_data = json.load(f)
            checkpoint_timestamps = [cp["as_of_time"] for cp in gt_data.get("checkpoints", [])]
    else:
        # Default checkpoints
        checkpoint_timestamps = ["2026-02-15T00:00:00Z", "2026-03-15T00:00:00Z", "2026-03-27T00:00:00Z"]

    output_checkpoints = []

    for ts in checkpoint_timestamps:
        # 1. Feature Aggregation up to checkpoint time
        features = stream_proc.compute_sliding_window_features(ts, window_days=45)

        # 2. Swarm Agents execution (Parallel structured writes to State Board)
        usage_agent.process_features(features, ts)
        support_agent.process_features(features, ts)
        txn_agent.process_features(features, ts)
        kyc_agent.process_features(features, ts)

        # 3. Synthesis & Hypothesis Tree Reasoning
        synth_res = synthesis_agent.synthesize_state(ts)

        # 4. Multi-Agent Debate & Red-Herring Audit
        reconciled_synth = debate_agent.evaluate_conflict(synth_res, ts)

        # 5. Action & Offer Selection
        action_proposal = action_agent.decide_action(reconciled_synth, ts)

        # 6. Critique-Refiner & Guardrail Pass
        raw_support_texts = [s.get("payload", {}).get("raw_text", "") for s in features.get("support_logs", [])]
        final_action = refiner_agent.audit_proposal(action_proposal, raw_support_texts)

        # 7. HITL Routing Calibration
        hitl_status = HITLEngine.evaluate_routing(
            action=final_action["action"],
            confidence_band=reconciled_synth["confidence_band"],
            action_subtype=final_action["action_subtype"]
        )

        output_cp = {
            "as_of_time": ts,
            "inferred_state": reconciled_synth["inferred_state"],
            "confidence_band": reconciled_synth["confidence_band"],
            "action": final_action["action"],
            "action_subtype": final_action["action_subtype"],
            "hitl_status": hitl_status,
            "notes": final_action["notes"]
        }
        output_checkpoints.append(output_cp)

    # Save inferred events output
    out_path = os.path.join(scenario_dir, output_filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output_checkpoints, f, indent=2)

    print(f"Generated inferred events written to: {out_path}")
    return out_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        out_file = run_scenario_pipeline(target_dir)
        
        # Evaluate automatically against ground truth
        gt_file = os.path.join(target_dir, "ground_truth.json")
        if os.path.exists(gt_file):
            from evaluate_scenarios import evaluate_scenario
            evaluate_scenario(gt_file, out_file)
    else:
        # Run across all practice scenarios
        base_dir = "customer_360_dataset"
        scenarios = ["scenario_01", "scenario_02", "scenario_03"]
        from evaluate_scenarios import evaluate_scenario
        for sc in scenarios:
            sc_dir = os.path.join(base_dir, sc)
            if os.path.exists(sc_dir):
                out_f = run_scenario_pipeline(sc_dir)
                gt_f = os.path.join(sc_dir, "ground_truth.json")
                if os.path.exists(gt_f):
                    evaluate_scenario(gt_f, out_f)
