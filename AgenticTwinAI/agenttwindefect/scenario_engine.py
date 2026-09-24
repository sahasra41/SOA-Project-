"""
Scenario comparison layer.

Generates candidate machine-parameter adjustments, runs each
scenario through the Digital Twin, and compares the resulting
machine-failure risk.

The scenarios are virtual what-if simulations. They do not
physically control the machine.
"""

from __future__ import annotations

import pandas as pd

from .digital_twin import ADJUSTABLE_PARAMS, DigitalTwin, ProcessState


# Candidate virtual adjustments for the AI4I machine parameters.
#
# Tool wear is intentionally excluded because it is treated as
# a monitored machine-health condition rather than an immediate
# controllable parameter.
STEP_SIZES = {
    "Air temperature [K]": [-2.0, -1.0, 1.0, 2.0],
    "Process temperature [K]": [-2.0, -1.0, 1.0, 2.0],
    "Rotational speed [rpm]": [-200, -100, 100, 200],
    "Torque [Nm]": [-10.0, -5.0, 5.0, 10.0],
}


# Approximate virtual adjustment cost.
#
# These are prototype scoring weights, not real industrial costs.
PARAM_COST_PER_UNIT = {
    "Air temperature [K]": 0.20,
    "Process temperature [K]": 0.20,
    "Rotational speed [rpm]": 0.01,
    "Torque [Nm]": 0.05,
}


def generate_scenarios(
    twin: DigitalTwin,
    state: ProcessState,
) -> pd.DataFrame:
    """
    Generate and compare virtual machine scenarios.

    Each scenario changes one machine parameter and evaluates
    the resulting failure probability using the Digital Twin.
    """

    baseline = twin.assess(state)

    rows = []

    for param in ADJUSTABLE_PARAMS:

        # Skip parameters for which no scenario steps are defined.
        if param not in STEP_SIZES:
            continue

        for delta in STEP_SIZES[param]:

            current_value = state.to_dict()[param]
            new_value = current_value + delta

            # Calculate a simple virtual adjustment cost.
            cost = abs(delta) * PARAM_COST_PER_UNIT[param]

            row = {
                "param": param,
                "delta": delta,
                "new_value": round(new_value, 3),

                "baseline_failure_probability": round(
                    baseline["failure_probability"],
                    4,
                ),

                "predicted_failure_probability": float("nan"),

                "baseline_failure_risk_percent": round(
                    baseline["failure_risk_percent"],
                    2,
                ),

                "predicted_failure_risk_percent": float("nan"),

                "risk_change": float("nan"),

                "risk_reduction_pp": float("nan"),

                "risk_level": "INVALID",

                "machine_failure_prediction": None,

                "adjustment_cost": round(cost, 3),

                "constraint_valid": False,

                "constraint_status": "NOT_SIMULATED",

                "validation_message": "",
            }

            try:
                result = twin.what_if(
                    state,
                    param,
                    delta,
                )

                after = result["state_after"]

                risk_change = result["risk_change"]

                row.update(
                    {
                        "predicted_failure_probability": round(
                            after["failure_probability"],
                            4,
                        ),

                        "predicted_failure_risk_percent": round(
                            after["failure_risk_percent"],
                            2,
                        ),

                        "risk_change": round(
                            risk_change,
                            4,
                        ),

                        "risk_reduction_pp": round(
                            -risk_change * 100,
                            2,
                        ),

                        "risk_level": after["risk_level"],

                        "machine_failure_prediction": after[
                            "machine_failure"
                        ],

                        "constraint_valid": True,

                        "constraint_status": "VALID",

                        "validation_message": "",
                    }
                )

            except (TypeError, ValueError, KeyError) as exc:

                row["constraint_valid"] = False

                row["constraint_status"] = "REJECTED"

                row["risk_level"] = "INVALID"

                row["validation_message"] = str(exc)

            rows.append(row)

    df = pd.DataFrame(rows)

    if df.empty:
        return df

    # ---------------------------------------------------------
    # Decision scoring
    # ---------------------------------------------------------
    #
    # Lower predicted failure probability is preferred.
    # Smaller parameter changes receive a lower adjustment cost.
    # Invalid scenarios receive a large penalty.
    #

    df["parameter_change_penalty"] = (
        0.15 * df["adjustment_cost"]
    )

    df["safety_penalty"] = (
        (~df["constraint_valid"]).astype(float) * 10.0
    )

    df["decision_score"] = (
        df["predicted_failure_probability"].fillna(1.0)
        + df["parameter_change_penalty"]
        + df["safety_penalty"]
    )

    # Utility represents improvement in failure risk after
    # accounting for the adjustment penalty.

    df["utility"] = (
        -df["risk_change"].fillna(0.0)
        - df["parameter_change_penalty"]
    )

    # Sort valid scenarios first, then lower decision score,
    # then higher utility.

    return df.sort_values(
        [
            "constraint_valid",
            "decision_score",
            "utility",
        ],
        ascending=[
            False,
            True,
            False,
        ],
    ).reset_index(drop=True)


if __name__ == "__main__":
    print("\nSCENARIO ENGINE TEST")
    print("=" * 70)

    from .defect_model import MachineFailureModel

    # Train the machine-failure model.
    model = MachineFailureModel()
    model.train()

    # Example machine state.
    machine = ProcessState(
        air_temperature=298.1,
        process_temperature=308.6,
        rotational_speed=1551,
        torque=42.8,
        tool_wear=0,
    )

    # Create Digital Twin.
    twin = DigitalTwin(model)

    # Generate virtual scenarios.
    scenarios = generate_scenarios(
        twin,
        machine,
    )

    print("\nBASELINE MACHINE STATE")
    print("-" * 70)

    baseline = twin.assess(machine)

    print(
        f"Baseline failure risk: "
        f"{baseline['failure_risk_percent']:.2f}%"
    )

    print(
        f"Baseline risk level: "
        f"{baseline['risk_level']}"
    )

    print("\nGENERATED SCENARIOS")
    print("-" * 70)

    display_columns = [
        "param",
        "delta",
        "new_value",
        "predicted_failure_risk_percent",
        "risk_reduction_pp",
        "risk_level",
        "decision_score",
    ]

    print(
        scenarios[display_columns].to_string(
            index=False
        )
    )

    print("\nBEST VALID SCENARIO")
    print("-" * 70)

    valid_scenarios = scenarios[
        scenarios["constraint_valid"]
    ]

    if not valid_scenarios.empty:

        best = valid_scenarios.iloc[0]

        print(
            f"Parameter : {best['param']}"
        )

        print(
            f"Change    : {best['delta']}"
        )

        print(
            f"New value : {best['new_value']}"
        )

        print(
            f"Risk      : "
            f"{best['predicted_failure_risk_percent']:.2f}%"
        )

        print(
            f"Risk change: "
            f"{best['risk_reduction_pp']:.2f} percentage points"
        )

        print(
            f"Risk level: {best['risk_level']}"
        )

    else:
        print("No valid scenarios were generated.")