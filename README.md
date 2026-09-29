# Agentic Customer 360 — Proactive Intervention Desk
### Inter IIT Tech Meet 15.0 Prepathon (Natural Language Processing Track)

**Author**: Om Mishra | Electronics Engineering (3rd Year), IIT (BHU) Varanasi | Roll No.: 24095073  
**GitHub Repository**: [https://github.com/0mM1shra/inter_iit_nlp_mid](https://github.com/0mM1shra/inter_iit_nlp_mid)  

---

## 📌 Executive Summary

"Customer 360" has long been the holy grail of enterprise architecture: aggregating a single, unified view of a customer's entire footprint across transactions, support tickets, app telemetry, and KYC updates. Historically, institutions dumped data into massive lakes and built passive CRM dashboards. However, dashboards are passive—they rely on human account managers to log in and spot subtle shifts, such as a high-value client quietly building up churn risk or entering financial distress.

This project implements **`ACT-TREE 360`** (*Actor-Critic Blackboard Swarm with Dynamic Life-Phase Hypothesis Trees*), an **Ambient, Event-Driven Multi-Agent System (MAS)** that continuously parses multi-modal customer telemetry streams, infers evolving customer states/life events (medical hardship, new child, churn risk, etc.), and executes bounded, costed interventions with strict explainability, traceability, and Human-in-the-Loop (HITL) checkpoints.

---

## 🚀 Key Evolutionary Highlights: Mid-Term $\to$ End-Term Evolution

The architecture evolved significantly from the preliminary Mid-Term design to the production-grade End-Term implementation:

```
+-----------------------------------------------------------------------------------+
|                           MID-TERM (Preliminary Design)                           |
|  - Paper research & theoretical agent definitions                                  |
|  - Static rule-based hypothesis checks                                            |
|  - Preliminary state board outline & static 1-page report                         |
|  - Baseline scenario inspection                                                    |
+-----------------------------------------------------------------------------------+
                                         │
                                         ▼ EVOLUTION & UPGRADES
+-----------------------------------------------------------------------------------+
|                            END-TERM (`ACT-TREE 360`)                              |
|  - Dynamic Bayesian Life-Phase Hypothesis Trees (belief tracking over time)       |
|  - Per-Customer Epistemic Blackboard (`StateBoard`) with temporal decay half-lives  |
|  - Actor-Critic Multi-Agent Debate Engine with Adversarial Red-Herring Auditing   |
|  - Hard-Stop Blast-Radius Guardrails & Data-Layer PII Tokenization                |
|  - Calibrated HITL Routing with Citation-Backed "Ask Why" Graph Generation         |
|  - Fully Runnable Python Codebase (`src/` & `run_pipeline.py`)                     |
|  - 100% Perfect Score Across All Benchmark Scenarios                              |
+-----------------------------------------------------------------------------------+
```

### Detailed Architectural Changes (Mid-Term vs. End-Term)

| Dimension | Mid-Term Submission (Preliminary) | End-Term Final Submission (`ACT-TREE 360`) |
|---|---|---|
| **State Inference Engine** | Static rule-based heuristic checks | **Dynamic Bayesian Life-Phase Hypothesis Trees**: Probabilistic belief trees ($P(\text{medical\_hardship})$, $P(\text{new\_child})$, $P(\text{churn\_risk})$) that track state trajectory over time. |
| **Memory Architecture** | Basic context logs | **Per-Customer Epistemic Blackboard (`StateBoard`)**: Customer-scoped key-value assertions with exponential decay half-lives ($\lambda_{usage}=14\text{d}$, $\lambda_{kyc}=365\text{d}$), eliminating context pollution. |
| **Red Herring Handling** | Manual inspection | **Actor-Critic Adversarial Debate Engine**: Actor Agent proposes state hypotheses, while Critic Agent audits counterfactual red-herring rules (isolating tuition wires, vacation refunds, and tax deposits). |
| **Safety & Security** | Prompt instructions | **Deterministic Hard-Stop Guardrails & Data-Layer PII Tokenization**: Non-bypassable regex scanners for legal/AML threats (`"lawsuit"`, `"attorney"`) and automatic PII redaction before LLM prompts. |
| **Human-in-the-Loop** | Conceptual checkpoint | **Calibrated HITL Engine**: Automated routing (`auto_approved` vs `escalated`) based on confidence bands and dollar value thresholds, paired with citation-backed "Ask Why" justification graphs. |
| **Technical Implementation** | Design documentation & scoring script | **Full Executable Python Engine (`src/` & `run_pipeline.py`)**: Production-grade multi-agent runtime engine achieving **100% evaluation scores** on all test scenarios. |

---

## 🏆 Benchmark Evaluation Results

Our system was evaluated using the automated scoring harness (`evaluate_scenarios.py`) across all official practice scenarios, achieving **100% Perfect Accuracy**:

| Practice Scenario | Scenario ID & Narrative | Checkpoints Passed | Red Herring Isolation | Final Score |
|---|---|---|---|---|
| **Scenario 01** | `scenario_05_major_medical_event` (Marcus Vance - Medical Hardship) | 3 / 3 (100%) | Tuition wire (`EVT_000382`) & Resort refund (`EVT_000402`) isolated | **110.0 / 110.0 (100.0%)** |
| **Scenario 02** | `scenario_06_new_child` (Priya Sharma - New Child Life Event) | 2 / 2 (100%) | Baby monitor electronics spend (`EVT_000328`) isolated | **70.0 / 70.0 (100.0%)** |
| **Scenario 03** | `scenario_07_churn_risk` (David Chen - Churn Risk Withdrawal) | 3 / 3 (100%) | Tax refund deposit (`EVT_000447`) isolated | **100.0 / 100.0 (100.0%)** |

---

## 📂 Repository Structure

```
inter_iit_nlp_mid/
├── README.md                                   # Root Landing Page & Comprehensive Overview
├── endterm_submission/                         # END-TERM SUBMISSION DELIVERABLES
│   ├── ENDTERM_SUBMISSION.md                 # Central End-Term Index & User Guide
│   ├── 01_research_log.md                    # Research Log & Theoretical Grounding (30% Weight)
│   ├── 02_system_architecture.md             # Architecture Spec & Visual Mermaid Flowcharts (20% Weight)
│   ├── 03_solution_document.md               # 3-Page Solution Document (Hard Constraint!)
│   └── 04_testing_and_evaluation.md          # Benchmark Evaluation Report & Failure Mode Analysis
├── midterm_submission/                         # MID-TERM SUBMISSION ARCHIVE
│   ├── MIDTERM_SUBMISSION.md                 # Mid-Term Submission Index
│   ├── 01_preliminary_research_document.md     # Preliminary Research Document
│   ├── 02_preliminary_system_architecture.md   # Preliminary System Architecture Spec
│   └── 03_one_page_report.pdf                  # One-Page Executive Report (PDF)
├── src/                                      # PRODUCTION PYTHON ENGINE CODEBASE (25% Weight)
│   ├── stream_processor.py                   # Event-time watermarking & sliding window aggregations
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
├── customer_360_dataset/                      # DATASET SCENARIOS & SCHEMAS
│   ├── README_dataset_schema.md                # Event Schema & Output Enum Specifications
│   ├── scenario_01/                            # Scenario 01: Medical Hardship (Marcus Vance)
│   ├── scenario_02/                            # Scenario 02: New Child Life Event (Priya Sharma)
│   └── scenario_03/                            # Scenario 03: Churn Risk (David Chen)
├── run_pipeline.py                           # Command-Line End-to-End Pipeline Entrypoint
├── evaluate_scenarios.py                     # Benchmark Evaluation Harness
└── .gitignore
```

---

## 📑 Complete Deliverables Guide

### 1. End-Term Submission Deliverables (`endterm_submission/`)
- **[01_research_log.md](endterm_submission/01_research_log.md)**: Comprehensive reading log covering 10 arXiv papers (MemGPT, MetaGPT, DyLAN, Self-RAG, Guardrails AI, Calibrated HITL), 5 engineering blogs (Stripe, Uber Flink, Netflix, Databricks, DoorDash), 4 agent frameworks, and Event Stream Analysis (**30% Weight**).
- **[02_system_architecture.md](endterm_submission/02_system_architecture.md)**: Visual Mermaid Flowcharts, Event-Time Streaming Ingestion, Shared Per-Customer State Board, 3-Tiered Memory Architecture, Swarm + Debate + Refiner Topologies, and Safety Rails (**20% Weight**).
- **[03_solution_document.md](endterm_submission/03_solution_document.md)**: **Hard 3-Page Solution Document** covering problem overview (Page 1), architecture & topologies (Page 2), and benchmark evaluation, non-negotiables & trade-offs (Page 3).
- **[04_testing_and_evaluation.md](endterm_submission/04_testing_and_evaluation.md)**: Detailed testing methodology, red herring isolation, lead-time calibration, and benchmark score breakdown.
- **[ENDTERM_SUBMISSION.md](endterm_submission/ENDTERM_SUBMISSION.md)**: Central submission index document and quickstart guide.

### 2. Mid-Term Submission Archive (`midterm_submission/`)
- **[01_preliminary_research_document.md](midterm_submission/01_preliminary_research_document.md)**: Initial hyperlinked preliminary research log.
- **[02_preliminary_system_architecture.md](midterm_submission/02_preliminary_system_architecture.md)**: Preliminary system architecture specification.
- **[03_one_page_report.pdf](midterm_submission/03_one_page_report.pdf)**: One-Page Executive Progress Report (PDF).
- **[MIDTERM_SUBMISSION.md](midterm_submission/MIDTERM_SUBMISSION.md)**: Mid-Term index file.

---

## 🛠️ Quickstart & Execution Guide

### Prerequisite
Python 3.9+ installed. No external heavy dependencies required (uses native Python standard libraries & JSON execution).

### 1. Run End-to-End Pipeline Across All Scenarios
To process live streams and generate `inferred_events.json` outputs for all practice scenarios:

```bash
python run_pipeline.py
```

### 2. Run Pipeline on a Specific Scenario
```bash
python run_pipeline.py customer_360_dataset/scenario_01
```

### 3. Run Automated Evaluation Harness
To score generated predictions against ground truth benchmarks:

```bash
python evaluate_scenarios.py customer_360_dataset/scenario_01/ground_truth.json customer_360_dataset/scenario_01/inferred_events.json
```
