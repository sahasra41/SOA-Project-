"""Validation rules for AI4I machine-state prediction and simulation."""

from __future__ import annotations

from dataclasses import fields
from math import isfinite
from numbers import Real


# Preferred operating bounds for virtual what-if adjustments.
PARAM_BOUNDS = {
    "Air temperature [K]": (295.0, 305.0),
    "Process temperature [K]": (305.0, 315.0),
    "Rotational speed [rpm]": (1000.0, 3000.0),
    "Torque [Nm]": (10.0, 80.0),
}


# Broader input bounds used to reject clearly invalid machine states.
INPUT_BOUNDS = {
    "air_temperature": (295.0, 305.0),
    "process_temperature": (305.0, 315.0),
    "rotational_speed": (500.0, 4000.0),
    "torque": (0.0, 100.0),
    "tool_wear": (0.0, 300.0),
}


def risk_level(probability: float) -> str:
    """Convert machine failure probability into a risk level."""

    if probability >= 0.75:
        return "HIGH"

    if probability >= 0.50:
        return "MEDIUM"

    return "LOW"


def validate_process_values(values: dict) -> dict:
    """
    Validate a machine state.

    Returns errors for invalid values and warnings for potentially
    concerning machine operating combinations.
    """

    errors: list[str] = []
    warnings: list[str] = []

    for name in INPUT_BOUNDS:

        if name not in values or values[name] is None:
            errors.append(f"{name} is missing")
            continue

        value = values[name]

        if isinstance(value, bool) or not isinstance(value, Real):
            errors.append(f"{name} must be numeric")
            continue

        if not isfinite(float(value)):
            errors.append(f"{name} must be finite")
            continue

        low, high = INPUT_BOUNDS[name]

        if not low <= float(value) <= high:
            errors.append(
                f"{name} must be between {low:g} and {high:g}"
            )

    # Only evaluate operating-condition warnings when the
    # basic machine state itself is valid.
    if not errors:

        # High process temperature relative to air temperature.
        temperature_difference = (
            values["process_temperature"]
            - values["air_temperature"]
        )

        if temperature_difference > 15:
            warnings.append(
                "Large temperature difference between process "
                "and air temperature requires operator review."
            )

        # High rotational speed combined with high torque.
        if (
            values["rotational_speed"] > 2500
            and values["torque"] > 60
        ):
            warnings.append(
                "High rotational speed combined with high torque "
                "may represent a high-load operating condition."
            )

        # High tool wear.
        if values["tool_wear"] > 200:
            warnings.append(
                "Tool wear is high; physical inspection or "
                "tool replacement should be considered."
            )

    return {
        "valid": not errors,
        "constraints_satisfied": (
            not errors and not warnings
        ),
        "errors": errors,
        "warnings": warnings,
    }


def validate_process_state(state) -> dict:
    """
    Validate a ProcessState dataclass.

    The Digital Twin uses this before performing a simulation.
    """

    values = {
        field.name: getattr(state, field.name)
        for field in fields(state)
    }

    return validate_process_values(values)


def validate_adjustment(
    state,
    param: str,
    delta: float,
) -> dict:
    """
    Validate a virtual change to a machine parameter.
    """

    errors: list[str] = []

    # Parameter must be one of the supported adjustable variables.
    if param not in PARAM_BOUNDS:
        errors.append(
            f"{param} is not an adjustable machine parameter"
        )

        return {
            "valid": False,
            "constraints_satisfied": False,
            "errors": errors,
            "warnings": [],
        }

    # Delta must be a finite number.
    if (
        isinstance(delta, bool)
        or not isinstance(delta, Real)
        or not isfinite(float(delta))
    ):
        errors.append(
            f"Adjustment for {param} must be numeric and finite"
        )

        return {
            "valid": False,
            "constraints_satisfied": False,
            "errors": errors,
            "warnings": [],
        }

    # Convert the ProcessState to the dataset-style parameter name.
    state_values = state.to_dict()

    if param not in state_values:
        errors.append(
            f"{param} is not available in the machine state"
        )

        return {
            "valid": False,
            "constraints_satisfied": False,
            "errors": errors,
            "warnings": [],
        }

    new_value = (
        state_values[param]
        + float(delta)
    )

    low, high = PARAM_BOUNDS[param]

    if not low <= new_value <= high:
        errors.append(
            f"{param} adjustment produces {new_value:g}, "
            f"outside allowed range {low:g} to {high:g}"
        )

        return {
            "valid": False,
            "constraints_satisfied": False,
            "errors": errors,
            "warnings": [],
        }

    # Create the virtual candidate state.
    candidate = state.with_unchecked_adjustment(
        param,
        float(delta),
    )

    result = validate_process_state(candidate)

    # A warning means the scenario is not considered fully safe
    # for automatic action.
    result["valid"] = (
        result["valid"]
        and result["constraints_satisfied"]
    )

    return result


if __name__ == "__main__":
    print("\nMACHINE VALIDATION TEST")
    print("=" * 60)

    from .digital_twin import ProcessState

    machine = ProcessState(
        air_temperature=298.1,
        process_temperature=308.6,
        rotational_speed=1551,
        torque=42.8,
        tool_wear=0,
    )

    result = validate_process_state(machine)

    print("\nCURRENT MACHINE STATE")
    print("-" * 60)

    print(f"Valid: {result['valid']}")
    print(
        f"Constraints satisfied: "
        f"{result['constraints_satisfied']}"
    )
    print(f"Errors: {result['errors']}")
    print(f"Warnings: {result['warnings']}")

    print("\nADJUSTMENT TEST")
    print("-" * 60)

    adjustment = validate_adjustment(
        machine,
        "Rotational speed [rpm]",
        -100,
    )

    print(f"Valid: {adjustment['valid']}")
    print(
        f"Constraints satisfied: "
        f"{adjustment['constraints_satisfied']}"
    )
    print(f"Errors: {adjustment['errors']}")
    print(f"Warnings: {adjustment['warnings']}")