"""
AgentTwinDefect AI
-------------------
Research extension of Dai et al. (2025), "Generative and Predictive AI for
digital twin systems in manufacturing" (Frontiers in AI).

The base paper implements Generative AI (3D reconstruction) and Predictive AI
(defect detection/classification) inside an AI-enabled Digital Twin (AI-DT)
framework, and explicitly leaves Explainable AI, Context-Aware AI, and
Agentic AI as *future work*.

This package fills that gap for the welding use case with a closed loop:

    ML Defect Prediction
        -> Digital Twin What-if Simulation
            -> Scenario Comparison
                -> Agentic Decision Layer
                    -> Corrective Recommendation

Modules:
    data_gen.py       - synthetic welding process/sensor data generator
    defect_model.py   - Predictive AI: ML defect probability/classification model
    digital_twin.py   - Digital Twin: what-if simulator built on the trained model
    scenario_engine.py- generates & scores candidate corrective scenarios
    agent.py          - Agentic Decision Layer: policy that picks + explains a fix
    pipeline.py        - end-to-end orchestration (the runnable demo)
"""
