# Agent Roles — NEEL

This document defines the **agent roles and responsibilities** within NEEL’s backend architecture.

NEEL is designed as a **multi-agent reasoning system**, where each agent has a clearly bounded role.  
No single agent has full authority over reasoning or decision-making.

This separation ensures:
- Safety
- Explainability
- Predictable behavior
- Maintainability

---

## 1. Why Agent Roles Are Explicitly Defined

Many AI systems blur responsibilities by treating the LLM as a monolithic agent.

NEEL intentionally avoids this.

By defining explicit agent roles:
- Each component has a single responsibility
- Failures are isolated
- Reasoning remains auditable
- The system behaves consistently under uncertainty

Agent roles in NEEL are **logical roles**, not necessarily separate services.

---

## 2. Core Agent Roles in NEEL

NEEL currently defines the following backend agent roles:

---

### 2.1 Analytics Agent

**Primary Responsibility:**  
Transform raw behavioral data into interpretable summaries.

**Responsibilities:**
- Aggregate time-based activity data
- Compute trends and distributions
- Produce human-interpretable metrics

**Constraints:**
- Does not predict outcomes
- Does not make decisions
- Does not reason or suggest actions

**Outputs:**
- Analytics summaries
- Time distributions
- Trend indicators

---

### 2.2 ML Signal Agent

**Primary Responsibility:**  
Generate directional signals from historical data.

**Responsibilities:**
- Produce habit stability indicators
- Identify productivity trends
- Detect behavioral clusters

**Constraints:**
- Outputs are probabilistic and directional
- Signals are never exposed directly to users
- Does not provide explanations

**Outputs:**
- Risk indicators
- Stability classifications
- Behavioral signals

---

### 2.3 Supervisor Agent

**Primary Responsibility:**  
Validate whether reasoning is safe and appropriate.

**Responsibilities:**
- Validate profile completeness
- Check data sufficiency
- Detect conflicts between signals
- Assign confidence levels
- Allow or block LLM reasoning

**Constraints:**
- Never generates advice
- Never optimizes metrics
- Never interacts with the user directly

**Outputs:**
- Reasoning authorization (ALLOW / BLOCK)
- Confidence level
- Warning list

The Supervisor has **veto power** over all downstream reasoning.

---

### 2.4 LLM Reasoning Agent

**Primary Responsibility:**  
Explain validated signals in natural language.

**Responsibilities:**
- Translate analytics into observations
- Reflect on patterns cautiously
- Suggest small, reversible actions
- Communicate uncertainty explicitly

**Constraints:**
- Must respect Supervisor decisions
- Cannot see raw ML outputs
- Cannot give absolute or medical advice
- Cannot override confidence policy

**Outputs:**
- Structured, explainable responses

---

### 2.5 Memory Agent (Planned)

**Primary Responsibility:**  
Manage user context and behavioral memory.

**Responsibilities:**
- Summarize session history
- Maintain short-term and long-term memory
- Filter noise from raw interactions

**Constraints:**
- Does not reason
- Does not suggest
- Does not store raw conversations blindly

**Outputs:**
- Structured memory summaries
- Context payloads for reasoning

---

## 3. Agent Interaction Model

Agents interact in a **strict, unidirectional flow**:
Analytics Agent
↓
ML Signal Agent
↓
Supervisor Agent
↓
LLM Reasoning Agent


No agent may bypass another agent’s responsibility.

---

## 4. Why This Design Is Important

This agent separation ensures:
- No single point of overconfidence
- Clear accountability
- Safer AI behavior
- Easier debugging and extension

Most AI projects merge these roles implicitly.  
NEEL makes them **explicit and enforceable**.

---

## 5. Design Principle

NEEL follows this rule:

> **Agents may inform downstream agents, but may never command them.**

This keeps the system cooperative rather than hierarchical.

---

## 6. Future Extensibility

This architecture allows future additions such as:
- Reflection agents
- Planning agents
- Evaluation agents

Without changing existing agent contracts.

---

## 7. Summary

NEEL’s backend is designed as a **collaboration of specialized agents**, each with a narrow and well-defined role.

This approach prioritizes:
- Safety
- Explainability
- Trust
- Long-term maintainability

Agent roles are foundational to NEEL’s agentic intelligence.

### 2.6 Reflection Agent

Primary Responsibility:
Evaluate the LLM’s generated response before it is shown to the user.

Responsibilities:
- Check tone vs confidence alignment
- Detect overconfident or unsafe phrasing
- Validate alignment with user goals and priorities
- Decide PASS / SOFTEN / REJECT

Constraints:
- Does not generate new advice
- Does not access raw data or ML outputs
- Does not interact with user directly

Outputs:
- Reflection decision
- List of detected issues

### 2.7 Regeneration Agent

Primary Responsibility:
Safely rewrite LLM responses when Reflection flags issues.

Responsibilities:
- Rewrite responses using stricter constraints
- Reduce prescriptiveness and overconfidence
- Preserve usefulness without violating safety

Constraints:
- Activated only when Reflection decision is SOFTEN
- Cannot introduce new advice
- Must respect original scope and confidence level

Outputs:
- Revised LLM response
