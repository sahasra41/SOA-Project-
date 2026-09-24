"""
End-to-end AgentTwinDefect AI demo.

Data source:
    data/ai4i.csv

Pipeline:
    AI4I machine data
          ↓
    Random Forest
          ↓
    Machine failure prediction
          ↓
    Digital Twin
          ↓
    What-if scenario evaluation
          ↓
    Agentic decision
"""

from __future__ import annotations

from .agent import AgentTwinDefectAgent
from .data_loader import FEATURE_COLUMNS, TARGET_COLUMN, load_dataset
from .defect_model import MachineFailureModel
from .digital_twin import DigitalTwin, ProcessState


def build_example_states():
    """
    Build example machine states for the Digital Twin and Agent.

    These are virtual demonstration states based on the feature
    ranges present in the AI4I dataset.
    """

    return [
        (
            "Normal operating condition",
            ProcessState(
                air_temperature=298.1,
                process_temperature=308.6,
                rotational_speed=1551,
                torque=42.8,
                tool_wear=0,
            ),
        ),
        (
            "Higher rotational speed",
            ProcessState(
                air_temperature=298.5,
                process_temperature=309.0,
                rotational_speed=2200,
                torque=45.0,
                tool_wear=80,
            ),
        ),
        (
            "High-load machine condition",
            ProcessState(
                air_temperature=300.0,
                process_temperature=312.0,
                rotational_speed=2600,
                torque=65.0,
                tool_wear=180,
            ),
        ),
        (
            "High tool-wear condition",
            ProcessState(
                air_temperature=299.5,
                process_temperature=310.5,
                rotational_speed=1800,
                torque=55.0,
                tool_wear=250,
            ),
        ),
    ]


def main():

    print("=" * 70)
    print("AgentTwinDefect AI - End-to-End Machine Demo")
    print("=" * 70)

    # --------------------------------------------------
    # 1. LOAD AI4I DATASET
    # --------------------------------------------------

    print("\n[1/4] Loading AI4I machine data from CSV...")

    train_df = load_dataset()

    print(
        f"      Loaded {len(train_df)} machine records."
    )

    print(
        f"      Input features: {len(FEATURE_COLUMNS)}"
    )

    for feature in FEATURE_COLUMNS:
        print(f"        - {feature}")

    print(
        f"      Target: {TARGET_COLUMN}"
    )

    print("\n      Machine failure distribution:")

    print(
        train_df[TARGET_COLUMN]
        .value_counts()
        .sort_index()
        .to_string()
    )

    # --------------------------------------------------
    # 2. TRAIN RANDOM FOREST
    # --------------------------------------------------

    print("\n[2/4] Training Random Forest machine-failure model...")

    predictor = MachineFailureModel(
        random_state=42
    )

    metrics = predictor.train(train_df)

    print("\n      Model evaluation:")

    print(
        f"        Accuracy  : {metrics['accuracy']:.4f}"
    )

    print(
        f"        Precision : {metrics['precision']:.4f}"
    )

    print(
        f"        Recall    : {metrics['recall']:.4f}"
    )

    print(
        f"        F1 Score  : {metrics['f1']:.4f}"
    )

    print("\n      Top predictive machine features:")

    importance = predictor.get_feature_importance()

    sorted_features = sorted(
        importance.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    for feature, value in sorted_features[:3]:
        print(
            f"        - {feature}: {value:.3f}"
        )

    # --------------------------------------------------
    # 3. CREATE DIGITAL TWIN + AGENT
    # --------------------------------------------------

    print(
        "\n[3/4] Creating Digital Twin + Agent..."
    )

    twin = DigitalTwin(predictor)

    agent = AgentTwinDefectAgent(twin)

    print(
        "      Digital Twin: READY"
    )

    print(
        "      Agent: READY"
    )

    # --------------------------------------------------
    # 4. RUN MACHINE SCENARIOS
    # --------------------------------------------------

    print(
        "\n[4/4] Running machine condition scenarios..."
    )

    for name, state in build_example_states():

        print("\n" + "-" * 70)

        print(
            f"SCENARIO: {name}"
        )

        print("-" * 70)

        print("\nMachine state:")

        for parameter, value in state.to_dict().items():
            print(
                f"  {parameter}: {value}"
            )

        # Agent evaluates the machine.
        decision = agent.decide(state)

        print("\n" + decision.summary())

        # --------------------------------------------------
        # Show top virtual scenarios
        # --------------------------------------------------

        print(
            "\nTop candidate virtual machine scenarios:"
        )

        columns = [
            "param",
            "delta",
            "new_value",
            "predicted_failure_risk_percent",
            "risk_reduction_pp",
            "risk_level",
            "adjustment_cost",
            "utility",
        ]

        available_columns = [
            column
            for column in columns
            if column in decision.scenario_table.columns
        ]

        print(
            decision.scenario_table[
                available_columns
            ]
            .head(5)
            .to_string(index=False)
        )

    # --------------------------------------------------
    # FINAL SUMMARY
    # --------------------------------------------------

    print("\n" + "=" * 70)

    print(
        "End-to-end demonstration completed successfully."
    )

    print(
        f"Decision log contains "
        f"{len(agent.decision_log)} entries."
    )

    print("=" * 70)


if __name__ == "__main__":
    main()