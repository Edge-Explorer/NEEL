# Supervisor Layer — NEEL

This document describes the design, purpose, and behavior of the **Supervisor Layer** in NEEL.

The Supervisor acts as a **gatekeeper** between data/ML signals and LLM reasoning.  
It ensures that AI responses are **safe, contextual, and responsible** before any advice or explanation is generated.

---

## Why a Supervisor Layer Exists

Most AI assistants directly generate responses from an LLM.  
NEEL intentionally avoids this pattern.

Reasons:
- Behavioral data is incomplete and noisy
- ML predictions are probabilistic, not absolute
- User goals and mental states vary over time
- Blind confidence can cause harmful suggestions

The Supervisor ensures that NEEL:
- Knows when it is safe to respond
- Knows when to be cautious
- Knows when not to respond at all

---

## Supervisor Responsibilities

The Supervisor performs **pre-reasoning validation** and does not generate advice itself.

Its responsibilities are limited to:

1. **Profile Completeness Validation**
2. **Risk Signal Detection**
3. **Conflict Detection**
4. **Confidence Assignment**
5. **Reasoning Authorization**

This strict scope prevents overreach and keeps the system interpretable.

---

## Inputs to the Supervisor

The Supervisor operates on structured inputs only:

### User Profile
- Long-term goals (e.g., career, education)
- Contextual metadata (e.g., known days of activity)

### Analytics Summary
- Aggregated time usage
- Productivity trends
- Recovery indicators

### ML Signals
- Directional predictions (e.g., unstable routine)
- Risk indicators (not final decisions)

### User Feedback
- Subjective signals (e.g., fatigue, stress)

The Supervisor does **not** consume raw chat history or authentication data.

---

## Validation Rules Implemented

### 1. Profile Completeness Check
- Blocks reasoning if goals are unknown
- Blocks reasoning if insufficient historical data exists

### 2. Risk Detection
- Flags low sleep or unstable productivity patterns
- Identifies conditions that require cautious advice

### 3. Conflict Detection
- Detects contradictions between objective metrics and subjective feedback
- Example: High productivity metrics but reported fatigue

---

## Supervisor Decision Output

The Supervisor outputs a structured decision:

```json
{
  "status": "ALLOW | BLOCK",
  "confidence": "LOW | MEDIUM | HIGH",
  "warnings": ["list of detected issues"]
}

## Relationship with Reflection Layer

The Supervisor governs whether reasoning may begin.

It does not evaluate the final wording or tone of LLM outputs.
That responsibility belongs to the Reflection Agent.

This separation ensures:
- Supervisor controls safety of reasoning
- Reflection controls safety of expression

