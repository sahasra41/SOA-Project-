"""
CSV-based live manufacturing data stream.

Each call to step() reads the next row from
inspection_data.csv.

defect_type is NOT passed to the model.
It is only present in the CSV as the known
training/validation label.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .data_loader import (
    DATASET_PATH,
    FEATURE_COLUMNS,
)
from .digital_twin import ProcessState


class LiveSensorStream:

    def __init__(
        self,
        csv_path=DATASET_PATH,
    ):

        self.csv_path = Path(csv_path)

        if not self.csv_path.is_file():
            raise FileNotFoundError(
                f"CSV file not found: {self.csv_path}"
            )

        self.data = pd.read_csv(
            self.csv_path
        )

        # Verify required input columns
        missing = [
            column
            for column in FEATURE_COLUMNS
            if column not in self.data.columns
        ]

        if missing:
            raise ValueError(
                "CSV is missing required input columns: "
                + ", ".join(missing)
            )

        self.data = self.data[
            FEATURE_COLUMNS
        ].copy()

        self.index = 0

        self.state = None

    def step(self) -> ProcessState:
        """
        Read the next CSV row.

        Only FEATURE_COLUMNS are converted
        into the ProcessState.

        defect_type is NOT read here.
        """

        # Restart when reaching end of CSV
        if self.index >= len(self.data):
            self.index = 0

        row = self.data.iloc[
            self.index
        ]

        self.index += 1

        self.state = ProcessState(
            product_length_mm=float(
                row["product_length_mm"]
            ),
            product_width_mm=float(
                row["product_width_mm"]
            ),
            product_thickness_mm=float(
                row["product_thickness_mm"]
            ),
            material_hardness_hb=float(
                row["material_hardness_hb"]
            ),
            process_temperature_c=float(
                row["process_temperature_c"]
            ),
            machine_pressure_kpa=float(
                row["machine_pressure_kpa"]
            ),
            surface_roughness_um=float(
                row["surface_roughness_um"]
            ),
            weight_deviation_pct=float(
                row["weight_deviation_pct"]
            ),
            inspection_temperature_c=float(
                row["inspection_temperature_c"]
            ),
            vibration_rms=float(
                row["vibration_rms"]
            ),
        )

        return self.state

    def apply_correction(
        self,
        param: str,
        new_value: float,
    ):
        """
        Apply a virtual correction to the current
        Digital Twin state.

        This does NOT change the physical machine.
        """

        if self.state is None:
            return

        setattr(
            self.state,
            param,
            new_value,
        )