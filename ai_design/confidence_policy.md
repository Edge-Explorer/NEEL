# Confidence Policy — NEEL

This document defines how **confidence** is represented, interpreted, and enforced across NEEL’s backend.

Confidence in NEEL is a **system-level concept**, not a probability score or a measure of correctness.

---

## 1. What Confidence Means in NEEL

Confidence represents the **system’s trust in the stability and sufficiency of context**, not the truth of a prediction.

It answers the question:
> “How safely can the system reason and suggest actions right now?”

Confidence does **not** measure:
- Model accuracy
- Prediction certainty
- User correctness

---

## 2. Why Confidence Is Explicitly Modeled

Most AI systems hide uncertainty.

NEEL explicitly models it to:
- Prevent overconfident advice
- Communicate limitations honestly
- Adjust tone and behavior dynamically
- Enable safe refusal when necessary

Confidence is treated as a **first-class control signal**.

---

## 3. Confidence Levels

NEEL uses three semantic confidence levels:

### LOW Confidence
Indicates:
- Insufficient historical data
- Conflicting signals
- High uncertainty

System behavior:
- Reasoning may be blocked
- Language must be cautious
- Explicit uncertainty must be stated
- No strong suggestions
- Emoji usage is discouraged or neutral only

---

### MEDIUM Confidence
Indicates:
- Partial data availability
- Mild inconsistencies
- Reasonable but incomplete context

System behavior:
- Exploratory reasoning allowed
- Suggestions must be reversible
- Balanced tone
- Light stylistic warmth permitted

---

### HIGH Confidence
Indicates:
- Stable patterns
- Sufficient historical context
- Low signal conflict

System behavior:
- Clear explanations allowed
- Still non-prescriptive
- Calm and confident tone
- Optional stylistic enhancements permitted

---

## 4. Components Governed by Confidence

Confidence affects multiple backend components:

- **Supervisor**: decides confidence level
- **LLM Reasoning**: adapts tone and structure
- **Suggestion Strength**: limits prescriptiveness
- **Stylistic Expression**: controls emoji usage
- **Response Framing**: enforces humility

No component may override confidence rules.

---

## 5. What Confidence Is NOT

Confidence is not:
- A probability score
- A numeric metric exposed to users
- A measure of user success or failure
- A replacement for validation logic

Confidence exists to protect **user trust**, not system ego.

---

## 6. Design Principle

NEEL follows this principle:

> **When confidence is low, the system speaks less — and more carefully.**

This principle is enforced consistently across the backend.

---

## 7. Summary

Confidence in NEEL is a behavioral control mechanism.

By making confidence explicit, NEEL:
- Avoids false authority
- Encourages reflective interaction
- Maintains long-term credibility

This policy ensures that intelligence in NEEL is expressed with responsibility.
