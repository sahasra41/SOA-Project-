# AgentTwinDefect AI: An Agentic Digital Twin Platform for Real-Time Hidden Defect Prediction in Smart Manufacturing

An AI-enabled **Digital Twin and machine-failure prediction platform** for predicting machine failure risk, simulating possible parameter changes, and supporting corrective decisions.

---

## Overview

**AgentTwinDefect AI** is a smart manufacturing platform that combines **Machine Learning, Digital Twin simulation, scenario analysis, and agentic decision support**.

The system uses the **AI4I 2020 Predictive Maintenance Dataset** to analyze machine operating conditions such as temperature, rotational speed, torque, and tool wear.

Instead of stopping at machine-failure prediction, the platform performs **what-if simulations** using a Digital Twin and evaluates possible corrective actions through an agentic decision layer.

---

## Problem Statement

Modern manufacturing machines continuously generate operating data.

Machine-learning models can predict whether a machine is likely to fail, but prediction alone does not answer:

> **What should be done after detecting the failure risk?**

AgentTwinDefect AI addresses this problem by connecting machine-failure prediction, Digital Twin simulation, scenario comparison, and agentic decision support.

---

## Objectives

- Predict machine failure using operating-condition data.
- Estimate machine failure probability and risk level.
- Represent the machine condition using a Digital Twin.
- Perform virtual what-if simulations.
- Compare possible machine-parameter changes.
- Generate an appropriate corrective-action recommendation.
- Provide continuous monitoring through a Streamlit dashboard.

---

## Proposed Solution

### 1. Machine Failure Prediction

A **Random Forest Classifier** analyzes machine operating parameters and predicts machine failure probability.

### 2. Digital Twin

The current machine condition is represented as a virtual machine state.

### 3. What-if Simulation

The Digital Twin evaluates possible changes to machine parameters such as:

- Air temperature
- Process temperature
- Rotational speed
- Torque

### 4. Scenario Comparison

Candidate scenarios are compared using failure risk, risk reduction, adjustment cost, and parameter constraints.

### 5. Agentic Decision

The agent evaluates the scenario results and produces:

```text
RECOMMEND
ESCALATE
NO_ACTION_NEEDED
System Workflow
AI4I Dataset
     ↓
Data Loader
     ↓
Random Forest
     ↓
Failure Risk
     ↓
Digital Twin
     ↓
What-if Scenarios
     ↓
Scenario Comparison
     ↓
Agent
     ↓
Streamlit Dashboard
Workflow Explanation
Machine-condition data is loaded from the AI4I dataset.
The data is validated and the required features are extracted.
Random Forest predicts machine failure and failure probability.
The current machine condition is represented in the Digital Twin.
Different machine-parameter changes are simulated virtually.
The scenarios are compared based on predicted risk and constraints.
The agent selects an appropriate decision.
The dashboard displays the machine condition and decision.
Workflow Summary

Load → Predict → Simulate → Compare → Decide → Monitor

Key Features
Machine failure prediction
Failure probability estimation
Digital Twin representation
What-if simulation
Scenario comparison
Parameter constraint validation
Agentic decision support
Continuous machine monitoring
Streamlit dashboard
End-to-end prediction-to-decision pipeline
Novelty

The main novelty of AgentTwinDefect AI is the integration of machine-failure prediction, Digital Twin what-if simulation, scenario comparison, and agentic decision support into one workflow.

Instead of:

Prediction Only

the system provides:

Prediction
    ↓
Simulation
    ↓
Scenario Evaluation
    ↓
Decision Support

The novelty is primarily architectural and integrative, extending the AI-enabled Digital Twin concept toward agentic decision support.

Technology Stack
Category	Technology	Purpose
Programming	Python	Application development
Data Processing	Pandas, NumPy	Data processing
Machine Learning	Scikit-learn	Failure prediction
ML Model	Random Forest	Classification
Digital Twin	Python	What-if simulation
Dashboard	Streamlit	Monitoring and visualization
Version Control	Git	Source-code management
Repository	GitHub	Project hosting
Architecture
                    ┌──────────────────────┐
                    │     AI4I Dataset     │
                    │       ai4i.csv       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │     Data Loader      │
                    │ Validation + Schema  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Random Forest ML   │
                    │  Failure Prediction  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Failure Risk      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    Digital Twin      │
                    │  What-if Simulation  │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Scenario Engine    │
                    │  Scenario Comparison │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Agentic Decision    │
                    │       Layer          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Streamlit Dashboard  │
                    └──────────────────────┘
Dataset
AI4I 2020 Predictive Maintenance Dataset

The project uses the AI4I 2020 Predictive Maintenance Dataset, containing 10,000 machine records.

Main Features
Feature	Description
Air temperature [K]	Ambient temperature
Process temperature [K]	Process temperature
Rotational speed [rpm]	Machine rotational speed
Torque [Nm]	Applied torque
Tool wear [min]	Tool wear
Target
Machine failure

The failure-mode columns are not used as primary model inputs to avoid target leakage.

Project Structure
AgentTwinDefect AI/
│
├── agenttwindefect/
│   ├── agent.py
│   ├── data_loader.py
│   ├── defect_model.py
│   ├── digital_twin.py
│   ├── live_stream.py
│   ├── pipeline.py
│   ├── scenario_engine.py
│   └── validation.py
│
├── data/
│   └── ai4i.csv
│
├── dashboard.py
└── README.md
Running the Project
Install Dependencies
pip install pandas numpy scikit-learn streamlit
Complete Pipeline
python -m agenttwindefect.pipeline
Model Training and Evaluation
python -m agenttwindefect.defect_model
Digital Twin
python -m agenttwindefect.digital_twin
Scenario Engine
python -m agenttwindefect.scenario_engine
Agent
python -m agenttwindefect.agent
Dashboard
python -m streamlit run dashboard.py
Model Evaluation

The Random Forest model is evaluated using:

Accuracy
Precision
Recall
F1 Score
Confusion Matrix
Feature Importance

Current test performance:

Accuracy  : approximately 98.3%
Precision : approximately 88.6%
Recall    : approximately 57.4%
F1 Score  : approximately 69.7%

Because the dataset is imbalanced, accuracy is considered together with failure-class recall and F1 score.

Expected Outcomes

AgentTwinDefect AI is designed to provide:

Early identification of machine failure risk.
Virtual evaluation of possible parameter changes.
Comparison of corrective scenarios.
Transparent agent-based decision support.
Continuous machine-condition monitoring.
A foundation for future real-time industrial integration.
Limitations
The Digital Twin is currently data-driven rather than physics-based.
AI4I is a benchmark dataset rather than a live industrial sensor feed.
Scenario evaluation mainly focuses on single-parameter changes.
The agent is rule-based rather than LLM-based.
The prototype does not directly control physical machinery.
Future Scope

The system can be extended with:

Real-time IoT sensor integration
Physics-based Digital Twin models
Explainable AI
Context-aware decision making
Multi-parameter optimization
Multi-agent architecture
LLM-based agent interaction
Real industrial machine integration
Base Paper

Dai et al. (2025).

Generative and Predictive AI for Digital Twin Systems in Manufacturing

Frontiers in Artificial Intelligence

https://doi.org/10.3389/frai.2025.1655470

Team
Name	Roll Number
S. Sushmita	2420090076
P. Goda Sahasra	2420090128
K. Amulya	2420090132
Project Guide

Dr. Srikanth Cherukuvada
Assistant Professor
Department of Computer Science and Engineering
KLH CSE Bowrampet Campus

Project Focus

AgentTwinDefect AI: An Agentic Digital Twin Platform for Real-Time Hidden Defect Prediction in Smart Manufacturing

Predict → Simulate → Compare → Decide
