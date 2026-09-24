"""Digital Twin what-if simulation for machine condition monitoring."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .data_loader import FEATURE_COLUMNS
from .defect_model import MachineFailureModel



ADJUSTABLE_PARAMS = [
    "Air temperature [K]",
    "Process temperature [K]",
    "Rotational speed [rpm]",
    "Torque [Nm]",
]


# Basic prototype bounds for safe what-if simulation.
# These are used only to prevent unrealistic scenario values.
PARAM_BOUNDS = {
    "Air temperature [K]": (295.0, 305.0),
    "Process temperature [K]": (305.0, 315.0),
    "Rotational speed [rpm]": (1000.0, 3000.0),
    "Torque [Nm]": (10.0, 80.0),
    "Tool wear [min]": (0.0, 300.0),
}


def risk_level(probability: float) -> str:
    """Convert failure probability into a simple risk category."""

    if probability >= 0.70:
        return "HIGH"
    if probability >= 0.30:
        return "MEDIUM"
    return "LOW"


@dataclass
class ProcessState:
    """
    Virtual representation of the current machine condition.

    The state contains the five machine variables used by the
    machine-failure prediction model.
    """

    air_temperature: float
    process_temperature: float
    rotational_speed: float
    torque: float
    tool_wear: float

    def to_dict(self) -> dict:
        """Return the state using AI4I dataset column names."""

        return {
            "Air temperature [K]": self.air_temperature,
            "Process temperature [K]": self.process_temperature,
            "Rotational speed [rpm]": self.rotational_speed,
            "Torque [Nm]": self.torque,
            "Tool wear [min]": self.tool_wear,
        }

    def to_frame(self) -> pd.DataFrame:
        """Convert the machine state into model input format."""

        return pd.DataFrame([self.to_dict()])[FEATURE_COLUMNS]

    def with_unchecked_adjustment(
        self,
        param: str,
        delta: float,
    ) -> "ProcessState":
        """Create a new state without performing safety checks."""

        values = self.to_dict()

        if param not in values:
            raise ValueError(f"Unknown machine parameter: {param}")

        values[param] = values[param] + delta

        return ProcessState(
            air_temperature=values["Air temperature [K]"],
            process_temperature=values["Process temperature [K]"],
            rotational_speed=values["Rotational speed [rpm]"],
            torque=values["Torque [Nm]"],
            tool_wear=values["Tool wear [min]"],
        )

    def with_adjustment(
        self,
        param: str,
        delta: float,
    ) -> "ProcessState":
        """
        Create a safe what-if machine state.

        Only parameters listed in ADJUSTABLE_PARAMS can be changed.
        """

        if param not in ADJUSTABLE_PARAMS:
            raise ValueError(
                f"{param} is not an adjustable machine parameter"
            )

        current_value = self.to_dict()[param]
        new_value = current_value + delta

        if param in PARAM_BOUNDS:
            low, high = PARAM_BOUNDS[param]

            if not low <= new_value <= high:
                raise ValueError(
                    f"{param} adjustment produces {new_value:g}, "
                    f"outside allowed range {low:g} to {high:g}"
                )

        return self.with_unchecked_adjustment(param, delta)


class DigitalTwin:
    """
    Data-driven Digital Twin for machine failure what-if analysis.

    The Digital Twin does not physically control a machine.
    It creates virtual machine states and uses the trained
    machine-failure model to estimate the resulting failure risk.
    """

    def __init__(self, predictor: MachineFailureModel):
        self.predictor = predictor

    def assess(self, state: ProcessState) -> dict:
        """Assess the current machine state."""

        result = self.predictor.predict_state(state.to_dict())

        failure_probability = result["failure_probability"]

        return {
            "machine_failure": result["machine_failure"],
            "failure_probability": failure_probability,
            "failure_risk_percent": failure_probability * 100.0,
            "risk_level": risk_level(failure_probability),
            "status": result["status"],
            "model_confidence": max(
                failure_probability,
                1.0 - failure_probability,
            ),
            "machine_state": state.to_dict(),
        }

    def what_if(
        self,
        state: ProcessState,
        param: str,
        delta: float,
    ) -> dict:
        """
        Simulate a virtual change to one machine parameter.

        The physical machine is not changed. Only the virtual
        Digital Twin state is modified.
        """

        new_state = state.with_adjustment(param, delta)

        before = self.assess(state)
        after = self.assess(new_state)

        risk_change = (
            after["failure_probability"]
            - before["failure_probability"]
        )

        return {
            "param": param,
            "delta": delta,
            "new_value": new_state.to_dict()[param],
            "state_before": before,
            "state_after": after,
            "risk_change": risk_change,
            "risk_change_percent": risk_change * 100.0,
            "resulting_state": new_state,
        }


if __name__ == "__main__":
    print("\nDIGITAL TWIN TEST")
    print("=" * 60)

    # Import and train the machine-failure model.
    model = MachineFailureModel()
    model.train()

    # Example machine state from the AI4I dataset.
    machine = ProcessState(
        air_temperature=298.1,
        process_temperature=308.6,
        rotational_speed=1551,
        torque=42.8,
        tool_wear=0,
    )

    twin = DigitalTwin(model)

    print("\nCURRENT MACHINE STATE")
    print("-" * 60)

    for parameter, value in machine.to_dict().items():
        print(f"{parameter}: {value}")

    current = twin.assess(machine)

    print("\nCURRENT FAILURE ASSESSMENT")
    print("-" * 60)
    print(f"Machine failure : {current['machine_failure']}")
    print(f"Failure risk    : {current['failure_risk_percent']:.2f}%")
    print(f"Risk level      : {current['risk_level']}")
    print(f"Status          : {current['status']}")

    print("\nWHAT-IF SIMULATION")
    print("-" * 60)

    scenario = twin.what_if(
        machine,
        "Rotational speed [rpm]",
        -100,
    )

    print(f"Parameter       : {scenario['param']}")
    print(f"Adjustment      : {scenario['delta']}")
    print(f"New value       : {scenario['new_value']}")

    print(
        f"Before risk     : "
        f"{scenario['state_before']['failure_risk_percent']:.2f}%"
    )

    print(
        f"After risk      : "
        f"{scenario['state_after']['failure_risk_percent']:.2f}%"
    )

    print(
        f"Risk change     : "
        f"{scenario['risk_change_percent']:.2f}%"
    )