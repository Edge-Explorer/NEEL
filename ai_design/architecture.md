# NEEL — Backend Architecture Overview

## 1. System Philosophy

NEEL is designed as a **self-regulating, agentic backend system**, not a conversational chatbot.

Core principles:
- Deterministic control over reasoning flow
- Explicit separation of intelligence responsibilities
- Safety-first decision making
- Memory-driven personalization
- No blind trust in LLM outputs

The system treats Large Language Models as **reasoning components**, not authorities.

---

## 2. High-Level Architecture

NEEL follows a layered, gated architecture:

Analytics Engine  
↓  
ML Signal Layer  
↓  
Supervisor Agent (Pre-Reasoning Gate)  
↓  
LLM Reasoning Agent  
↓  
Reflection Agent (Post-Reasoning Gate)  
↓  
Regeneration Loop (If Required)  
↓  
User Response

Each layer has a **single responsibility** and **explicit input/output contracts**.

---

## 3. Core Architectural Components

### 3.1 Analytics Engine
- Aggregates raw user activity into interpretable metrics
- Computes averages, ratios, trends, and summaries
- Produces deterministic, explainable outputs
- Does not perform prediction or inference

Purpose:
Provide structured context for downstream intelligence layers.

---

### 3.2 ML Signal Layer
- Uses trained ML models for:
  - Academic performance estimation
  - Habit clustering
  - Time balance scoring
- Outputs **signals**, not decisions
- Model outputs are never shown directly to the user

Purpose:
Provide probabilistic indicators, not prescriptions.

---

### 3.3 Supervisor Agent (Pre-Reasoning Control)

Responsibilities:
- Validate sufficiency and stability of data
- Detect conflicts or unreliable contexts
- Assign confidence levels (LOW / MEDIUM / HIGH)
- Decide whether LLM reasoning is allowed

Key property:
The Supervisor can **block reasoning entirely**.

---

### 3.4 LLM Reasoning Agent

Responsibilities:
- Convert analytics and ML signals into human-readable explanations
- Provide cautious, non-prescriptive guidance
- Respect confidence and safety constraints

Constraints:
- Cannot access raw data
- Cannot see ML model internals
- Cannot bypass Supervisor decisions

LLM output is treated as a **draft**, not a final answer.

---

### 3.5 Reflection Agent (Post-Reasoning Control)

Responsibilities:
- Evaluate the LLM’s generated response
- Check tone vs confidence alignment
- Detect overconfidence, unsafe phrasing, or goal misalignment
- Decide PASS / SOFTEN / REJECT

Design choice:
Rule-based, deterministic evaluation for auditability and safety.

---

### 3.6 Regeneration Loop

Activated when:
- Reflection decision = SOFTEN

Responsibilities:
- Rewrite the LLM response using stricter constraints
- Reduce prescriptive language
- Preserve original scope without introducing new advice

The regeneration loop allows NEEL to **self-correct instead of failing silently**.

---

## 4. Memory Architecture

NEEL does not store raw conversations as memory.

Memory types:
- Short-Term Memory: recent aggregated behavior
- Reflective Memory: detected patterns and trends
- Profile Memory: stable user attributes (goals, priorities)

Memory is:
- Structured
- Summarized
- Re-injected on every agent execution

Principle:
LLMs do not remember users — systems do.

---

## 5. Execution Orchestration

NEEL uses LangGraph to:
- Enforce execution order
- Apply conditional routing
- Prevent unauthorized reasoning paths
- Guarantee reflection before user exposure

Prompt discipline is supported by **hard control flow**, not trust.

---

## 6. Architectural Differentiators

What makes NEEL different:
- Pre- and post-reasoning validation
- Self-correcting intelligence loop
- Confidence-aware language control
- Explicit separation of reasoning and evaluation
- Deterministic safety enforcement

This architecture mirrors real-world, production-grade AI systems.

---

## 7. Scope Boundaries

Intentionally excluded from this layer:
- Frontend/UI concerns
- Authentication implementation details
- Database schema specifics
- Cloud deployment strategies

This document focuses strictly on **backend intelligence architecture**.
