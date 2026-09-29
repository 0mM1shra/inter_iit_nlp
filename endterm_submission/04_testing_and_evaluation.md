# End-Term Testing & Evaluation Report
**Project**: Agentic Customer 360 — Proactive Intervention Desk  
**Framework**: `ACT-TREE 360`  
**Author**: Om Mishra | Electronics Engineering (3rd Year), IIT (BHU) Varanasi | Roll No.: 24095073  

---

## 1. Evaluation Harness & Methodology

In accordance with Section 7.5 and 8.1 of the Problem Statement, system accuracy was evaluated using the automated scoring harness (`evaluate_scenarios.py`).

The harness evaluates predictions against ground truth timelines across five metrics:
1. **State Inference Accuracy**: Correctly identifying `inferred_state`.
2. **Action Precision**: Selecting the exact bounded `action` and `action_subtype`.
3. **HITL Calibration**: Routing logic matching `hitl_status` (`auto_approved` vs `escalated`).
4. **False Positive & Red Herring Penalties**: Penalizing premature actions triggered by noisy events.
5. **Timeliness & Lead Time**: Evaluating inference at target timestamp checkpoints.

---

## 2. Benchmark Score Summary

```
==================================================
 Running ACT-TREE 360 Pipeline on: customer_360_dataset\scenario_01
==================================================
Scenario ID: scenario_05_major_medical_event
Narrative Summary: Marcus Vance (Medical Emergency)
--- Checking Checkpoints (3 expected) ---
Checkpoint #1 [2026-02-15T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Checkpoint #2 [2026-03-12T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Checkpoint #3 [2026-03-26T00:00:00Z]: [PASS] (Score: 30.0/30.0)
--- Checking Red Herring / False Positive Penalties (2 checks) ---
Red Herring EVT_000382 (Tuition Wire): [PASS]
Red Herring EVT_000402 (Resort Refund): [PASS]
FINAL SCORE: 110.0 / 110.0 (100.0%)

==================================================
 Running ACT-TREE 360 Pipeline on: customer_360_dataset\scenario_02
==================================================
Scenario ID: scenario_06_new_child
Narrative Summary: Priya Sharma (New Child Life Event)
--- Checking Checkpoints (2 expected) ---
Checkpoint #1 [2026-02-20T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Checkpoint #2 [2026-03-27T00:00:00Z]: [PASS] (Score: 30.0/30.0)
--- Checking Red Herring / False Positive Penalties (1 checks) ---
Red Herring EVT_000328 (Baby Monitor Electronics Spend): [PASS]
FINAL SCORE: 70.0 / 70.0 (100.0%)

==================================================
 Running ACT-TREE 360 Pipeline on: customer_360_dataset\scenario_03
==================================================
Scenario ID: scenario_07_churn_risk
Narrative Summary: David Chen (Churn Risk Withdrawal)
--- Checking Checkpoints (3 expected) ---
Checkpoint #1 [2026-02-15T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Checkpoint #2 [2026-03-08T00:00:00Z]: [PASS] (Score: 30.0/30.0)
Checkpoint #3 [2026-04-10T00:00:00Z]: [PASS] (Score: 30.0/30.0)
--- Checking Red Herring / False Positive Penalties (1 checks) ---
Red Herring EVT_000447 (Tax Refund Deposit): [PASS]
FINAL SCORE: 100.0 / 100.0 (100.0%)
```

---

## 3. Failure Mode & Red Herring Analysis

### 3.1 Red Herring Isolation Mechanisms
- **Tuition Wire (`EVT_000382`)**: Large outbound transfer to a university. The Actor-Critic Debate agent verified MCC category and counterparty name, preventing the system from mistaking tuition payments for sudden wealth drain or account takeover.
- **Resort Refund (`EVT_000402`)**: Vacation refund deposit. The system suppressed investment offer triggers by requiring sustained wealth growth indicators over 60 days.
- **Tax Refund (`EVT_000447`)**: Large deposit during pre-churn activity. Recognized as a passive tax refund resting temporarily prior to account closure.

### 3.2 Lead-Time Calibration Insights
- In **Scenario 03 (David Chen)**, detection at Checkpoint #2 (March 08) immediately following standing instruction cancellation saved the relationship. Waiting until Checkpoint #3 (April 10, zero card usage) was flagged as late-stage outreach.
