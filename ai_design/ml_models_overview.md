# ML Models Overview — NEEL

This document explains the purpose, design choices, and scope of the machine learning models implemented in **Notebook 05**.

The goal of these models is **not automated decision-making**, but **behavioral signal extraction** to support reasoning, analytics, and supervision.

---

## Design Philosophy

NEEL treats machine learning as a **signal generator**, not as an authority.

Key principles:
- Models must be interpretable
- Outputs must be explainable to a human
- ML predictions are never final decisions
- Final reasoning happens after validation and supervision

As a result, complex models and aggressive metric optimization are intentionally avoided.

---

## Models Implemented

### 1. Productivity Regression Model

**Objective:**  
Understand how time distribution and routine stability relate to productivity.

**Input Features:**
- Work ratio
- Leisure ratio
- Health ratio
- Routine variability

**Target:**
- Productivity score

**Model Used:**
- Linear Regression

**Rationale:**
- Captures directional relationships
- Easy to explain (e.g., more leisure → lower productivity)
- Stable across small datasets

---

### 2. Academic Performance Model

**Objective:**  
Estimate whether academic effort aligns with performance outcomes.

**Input Features:**
- Study minutes per week
- Attendance percentage
- Assignments completed

**Target:**
- Exam score

**Model Used:**
- Linear Regression

**Rationale:**
- Academic performance is modeled as a function of effort
- Linear relationships are sufficient and interpretable
- Supports reasoning such as “effort is sufficient / insufficient”

---

### 3. Habit Risk Classification Model

**Objective:**  
Identify potentially risky habit patterns.

**Input Features:**
- Distraction load
- Recovery score
- Time management score

**Target:**
- Binary habit risk label (heuristically derived)

**Model Used:**
- Logistic Regression

**Rationale:**
- Produces probabilistic risk signals
- Simple, transparent decision boundary
- Final validation handled by supervisor layer

---

### 4. Routine Behavior Clustering

**Objective:**  
Group users into routine archetypes.

**Input Features:**
- Work minutes
- Leisure minutes
- Exercise minutes
- Sleep minutes

**Model Used:**
- KMeans Clustering

**Rationale:**
- No ground-truth labels exist for routines
- Clustering reveals natural behavior patterns
- Clusters are later labeled descriptively (e.g., balanced, overworked)

---

## Evaluation Strategy

Traditional metrics such as accuracy, recall, and F1-score are intentionally **not emphasized**.

Instead, models are validated on:
- Stability of predictions
- Directional correctness
- Interpretability
- Consistency with human intuition

This aligns with NEEL’s role as a **decision-support system**, not an automated decision-maker.

---

## Artifacts Saved

All trained models are serialized and stored for backend inference:
- `productivity_model.pkl`
- `study_performance_model.pkl`
- `habit_risk_model.pkl`
- `routine_cluster_model.pkl`

Encoders and scalers are not saved at this stage, as current models operate on interpretable numeric features.

---

## Summary

Notebook 05 establishes a reliable ML foundation for NEEL by:
- Using conservative, interpretable models
- Avoiding overfitting and metric obsession
- Producing signals suitable for supervision and reasoning

These models enable NEEL to **understand patterns**, not to dictate actions.
