# Inter IIT Tech Meet 15.0 Prepathon — End-Term Submission
**Problem Statement**: Agentic Customer 360 — Proactive Intervention Desk  
**Track**: Natural Language Processing (NLP)  
**Author**: Om Mishra | Electronics Engineering (3rd Year), IIT (BHU) Varanasi | Roll No.: 24095073  
**Framework**: `ACT-TREE 360` (Actor-Critic Blackboard Swarm with Dynamic Life-Phase Hypothesis Trees)  
**GitHub Repository**: https://github.com/0mM1shra/inter_iit_nlp_mid  

---

## 📌 End-Term Submission Deliverables Index

This directory contains the complete set of required deliverables for the **End-Term Submission** as outlined in Section 7 & Section 9 of the Problem Statement:

| Deliverable # | Document Name | Description & Key Focus | Link to File |
|---|---|---|---|
| **01** | **Research Log & Literature Grounding** | Grounded in 10 arXiv papers (MemGPT, MetaGPT, DyLAN, Self-RAG, Guardrails AI, Calibrated HITL), 5 engineering blogs (Stripe, Uber Flink, Netflix, Databricks, DoorDash), 4 frameworks, and Event Stream Analysis. Weighs 30% of total score. | [01_research_log.md](file:///c:/Users/DELL/Documents/Inter%20IIT/NLP/endterm_submission/01_research_log.md) |
| **02** | **System Architecture Specification** | Detailed visual Mermaid flowchart & text specification covering Event-Time Streaming Ingestion, Shared Per-Customer State Board, Tiered Memory, Hybrid MAS Topology (Swarm + Debate + Refiner), Non-Negotiable Guardrails, and HITL Checkpoints. | [02_system_architecture.md](file:///c:/Users/DELL/Documents/Inter%20IIT/NLP/endterm_submission/02_system_architecture.md) |
| **03** | **Solution Document (3 Pages)** | Hard 3-page solution document explaining problem overview (Page 1), architecture & MAS topologies (Page 2), and benchmark evaluation results, non-negotiables & trade-offs (Page 3). | [03_solution_document.md](file:///c:/Users/DELL/Documents/Inter%20IIT/NLP/endterm_submission/03_solution_document.md) |
| **04** | **Testing & Evaluation Report** | Automated evaluation results against all test scenarios showing 100% accuracy, red herring isolation, and lead time calibration. | [04_testing_and_evaluation.md](file:///c:/Users/DELL/Documents/Inter%20IIT/NLP/endterm_submission/04_testing_and_evaluation.md) |
| **Codebase Engine** | **`run_pipeline.py` & `src/`** | Fully working Python engine running swarm agents, state board, hypothesis tree synthesis, actor-critic debate, guardrails, and HITL routing. | [`run_pipeline.py`](file:///c:/Users/DELL/Documents/Inter%20IIT/NLP/run_pipeline.py) |

---

## 🚀 Quickstart: Running the Codebase Engine

Execute the full pipeline across all practice scenarios:

```bash
python run_pipeline.py
```

Execute on a specific scenario:

```bash
python run_pipeline.py customer_360_dataset/scenario_01
```

Run automated evaluation harness:

```bash
python evaluate_scenarios.py customer_360_dataset/scenario_01/ground_truth.json customer_360_dataset/scenario_01/inferred_events.json
```
