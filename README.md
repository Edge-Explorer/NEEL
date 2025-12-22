# 🧠 NEEL — A Self-Regulating Agentic AI Backend

NEEL is a **backend-first, agentic AI system** designed to analyze user behavior, reason cautiously, validate its own outputs, and correct itself before responding.

It is **not a chatbot**.  
It is **not a prompt experiment**.  
It is a **controlled, self-reviewing intelligence system**.

---

## 🔍 What Problem NEEL Solves

Most AI systems:
- Generate answers directly from models
- Trust LLM outputs blindly
- Lack validation, memory discipline, and safety enforcement

NEEL was built to answer a different question:

> **How can an AI system think, check itself, and respond responsibly?**

---

## 🧠 Core Philosophy

NEEL is designed around four principles:

1. **LLMs are not authorities**  
   They are reasoning components whose outputs must be reviewed.

2. **Control flow matters more than prompts**  
   Safety is enforced programmatically, not by instruction alone.

3. **Memory should support insight, not recall**  
   NEEL remembers patterns and summaries, not raw conversations.

4. **Uncertainty should be communicated honestly**  
   Confidence is contextual and explicitly managed.

---

## 🏗 High-Level Architecture

NEEL follows a layered, gated execution pipeline:
Analytics Engine
↓
ML Signal Layer
↓
Supervisor Agent (pre-reasoning gate)
↓
LLM Reasoning Agent
↓
Reflection Agent (post-reasoning review)
↓
Regeneration Loop (if needed)
↓
User Response


Every step has a **single responsibility** and **explicit constraints**.

---

## 🧩 System Components

### 1️⃣ Analytics Engine
- Aggregates raw user activity (time, habits, productivity)
- Computes interpretable metrics and trends
- Deterministic and explainable

📄 Documented in: `analytics_engine_overview.md`

---

### 2️⃣ Machine Learning Signal Layer
- Academic estimation models
- Habit clustering models
- Time balance scoring

Model outputs are used as **signals**, not final decisions.

📄 Documented in: `ml_models_overview.md`

---

### 3️⃣ Supervisor Agent (Pre-Reasoning Control)
- Validates data sufficiency and stability
- Detects conflicts in context
- Assigns confidence levels (LOW / MEDIUM / HIGH)
- Can block reasoning entirely

📄 Documented in: `supervisor_rules.md`

---

### 4️⃣ LLM Reasoning Agent
- Converts analytics and signals into human-readable explanations
- Produces cautious, non-prescriptive guidance
- Operates only if Supervisor allows

LLM output is treated as a **draft**, not a final answer.

📄 Documented in: `llm_reasoning_overview.md`

---

### 5️⃣ Reflection Agent (Post-Reasoning Review)
- Evaluates the LLM’s generated response
- Checks tone vs confidence alignment
- Detects overconfidence, unsafe phrasing, or misalignment
- Outputs: `PASS`, `SOFTEN`, or `REJECT`

This agent is **rule-based** for determinism and auditability.

📄 Documented in: `reflection_agent_overview.md`

---

### 6️⃣ Regeneration Loop (Self-Correction)
- Activated only when Reflection returns `SOFTEN`
- Forces the LLM to rewrite its response under stricter constraints
- Preserves usefulness while reducing risk

This completes NEEL’s **closed-loop intelligence system**.

📄 Documented in: `regeneration_loop.md`

---

### 7️⃣ Memory System
NEEL does **not** store raw conversations.

Memory types:
- **Profile Memory** — stable user identity and goals
- **Short-Term Memory** — recent summarized behavior
- **Reflective Memory** — detected patterns and trends

Memory is injected into every run.

> **LLMs do not remember users. Systems do.**

📄 Documented in: `architecture.md`

---

## 🔁 Execution Orchestration

NEEL uses **LangGraph** to:
- Enforce execution order
- Apply conditional routing
- Prevent unsafe reasoning paths
- Guarantee reflection before user exposure

Prompt discipline is supported by **hard control flow**, not trust.

---

## ⚠️ Failure-Aware Design

NEEL explicitly models failure instead of ignoring it.

Handled failure modes include:
- LLM hallucination
- Overconfidence under low certainty
- Goal or priority misalignment
- Unsafe prescriptive advice
- Data insufficiency
- Compounding memory errors

📄 Documented in: `failure_modes.md`

---


---

## 🧪 Current Status

- ✅ Backend intelligence pipeline complete
- ✅ Agentic control fully enforced
- ✅ Self-review and self-correction implemented
- ⏳ API layer (planned)
- ⏳ Frontend integration (planned)

---

## 🎯 Why NEEL Is Different

Most projects demonstrate:
- Model accuracy
- Prompt creativity

NEEL demonstrates:
- **Judgment**
- **Restraint**
- **Self-correction**
- **System-level thinking**

This project focuses on **how AI should behave**, not just what it can generate.

---

## 👤 Author

**Karan Shelar**  
ML / AI Engineer (Backend-Focused)

This project was built to explore:
- Responsible AI design
- Agentic systems
- Safety-aware reasoning architectures

---

## 📌 Final Note

NEEL is intentionally backend-only at this stage.  
Frontend, database, and deployment layers will be added **after** the intelligence system is complete.

> *A system that thinks without checking itself is incomplete.*

**NEEL checks itself.**
