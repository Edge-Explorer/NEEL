# Data Selection Rationale for NEEL

This document explains:
- Why a subset of datasets was explored initially
- What role each dataset plays in NEEL’s ML lifecycle
- When and how remaining datasets are used

The goal is to avoid redundant exploration while ensuring full behavioral coverage.

## Core Principle

NEEL is a behavioral analysis system, not a dataset-driven ML demo.

Datasets are selected based on the *signals they provide*, not their quantity.
Once the complete behavioral signal space is identified, additional datasets are deferred to later stages.

## Datasets Explored in Initial Analysis

The following datasets were explored in Notebook 01:

1. Student Study Habits  
2. Enhanced Student Habits & Performance  
3. Time Management & Productivity Insights  

These datasets were chosen because together they cover:
- Academic effort
- Leisure and distraction
- Health and recovery
- Time allocation
- Productivity outcomes

## Datasets Deferred from Initial Exploration

The following datasets were intentionally not explored in Notebook 01:

- Cleaned Students Performance  
- Extended Employee Performance and Productivity  
- 2 Year Dataset  
- Samples Dataset  

These datasets do not introduce new behavioral signals.  
Instead, they provide:
- Outcome-only views
- Domain variations
- Longitudinal extensions
- Pipeline testing data

## Planned Usage of Deferred Datasets

- Cleaned Students Performance  
  Used for validating correlations between habits and outcomes.

- Extended Employee Performance and Productivity  
  Used for stress-testing analytics and generalization checks.

- 2 Year Dataset  
  Used after schema finalization for long-term (monthly/yearly) trend analysis.

- Samples Dataset  
  Used exclusively for testing and debugging the data pipeline.

## Final Note

This phased data usage approach prevents premature optimization,
keeps exploration focused,
and ensures that schema design is driven by behavior, not data volume.