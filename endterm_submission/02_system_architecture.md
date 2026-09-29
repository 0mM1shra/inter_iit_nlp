# End-Term System Architecture Specification (`ACT-TREE 360`)
**Framework**: Actor-Critic Blackboard Swarm with Dynamic Life-Phase Hypothesis Trees  
**Event**: Inter IIT Tech Meet 15.0 Prepathon (NLP Track)  
**Author**: Om Mishra | Electronics Engineering (3rd Year), IIT (BHU) Varanasi | Roll No.: 24095073  

---

## 1. High-Level Architecture Overview

The **`ACT-TREE 360`** system architecture transforms raw, asynchronous, multi-modal streaming data into real-time customer state inferences and targeted, safe enterprise interventions. The system operates on an **Ambient, Event-Driven Multi-Agent System (MAS)** model backed by a **Shared Per-Customer State Board** and a **3-Tier Memory Architecture**.

### Architecture Diagram

```mermaid
flowchart TD
    subgraph Data_Ingestion ["1. Streaming Ingestion Layer (Async)"]
        Stream[Live Multi-Source Event Stream\ncard, ach, core_banking, web_app, support, kyc]
        TimeWatermark[Event-Time Watermark &\nOut-of-Order Queue]
        WindowAgg[Windowed Feature Aggregator\n30d login trends, spend baselines, anomaly scores]
        Stream --> TimeWatermark --> WindowAgg
    end

    subgraph Memory_Layer ["2. Per-Customer State & Memory Architecture"]
        StateBoard[Shared Per-Customer State Board\nStructured reads: login_trend, spend_anomaly, sentiment]
        EpisodicDB[(Episodic Memory DB\nPer-customer chronological interventions & outcomes)]
        SemanticDB[(Semantic Knowledge Base\nEligibility rules, compliance policies, pre-churn models)]
        WorkingMem[Working Memory\nActive session state & open ticket context]
    end

    subgraph Swarm_Layer ["3. Domain Specialist Agent Swarm (Parallel / Async)"]
        UsageAgent[Usage/Engagement Agent\nTool: Session Analytics, Login Frequency]
        SupportAgent[Support/Sentiment Agent\nTool: Transcript NLP, Urgency Classifier]
        TxnAgent[Transaction/Billing Agent\nTool: Spend Anomaly Score, Merchant MCC Query]
        KYCAgent[KYC/Compliance Agent\nTool: Watchlist Match, KYC Update DB]

        WindowAgg --> UsageAgent & SupportAgent & TxnAgent & KYCAgent
        UsageAgent & SupportAgent & TxnAgent & KYCAgent -->|Publish structured reads| StateBoard
    end

    subgraph Guardrail_FastPath ["4. Emergency Guardrail Engine (Sync / Fast-Path)"]
        Guardrail[Escalation/Guardrail Agent\nHard-coded keyword/regex scanner]
        Stream -->|Real-time scan| Guardrail
        Guardrail -->|Legal Threat / Self-Harm / Fraud Spike| LegalQueue[Legal/Fraud Escalation Queue]
    end

    subgraph Coordination_Layer ["5. Decision Synthesis & Coordination Layer"]
        DerivedTrigger{Derived Trigger\n2+ Swarm Anomalies Flagged?}
        StateBoard --> DerivedTrigger
        DerivedTrigger -->|Yes| SynthesisAgent[Synthesis & Correlation Agent\nInfers customer state & life event]
        
        ConflictCheck{Swarm Disagreement?}
        SynthesisAgent --> ConflictCheck
        ConflictCheck -->|Yes| DebateLayer[Multi-Agent Debate\nActor-Critic Adversarial Audit]
        DebateLayer --> FinalState[Reconciled Inferred State & Confidence Band]
        ConflictCheck -->|No| FinalState
    end

    subgraph Action_Pipeline ["6. Action & Refinement Pipeline"]
        OfferAgent[Offer / Eligibility Agent\nTool: Policy RAG, Offer Matrix]
        ActionAgent[Retention / Action Agent\nTool: LLM Message Composer, CRM Grounding]
        RefinerAgent[Critique / Compliance Refiner\nTool: Guardrail Checker, Cost Estimator]

        FinalState --> OfferAgent --> ActionAgent --> RefinerAgent
        RefinerAgent --> HITLCheck{HITL Checkpoint\nConfidence & Budget Thresholds}
    end

    subgraph HITL_Layer ["7. Human-in-the-Loop & Execution (Sync Checkpoint)"]
        HITLCheck -->|Auto-Approved| ExecEngine[Action Execution Engine]
        HITLCheck -->|Escalated| Dashboard[Human Approver Dashboard\nIncludes 'Ask Why' Citation Trace]
        Dashboard -->|Approve/Modify/Reject| AuditLog[(Audit Log DB)]
        ExecEngine --> AuditLog
        AuditLog -->|Update outcomes| EpisodicDB
    end
```

---

## 2. Component Specifications & Agent Rosters

### 2.1 Domain Specialist Swarm Agents (Parallel Execution)

| Agent Name | Monitored Data / Signals | Toolset & Data Source Access | Trigger Type | Output Written to State Board |
|---|---|---|---|---|
| **Usage / Engagement Agent** | App/web login frequency, feature drop-off, session length trends | `query_telemetry_db`, `compute_rolling_login_avg` | Event-based (login event) + Time-based (daily rollup) | `login_frequency_trend` (-40%), `app_engagement_score` |
| **Support / Sentiment Agent** | Support tickets, chat transcripts, call summaries | `sentiment_classifier`, `urgency_scanner`, `ticket_history_db` | Event-based (new ticket/message) | `sentiment_score` (-0.82), `unresolved_complaint_flag` |
| **Transaction / Billing Agent** | Payments, ACH/wire transfers, credit card spending, merchant MCCs | `txn_anomaly_scorer`, `historical_baseline_query` | Event-based (transaction stream) | `spend_anomaly_score`, `large_outbound_transfer_flag` |
| **KYC / Compliance Agent** | Address changes, marital status, dependents update, sanctions matches | `kyc_database_query`, `watchlist_lookup` | Event-based (KYC update) + Time-based (quarterly) | `dependents_change_flag`, `kyc_status` |

---

### 2.2 Core Synthesis & Action Agents

| Agent Name | Responsibilities | Toolset & Inputs | Trigger Type | Output Package |
|---|---|---|---|---|
| **Synthesis / Correlation Agent** | Reconciles swarm signals from State Board; infers customer life event & state | State Board reader, Episodic RAG retriever | Agent-dependent (fires when 2+ swarm signals trigger) | `inferred_state`, `confidence_band` (`low`/`medium`/`high`) |
| **Actor-Critic Debate Agent** | Audits state hypothesis against counterfactual red-herring rules | Counterfactual rules, State Board reader | Agent-dependent (fires on swarm contradiction) | Reconciled state & confidence band |
| **Offer / Eligibility Agent** | Verifies eligibility for loans, credit limits, fee waivers, payment plans | `policy_rag_query`, `eligibility_calculator` | Agent-dependent (fires post-Synthesis) | `eligible_action_subtypes`, `max_value_cap` |
| **Retention / Action Agent** | Decides specific intervention & drafts outreach message or escalation brief | `llm_message_composer`, `crm_record_grounding` | Agent-dependent (fires post-Offer) | Drafted action proposal (`action`, `action_subtype`) |
| **Critique / Compliance Refiner** | Audits proposal for tone, compliance, cost feasibility, and policy adherence | `policy_guardrail_checker`, `cost_estimator` | Agent-dependent (fires post-Action Agent draft) | Reviewed & refined action proposal or rejection back-step |

---

### 2.3 Non-Negotiable Safety & Guardrail Agents

| Agent Name | Responsibilities | Implementation Mechanism | Trigger Type | Action |
|---|---|---|---|---|
| **Escalation / Guardrail Agent** | Hard-stop condition scanner (legal threats, legal terms, AML spikes) | Deterministic regex/keyword scanner & strict rule bypass | Event-based (instant stream bypass) | Halts pipeline, sets `action = compliance_fraud_hold`, routes to legal |

---

## 3. Memory Architecture Details

### 3.1 Tier 1: Working Memory (Short-Term Session State)
- **Scope**: Ephemeral, single-customer active session context (e.g., active support ticket text, recent 3 logins).
- **Lifecycle**: Discarded or compressed once the current event sequence resolves.

### 3.2 Tier 2: Episodic Memory (Long-Term Per-Customer Log)
- **Scope**: Running history of past interventions, flags, and outcomes for this specific customer.
- **Storage**: Vector index + relational metadata table (`customer_id`, `timestamp`, `event_summary`, `intervention_taken`, `customer_response`).
- **Retrieval**: Weighted decay formula: $Score = \alpha \cdot \text{Recency} + \beta \cdot \text{Importance} + \gamma \cdot \text{Relevance}$.
- **Decay Policy**: Events older than 12 months are aggregated into a static profile summary unless explicitly flagged as a major life event baseline.

### 3.3 Tier 3: Semantic Memory (Cross-Customer & Policy Knowledge Base)
- **Scope**: Product rules, eligibility limits, pre-churn behavioral archetypes, regulatory guidelines.
- **Access**: Read-only for all agents via Policy RAG.

### 3.4 Shared Per-Customer State Board
- **Pattern**: Structured key-value blackboard scoped strictly to `customer_id`.
- **Purpose**: Prevents context pollution. Swarm agents write *structured findings* (e.g., `login_trend: -40%`), NOT raw chain-of-thought traces. Downstream Synthesis Agent reads all published key-values to build state.

---

## 4. Non-Negotiable System Features

### 4.1 Explainability as a First-Class Output
Every action decision emitted by the system includes a structured `explanation` object:
```json
{
  "cited_signal_events": ["EVT_000392", "EVT_000406", "EVT_000444"],
  "retrieved_episodic_context": "Customer had ER visit on Feb 2 followed by disability income reduction on Feb 24.",
  "policy_rule_cited": "POL_MED_HARDSHIP_04: High-value customer with medical income disruption eligible for 6-month payment plan.",
  "reasoning_summary": "Sustained medical spending combined with reduced disability income and explicit support ticket justifies medical hardship payment plan."
}
```

### 4.2 Traceability & Audit Trail
Every agent execution emits an OpenTelemetry-compatible span:
- `trace_id`: Unique identifier per customer evaluation session.
- `span_id`, `agent_name`, `input_state_board_snapshot`, `prompt_template_version`, `tool_calls`, `output_json`.

### 4.3 Deterministic Guardrails & PII Security
- **Hard-Stop Conditions**: Keywords (`"lawsuit"`, `"attorney"`, `"legal action"`) trigger an immediate pipeline halt and route to legal.
- **PII Redaction**: Data-layer masking strips SSNs, full credit card numbers, and raw phone numbers before generating LLM prompt contexts.
- **Safe Blast Radii**: Autonomous agents can only *draft* proposals; execute/send actions require HITL approval or auto-approval within predefined low-risk policy thresholds.
