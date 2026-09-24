"""
Agentic Decision Layer (AAI).

This module extends the machine-failure prediction and Digital Twin
with a transparent agentic decision policy.

The agent:
1. Evaluates the current machine failure risk.
2. Generates virtual what-if scenarios.
3. Compares the scenarios using failure-risk reduction and adjustment cost.
4. Produces one of four decisions:
   - AUTO_ACT
   - RECOMMEND
   - ESCALATE
   - NO_ACTION_NEEDED

AUTO_ACT in this prototype means that the agent has selected a
virtual action as suitable for automatic execution logic. The
prototype does NOT physically control a machine.

The decision rationale is stored for operator audit and future
feedback/learning analysis.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

import pandas as pd

from .digital_twin import DigitalTwin, ProcessState
from .scenario_engine import generate_scenarios


# ------------------------------------------------------------
# Agent decision policy
# ------------------------------------------------------------

# Minimum absolute failure-risk reduction required for AUTO_ACT.
AUTO_ACT_RISK_DROP = 0.15

# Maximum virtual adjustment cost allowed for AUTO_ACT.
AUTO_ACT_MAX_COST = 1.0

# Minimum failure-risk reduction worth recommending.
RECOMMEND_RISK_DROP = 0.05

# Baseline failure probability above this value is considered
# elevated risk by the agent.
HIGH_RISK_THRESHOLD = 0.50


@dataclass
class Decision:
    """Stores one agent decision and its supporting evidence."""

    action: str
    baseline_failure_probability: float
    chosen_scenario: dict | None
    rationale: str
    scenario_table: pd.DataFrame

    baseline_risk_level: str = "UNKNOWN"

    decision_score: float | None = None

    constraint_valid: bool = False

    warning: str | None = None

    timestamp: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )

    def summary(self) -> str:
        """Return a human-readable explanation of the decision."""

        lines = [
            f"[{self.timestamp}] Decision: {self.action}",
            (
                "Baseline failure probability: "
                f"{self.baseline_failure_probability:.1%}"
            ),
            (
                "Current risk level: "
                f"{self.baseline_risk_level}"
            ),
        ]

        if self.chosen_scenario is not None:

            scenario = self.chosen_scenario

            lines.append(
                "Selected virtual change: "
                f"{scenario['param']} "
                f"{'+' if scenario['delta'] > 0 else ''}"
                f"{scenario['delta']} "
                f"-> new value {scenario['new_value']}"
            )

            lines.append(
                "Predicted failure probability: "
                f"{scenario['predicted_failure_probability']:.1%}"
            )

            lines.append(
                "Risk reduction: "
                f"{scenario['risk_reduction_pp']:+.2f} "
                "percentage points"
            )

            lines.append(
                "Constraint status: "
                f"{scenario['constraint_status']}"
            )

            lines.append(
                "Decision score: "
                f"{scenario['decision_score']:.3f}"
            )

        if self.warning:
            lines.append(
                f"Warning: {self.warning}"
            )

        lines.append(
            f"Rationale: {self.rationale}"
        )

        return "\n".join(lines)


class AgentTwinDefectAgent:
    """
    Agentic decision layer for machine-failure scenarios.

    The class name is retained for compatibility with the existing
    project structure, while its logic now operates on machine
    condition and failure-risk predictions.
    """

    def __init__(self, twin: DigitalTwin):
        self.twin = twin

        # Decision history acts as the feedback/audit hook.
        self.decision_log: list[Decision] = []

    def decide(self, state: ProcessState) -> Decision:
        """
        Evaluate the current machine state and choose an action.
        """

        # ----------------------------------------------------
        # Step 1: Assess current machine condition
        # ----------------------------------------------------

        baseline = self.twin.assess(state)

        baseline_risk = baseline[
            "failure_probability"
        ]

        # ----------------------------------------------------
        # Step 2: Generate virtual what-if scenarios
        # ----------------------------------------------------

        scenarios = generate_scenarios(
            self.twin,
            state,
        )

        valid_scenarios = scenarios[
            scenarios["constraint_valid"]
        ]

        # The scenario engine already ranks scenarios.
        best = (
            valid_scenarios.iloc[0]
            if not valid_scenarios.empty
            else None
        )

        warning = None

        # ----------------------------------------------------
        # Step 3: Handle case where no valid scenario exists
        # ----------------------------------------------------

        if best is None:

            decision = Decision(
                action="ESCALATE",

                baseline_failure_probability=baseline_risk,

                chosen_scenario=None,

                rationale=(
                    "No valid virtual machine adjustment was "
                    "available within the defined operating "
                    "constraints. Human engineering review is "
                    "required."
                ),

                scenario_table=scenarios,

                baseline_risk_level=baseline[
                    "risk_level"
                ],

                constraint_valid=False,

                warning=(
                    "No valid machine scenario was available."
                ),
            )

            self.decision_log.append(decision)

            return decision

        # ----------------------------------------------------
        # Step 4: Check whether the selected scenario still
        #         leaves the machine at HIGH risk.
        # ----------------------------------------------------

        if best["risk_level"] == "HIGH":

            warning = (
                "The selected virtual configuration reduces "
                "risk but the resulting machine state remains "
                "HIGH risk."
            )

        # Calculate how much the scenario reduces failure risk.

        risk_reduction = -float(
            best["risk_change"]
        )

        # ----------------------------------------------------
        # Step 5: NO ACTION NEEDED
        # ----------------------------------------------------

        if (
            baseline_risk < HIGH_RISK_THRESHOLD
            and risk_reduction < RECOMMEND_RISK_DROP
        ):

            decision = Decision(
                action="NO_ACTION_NEEDED",

                baseline_failure_probability=baseline_risk,

                chosen_scenario=None,

                rationale=(
                    f"Baseline machine failure probability "
                    f"({baseline_risk:.1%}) is below the "
                    f"{HIGH_RISK_THRESHOLD:.0%} elevated-risk "
                    "threshold, and the best available virtual "
                    f"adjustment reduces risk by only "
                    f"{risk_reduction:.1%}. "
                    "The machine is within the defined "
                    "acceptable operating range."
                ),

                scenario_table=scenarios,

                baseline_risk_level=baseline[
                    "risk_level"
                ],

                decision_score=float(
                    best["decision_score"]
                ),

                constraint_valid=bool(
                    best["constraint_valid"]
                ),

                warning=warning,
            )

        # ----------------------------------------------------
        # Step 6: AUTO ACT
        # ----------------------------------------------------

        elif (
            risk_reduction >= AUTO_ACT_RISK_DROP
            and best["adjustment_cost"]
            <= AUTO_ACT_MAX_COST
        ):

            decision = Decision(
                action="AUTO_ACT",

                baseline_failure_probability=baseline_risk,

                chosen_scenario=best.to_dict(),

                rationale=(
                    f"The selected virtual scenario "
                    f"({best['param']} {best['delta']:+g}) "
                    f"reduces predicted machine failure risk "
                    f"by {risk_reduction:.1%}, meeting the "
                    f"{AUTO_ACT_RISK_DROP:.0%} automatic-action "
                    f"threshold. Its virtual adjustment cost "
                    f"({best['adjustment_cost']:.2f}) is within "
                    f"the {AUTO_ACT_MAX_COST:.2f} limit. "
                    "The action is selected by the agent's "
                    "transparent policy and logged for audit."
                ),

                scenario_table=scenarios,

                baseline_risk_level=baseline[
                    "risk_level"
                ],

                decision_score=float(
                    best["decision_score"]
                ),

                constraint_valid=bool(
                    best["constraint_valid"]
                ),

                warning=warning,
            )

        # ----------------------------------------------------
        # Step 7: RECOMMEND
        # ----------------------------------------------------

        elif risk_reduction >= RECOMMEND_RISK_DROP:

            decision = Decision(
                action="RECOMMEND",

                baseline_failure_probability=baseline_risk,

                chosen_scenario=best.to_dict(),

                rationale=(
                    f"The selected virtual scenario reduces "
                    f"machine failure risk by "
                    f"{risk_reduction:.1%}. This is a meaningful "
                    "improvement, but it does not satisfy the "
                    "automatic-action threshold or cost policy. "
                    "The change is therefore presented to the "
                    "operator for human approval."
                ),

                scenario_table=scenarios,

                baseline_risk_level=baseline[
                    "risk_level"
                ],

                decision_score=float(
                    best["decision_score"]
                ),

                constraint_valid=bool(
                    best["constraint_valid"]
                ),

                warning=warning,
            )

        # ----------------------------------------------------
        # Step 8: ESCALATE
        # ----------------------------------------------------

        else:

            decision = Decision(
                action="ESCALATE",

                baseline_failure_probability=baseline_risk,

                chosen_scenario=best.to_dict(),

                rationale=(
                    f"Baseline machine failure probability "
                    f"is {baseline_risk:.1%}, but no available "
                    "single-parameter virtual adjustment "
                    f"reduces risk by at least "
                    f"{RECOMMEND_RISK_DROP:.0%}. "
                    "The current Digital Twin parameter space "
                    "may therefore be insufficient to address "
                    "the underlying machine condition. "
                    "Human engineering investigation is required "
                    "instead of selecting an ineffective action."
                ),

                scenario_table=scenarios,

                baseline_risk_level=baseline[
                    "risk_level"
                ],

                decision_score=float(
                    best["decision_score"]
                ),

                constraint_valid=bool(
                    best["constraint_valid"]
                ),

                warning=warning,
            )

        # ----------------------------------------------------
        # Step 9: Store decision history
        # ----------------------------------------------------

        self.decision_log.append(decision)

        return decision


if __name__ == "__main__":
    print("\nAGENTIC DECISION LAYER TEST")
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

    # Create the Digital Twin.
    twin = DigitalTwin(model)

    # Create the agent.
    agent = AgentTwinDefectAgent(twin)

    # Ask the agent to evaluate the machine.
    decision = agent.decide(machine)

    print("\nAGENT DECISION")
    print("-" * 70)

    print(decision.summary())

    print("\nSCENARIO COUNT")
    print("-" * 70)

    print(
        f"Total scenarios evaluated: "
        f"{len(decision.scenario_table)}"
    )

    print(
        f"Valid scenarios: "
        f"{decision.scenario_table['constraint_valid'].sum()}"
    )

    print(
        f"Decision log size: "
        f"{len(agent.decision_log)}"
    )