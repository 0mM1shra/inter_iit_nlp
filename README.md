# Agentic Customer 360 — Proactive Intervention Desk
### Inter IIT Tech Meet 15.0 Prepathon (Natural Language Processing Track)
**End-Term Final Submission**  
**Author**: Om Mishra | Electronics Engineering (3rd Year), IIT (BHU) Varanasi | Roll No.: 24095073  
**GitHub Repository**: https://github.com/0mM1shra/inter_iit_nlp_mid  

---

## 📌 Executive Summary
This repository contains the **End-Term Final Submission** for the *Agentic Customer 360 — Proactive Intervention Desk* problem statement.

Traditional Customer 360 architectures rely on static CRM dashboards requiring manual human observation. This project implements **`ACT-TREE 360`** (*Actor-Critic Blackboard Swarm with Dynamic Life-Phase Hypothesis Trees*), an **Ambient, Event-Driven Multi-Agent System (MAS)** that continuously parses multi-modal customer event streams (card transactions, banking ledgers, web/app telemetry, support logs, KYC updates), infers evolving customer states/life events (medical hardship, new child, churn risk, etc.), and executes costed interventions with strict explainability, traceability, and Human-in-the-Loop (HITL) checkpoints.

---

## 🏆 Key Achievements & Evaluation Benchmarks

Our system was benchmarked using the automated evaluation harness (`evaluate_scenarios.py`) across all official practice scenarios, achieving a **100% Perfect Score**:

- **Scenario 01 (Marcus Vance - Medical Hardship)**: **110.0 / 110.0 (100.0%)**
- **Scenario 02 (Priya Sharma - New Child Event)**: **70.0 / 70.0 (100.0%)**
- **Scenario 03 (David Chen - Churn Risk Withdrawal)**: **100.0 / 100.0 (100.0%)**

---

## 📂 Repository Structure & End-Term Deliverables

All required deliverables are compiled under `endterm_submission/` and `src/`:

```
NLP/
├── endterm_submission/
│   ├── ENDTERM_SUBMISSION.md                 # Central End-Term Index & User Guide
│   ├── 01_research_log.md                    # Research Log & Literature Grounding (30% Weight)
│   ├── 02_system_architecture.md             # Architecture Spec & Visual Mermaid Flowcharts (20% Weight)
│   ├── 03_solution_document.md               # 3-Page Solution Document (Hard Constraint!)
│   └── 04_testing_and_evaluation.md          # Benchmark Evaluation Report & Failure Mode Analysis
├── src/                                      # Complete Working Codebase (25% Weight)
│   ├── stream_processor.py                   # Event-time watermarking & windowed feature aggregations
│   ├── state_board.py                        # Shared Per-Customer State Board with decay
│   ├── memory_engine.py                      # 3-Tiered Memory Architecture (Working, Episodic, Semantic)
│   ├── guardrails.py                         # Hard-stop keyword guardrails & data-layer PII redaction
│   ├── hitl_engine.py                        # Calibrated HITL routing & citation graph generator
│   └── agents/
│       ├── usage_agent.py                    # App/web telemetry & login trend analyzer
│       ├── support_agent.py                  # Support transcript NLP & sentiment scanner
│       ├── txn_agent.py                      # Ledger anomaly scorer & standing instruction tracker
│       ├── kyc_agent.py                      # Demographic & KYC update processor
│       ├── synthesis_agent.py                # Bayesian Life-Phase Hypothesis Tree engine
│       ├── debate_agent.py                   # Actor-Critic multi-agent debate engine
│       ├── action_agent.py                   # Offer eligibility & action composer
│       └── refiner_agent.py                  # Critique-Refiner compliance & tone auditor
├── midterm_submission/                       # Mid-Term Submission Archive
├── run_pipeline.py                           # Command-line pipeline entrypoint
├── evaluate_scenarios.py                     # Benchmark scoring harness
└── README.md                                 # Top-level repository landing page
```

---

## 📑 End-Term Deliverables Overview

| Deliverable | File Link | Key Highlights |
|---|---|---|
| **Deliverable 1: Research Log** | [`endterm_submission/01_research_log.md`](endterm_submission/01_research_log.md) | Grounded in 10 arXiv papers (MemGPT, MetaGPT, DyLAN, Self-RAG, Guardrails AI, Calibrated HITL), 5 engineering blogs (Stripe, Uber Flink, Netflix, Databricks, DoorDash), 4 agent frameworks, and Event Stream Analysis. |
| **Deliverable 2: System Architecture Spec** | [`endterm_submission/02_system_architecture.md`](endterm_submission/02_system_architecture.md) | Visual Mermaid Flowcharts, Event-Time Streaming Ingestion, Shared Per-Customer State Board, 3-Tiered Memory Architecture, Swarm + Debate + Refiner Topologies, and Safety Rails. |
| **Deliverable 3: Solution Document (3 Pages)** | [`endterm_submission/03_solution_document.md`](endterm_submission/03_solution_document.md) | Hard 3-page solution document covering problem overview (Page 1), architecture & topologies (Page 2), and benchmark evaluation, non-negotiables & trade-offs (Page 3). |
| **Deliverable 4: Testing & Evaluation** | [`endterm_submission/04_testing_and_evaluation.md`](endterm_submission/04_testing_and_evaluation.md) | Detailed testing methodology, red herring isolation, lead-time calibration, and benchmark score breakdown. |
| **End-Term Index** | [`endterm_submission/ENDTERM_SUBMISSION.md`](endterm_submission/ENDTERM_SUBMISSION.md) | Central submission summary index and execution guide. |

---

## 🚀 Quickstart: Running the Pipeline Engine

To run the end-to-end multi-agent pipeline and evaluate scores:

```bash
python run_pipeline.py
```

To evaluate predictions against ground truth for a specific scenario:

```bash
python evaluate_scenarios.py customer_360_dataset/scenario_01/ground_truth.json customer_360_dataset/scenario_01/inferred_events.json
```
