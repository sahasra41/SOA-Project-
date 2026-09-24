"""
AgentTwinDefect AI - Machine Failure Monitoring Dashboard.

AI4I 2020 machine-condition workflow:

AI4I CSV
    |
    v
Machine Failure Model
    |
    v
Failure Risk
    |
    v
Digital Twin
    |
    v
Virtual What-if Scenarios
    |
    v
Agentic Decision

The dashboard uses a simulated CSV sensor stream.
It does not physically control a machine.
"""

from __future__ import annotations

import time
import traceback

import pandas as pd
import streamlit as st

from agenttwindefect.agent import AgentTwinDefectAgent
from agenttwindefect.data_loader import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    load_dataset,
)
from agenttwindefect.defect_model import MachineFailureModel
from agenttwindefect.digital_twin import DigitalTwin, ProcessState


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AgentTwinDefect AI",
    page_icon="",
    layout="wide",
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 90% -10%,
            #1b4c3d 0,
            transparent 28%
        ),
        radial-gradient(
            circle at 0% 100%,
            #142b29 0,
            transparent 30%
        ),
        #081412;
    color: #eef7f2;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #0b1b18;
    border-right: 1px solid #24443a;
}

[data-testid="stSidebar"] * {
    color: #eef7f2;
}

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #112a23,
        #0d1d1a
    );
    border: 1px solid #24443a;
    border-radius: 14px;
    padding: .8rem 1rem;
}

[data-testid="stMetricLabel"] {
    color: #91aaa0;
}

[data-testid="stMetricValue"] {
    color: #eef7f2;
}

.stDataFrame,
[data-testid="stExpander"] {
    border: 1px solid #24443a;
    border-radius: 14px;
    overflow: hidden;
}

[data-testid="stExpander"] {
    background: #0d1d1a;
}

.stButton > button {
    border: 1px solid #3d6f5b;
    background: #163a2e;
    color: #effff3;
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #d8ff62;
    color: #d8ff62;
}

h1,
h2,
h3,
p,
[data-testid="stMetricValue"] {
    font-family: sans-serif;
}

.hero {
    padding: 1.2rem 1.5rem;
    border: 1px solid #2c5a49;
    border-radius: 18px;
    background: linear-gradient(
        120deg,
        #112d25,
        #174938
    );
    color: #f5fff6;
    box-shadow: 0 16px 45px #00000038;
}

.hero h1 {
    margin: 0;
    font-size: 2.35rem;
}

.hero p {
    margin: .28rem 0 0;
    color: #bde6ce;
    font-size: .95rem;
}

.section-label {
    color: #8ed6ad;
    font-size: .75rem;
    text-transform: uppercase;
    letter-spacing: .1em;
    margin-top: 1rem;
    margin-bottom: .5rem;
}

.explain {
    padding: 1rem 1.1rem;
    border-left: 4px solid #d8ff62;
    background: #10251f;
    border-radius: 0 12px 12px 0;
}

.decision {
    padding: 1rem 1.1rem;
    border-radius: 14px;
    background: #10251f;
    border: 1px solid #315c4b;
    box-shadow: 0 8px 24px #00000026;
}

.small {
    color: #91aaa0;
    font-size: .86rem;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# MODEL + AGENT
# ============================================================

@st.cache_resource
def load_agent() -> AgentTwinDefectAgent:
    """
    Train the Random Forest once and create
    the Digital Twin and Agent.
    """

    dataset = load_dataset()

    predictor = MachineFailureModel(
        random_state=42
    )

    predictor.train(dataset)

    twin = DigitalTwin(
        predictor
    )

    return AgentTwinDefectAgent(
        twin
    )


agent = load_agent()


# ============================================================
# AI4I DATASET
# ============================================================

@st.cache_data
def get_dataset():
    return load_dataset()


dataset = get_dataset()


# ============================================================
# SESSION STATE
# ============================================================

if "row_index" not in st.session_state:
    st.session_state.row_index = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "last_decision" not in st.session_state:
    st.session_state.last_decision = None

if "running" not in st.session_state:
    st.session_state.running = False


# ============================================================
# CONVERT DATASET ROW TO MACHINE STATE
# ============================================================

def row_to_state(
    row: pd.Series,
) -> ProcessState:
    """
    Convert an AI4I dataset row into
    a virtual machine state.
    """

    return ProcessState(
        air_temperature=float(
            row["Air temperature [K]"]
        ),
        process_temperature=float(
            row["Process temperature [K]"]
        ),
        rotational_speed=float(
            row["Rotational speed [rpm]"]
        ),
        torque=float(
            row["Torque [Nm]"]
        ),
        tool_wear=float(
            row["Tool wear [min]"]
        ),
    )


def next_machine_state() -> ProcessState:
    """
    Read the next AI4I record.

    This simulates a continuous
    machine-data streaming feed.
    """

    row = dataset.iloc[
        st.session_state.row_index
        % len(dataset)
    ]

    st.session_state.row_index += 1

    return row_to_state(row)


# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">
    <h1>AgentTwinDefect AI</h1>
    <p>
        Machine intelligence |
        Predict · Simulate · Decide
    </p>
</div>
""",
    unsafe_allow_html=True,
)

st.caption(
    "AI4I machine parameters -> failure prediction -> "
    "Digital Twin what-if simulation -> agentic decision"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("Control Room")

    # --------------------------------------------------------
    # RUN / PAUSE BUTTONS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "Run",
            width="stretch",
        ):

            st.session_state.running = True
            st.rerun()

    with col2:

        if st.button(
            "Pause",
            width="stretch",
        ):

            st.session_state.running = False
            st.rerun()

    # --------------------------------------------------------
    # INPUT INTERVAL
    # --------------------------------------------------------

    refresh_secs = st.slider(
        "Input interval (seconds)",
        min_value=1,
        max_value=10,
        value=3,
        help="Time between automatic machine observations.",
    )

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    if st.button(
        "Reset",
        width="stretch",
    ):

        st.session_state.row_index = 0
        st.session_state.history = []
        st.session_state.last_decision = None
        st.session_state.running = False

        st.rerun()

    st.divider()

    # --------------------------------------------------------
    # MONITORING STATUS
    # --------------------------------------------------------

    st.markdown("Monitoring Status")

    if st.session_state.running:

        st.success("MONITORING RUNNING")

        st.caption(
            f"Automatically reading the next machine "
            f"observation every {refresh_secs} seconds."
        )

    else:

        st.warning("MONITORING PAUSED")

        st.caption(
            "No new machine observation is being processed."
        )

    st.divider()

    # --------------------------------------------------------
    # DATA SOURCE
    # --------------------------------------------------------

    st.markdown("Data Source")

    st.caption(
        f"AI4I dataset\n\n"
        f"{len(dataset)} machine records\n\n"
        f"Target: `{TARGET_COLUMN}`"
    )

    st.divider()

    # --------------------------------------------------------
    # MODEL STATUS
    # --------------------------------------------------------

    st.markdown("Model Status")

    st.success("Random Forest: READY")
    st.success("Digital Twin: READY")
    st.success("Agent: READY")

    st.caption(
        "The dashboard uses CSV data as a simulated "
        "sensor stream. It does not physically control "
        "the machine."
    )


# ============================================================
# AUTOMATIC MACHINE MONITORING
# ============================================================

if st.session_state.running:

    try:

        # ----------------------------------------------------
        # TAKE NEXT MACHINE INPUT
        # ----------------------------------------------------

        state = next_machine_state()

        # ----------------------------------------------------
        # MACHINE FAILURE PREDICTION
        # ----------------------------------------------------

        decision = agent.decide(
            state
        )

        # ----------------------------------------------------
        # DIGITAL TWIN ASSESSMENT
        # ----------------------------------------------------

        assessment = agent.twin.assess(
            state
        )

        # ----------------------------------------------------
        # SAVE CURRENT DECISION
        # ----------------------------------------------------

        st.session_state.last_decision = (
            decision
        )

        # ----------------------------------------------------
        # SAVE MONITORING HISTORY
        # ----------------------------------------------------

        st.session_state.history.append(
            {
                "Cycle":
                    len(
                        st.session_state.history
                    ) + 1,

                "Failure Risk (%)":
                    assessment[
                        "failure_risk_percent"
                    ],

                "Risk Level":
                    assessment[
                        "risk_level"
                    ],

                "Prediction":
                    (
                        "FAILURE"
                        if assessment[
                            "machine_failure"
                        ]
                        else "NORMAL"
                    ),

                "Agent Decision":
                    decision.action,
            }
        )

        # Keep latest 100 cycles
        st.session_state.history = (
            st.session_state.history[-100:]
        )

    except (
        TypeError,
        ValueError,
        KeyError,
    ) as exc:

        traceback.print_exc()

        st.error(
            f"Monitoring error: {exc}"
        )


# ============================================================
# CURRENT MACHINE STATE
# ============================================================

if st.session_state.row_index == 0:

    current_index = 0

else:

    current_index = (
        st.session_state.row_index - 1
    ) % len(dataset)


current_row = dataset.iloc[
    current_index
]

state = row_to_state(
    current_row
)

decision = (
    st.session_state.last_decision
)


# ============================================================
# CURRENT MACHINE ASSESSMENT
# ============================================================

try:

    assessment = agent.twin.assess(
        state
    )

except (
    TypeError,
    ValueError,
    KeyError,
) as exc:

    traceback.print_exc()

    st.error(
        f"Prediction unavailable: {exc}"
    )

    st.stop()


# ============================================================
# SECTION 01 - CURRENT MACHINE STATE
# ============================================================

st.markdown(
    '<div class="section-label">'
    '01 / CURRENT MACHINE STATE'
    '</div>',
    unsafe_allow_html=True,
)

summary_cols = st.columns(5)

summary_cols[0].metric(
    "Cycle",
    f"#{current_index + 1:04d}",
)

summary_cols[1].metric(
    "Failure Risk",
    f"{assessment['failure_risk_percent']:.2f}%",
)

summary_cols[2].metric(
    "Risk Level",
    assessment["risk_level"],
)

summary_cols[3].metric(
    "Prediction",
    (
        "FAILURE"
        if assessment["machine_failure"]
        else "NORMAL"
    ),
)

summary_cols[4].metric(
    "Model Confidence",
    f"{assessment['model_confidence']:.1%}",
)

st.progress(
    min(
        max(
            assessment[
                "failure_probability"
            ],
            0.0,
        ),
        1.0,
    ),
    text=(
        f"Predicted Machine Failure Risk: "
        f"{assessment['failure_risk_percent']:.2f}% "
        f"| {assessment['risk_level']}"
    ),
)


# ============================================================
# SECTION 02 - MACHINE INPUT SIGNALS
# ============================================================

left, right = st.columns(
    [1.15, 1]
)


with left:

    st.markdown(
        '<div class="section-label">'
        '02 / MACHINE INPUT SIGNALS'
        '</div>',
        unsafe_allow_html=True,
    )

    machine_rows = []

    for feature in FEATURE_COLUMNS:

        value = state.to_dict()[
            feature
        ]

        machine_rows.append(
            {
                "Parameter": feature,
                "Current Value": round(
                    value,
                    3,
                ),
            }
        )

    st.dataframe(
        pd.DataFrame(
            machine_rows
        ),
        width="stretch",
        hide_index=True,
        height=250,
    )


with right:

    st.markdown(
        '<div class="section-label">'
        '03 / MACHINE HEALTH'
        '</div>',
        unsafe_allow_html=True,
    )

    status = (
        "NORMAL"
        if assessment["risk_level"] == "LOW"
        else "ATTENTION REQUIRED"
    )

    prediction_text = (
        "Machine failure risk detected"
        if assessment["machine_failure"]
        else "No machine failure predicted"
    )

    st.markdown(
        f"**Machine status:** {status}"
    )

    st.markdown(
        f"**Failure probability:** "
        f"{assessment['failure_probability']:.2%}"
    )

    st.markdown(
        f"**Risk category:** "
        f"{assessment['risk_level']}"
    )

    st.markdown(
        f"**Prediction:** "
        f"{prediction_text}"
    )

    

# ============================================================
# SECTION 04 - AGENT DECISION
# ============================================================

st.markdown(
    '<div class="section-label">'
    '04 / AGENTIC DECISION'
    '</div>',
    unsafe_allow_html=True,
)


if decision:

    action = decision.action

    if action == "ESCALATE":

        st.warning(
            "Agent recommends escalation to a human engineer."
        )

    elif action == "RECOMMEND":

        st.info(
            "Agent recommends a virtual machine parameter "
            "adjustment for operator review."
        )

    elif action == "AUTO_ACT":

        st.success(
            "Agent selected a virtual action that meets "
            "the automatic-action policy."
        )

    else:

        st.success(
            "No intervention is required under the "
            "current risk policy."
        )

    # --------------------------------------------------------
    # CHOSEN SCENARIO
    # --------------------------------------------------------

    if decision.chosen_scenario:

        scenario = decision.chosen_scenario

        direction = (
            "increase"
            if scenario["delta"] > 0
            else "reduce"
        )

        amount = abs(
            scenario["delta"]
        )

        selected_risk = (
            scenario[
                "predicted_failure_probability"
            ]
        )

        risk_reduction = (
            scenario[
                "risk_reduction_pp"
            ]
        )

        decision_html = f"""
<div class="decision">

    <b>AGENT DECISION: {action}</b>

    <br><br>

    Virtual action:
    <b>
    {direction} {scenario['param']}
    by {amount:g}
    </b>

    <br>

    New virtual value:
    <b>
    {scenario['new_value']:g}
    </b>

    <br><br>

    Current failure risk:
    <b>
    {decision.baseline_failure_probability:.2%}
    </b>

    →

    Simulated failure risk:
    <b>
    {selected_risk:.2%}
    </b>

    <br>

    Risk reduction:
    <b>
    {risk_reduction:+.2f}
    percentage points
    </b>

    <br>

    Constraint status:
    <b>
    {scenario['constraint_status']}
    </b>

    <br>

    Decision score:
    <b>
    {scenario['decision_score']:.3f}
    </b>

</div>
"""

        st.markdown(
            decision_html,
            unsafe_allow_html=True,
        )

    else:

        st.info(
            "No parameter change is currently recommended."
        )

    # --------------------------------------------------------
    # AGENT RATIONALE
    # --------------------------------------------------------

    with st.expander(
        "Agent rationale"
    ):

        st.write(
            decision.rationale
        )


# ============================================================
# SECTION 05 - DIGITAL TWIN WHAT-IF SCENARIOS
# ============================================================

if decision:

    st.markdown(
        '<div class="section-label">'
        '05 / DIGITAL TWIN WHAT-IF SCENARIOS'
        '</div>',
        unsafe_allow_html=True,
    )

    scenario_table = (
        decision.scenario_table.copy()
    )

    table_columns = [
        "param",
        "delta",
        "new_value",
        "predicted_failure_risk_percent",
        "risk_level",
        "risk_reduction_pp",
        "constraint_status",
        "decision_score",
    ]

    available_columns = [
        column
        for column in table_columns
        if column in scenario_table.columns
    ]

    display_table = scenario_table[
        available_columns
    ].copy()

    display_table.columns = [
        column.replace(
            "_",
            " ",
        ).title()
        for column in display_table.columns
    ]

    st.dataframe(
        display_table,
        width="stretch",
        hide_index=True,
        height=400,
    )

    st.caption(
        "All scenarios are virtual Digital Twin "
        "simulations. They do not modify the physical "
        "machine."
    )


# ============================================================
# SECTION 06 - MODEL EVIDENCE
# ============================================================

st.markdown(
    '<div class="section-label">'
    '06 / MODEL EVIDENCE'
    '</div>',
    unsafe_allow_html=True,
)


# ------------------------------------------------------------
# RANDOM FOREST EVALUATION
# ------------------------------------------------------------

with st.expander(
    "Random Forest evaluation"
):

    metrics = (
        agent.twin.predictor.metrics
    )

    metric_cols = st.columns(4)

    metric_cols[0].metric(
        "Accuracy",
        f"{metrics['accuracy']:.2%}",
    )

    metric_cols[1].metric(
        "Precision",
        f"{metrics['precision']:.2%}",
    )

    metric_cols[2].metric(
        "Recall",
        f"{metrics['recall']:.2%}",
    )

    metric_cols[3].metric(
        "F1 Score",
        f"{metrics['f1']:.2%}",
    )

    st.caption(
        "Because machine failures are relatively rare "
        "in the AI4I dataset, recall and F1 should be "
        "considered alongside accuracy."
    )


# ------------------------------------------------------------
# FEATURE IMPORTANCE
# ------------------------------------------------------------

with st.expander(
    "Feature importance"
):

    importance = pd.Series(
        agent.twin.predictor.get_feature_importance()
    ).sort_values(
        ascending=False
    )

    importance_df = pd.DataFrame(
        {
            "Machine Parameter":
                importance.index,

            "Importance":
                importance.values,
        }
    )

    st.dataframe(
        importance_df,
        width="stretch",
        hide_index=True,
    )

    st.caption(
        "Random Forest feature importance indicates "
        "how useful each input was to the trained model. "
        "It is not proof of causal influence."
    )


# ============================================================
# SECTION 07 - DECISION HISTORY
# ============================================================

if st.session_state.history:

    st.markdown(
        '<div class="section-label">'
        '07 / MONITORING HISTORY'
        '</div>',
        unsafe_allow_html=True,
    )

    history_df = pd.DataFrame(
        st.session_state.history
    )

    history_cols = st.columns(3)

    history_cols[0].metric(
        "Cycles assessed",
        len(history_df),
    )

    history_cols[1].metric(
        "Average failure risk",
        f"{history_df['Failure Risk (%)'].mean():.2f}%",
    )

    history_cols[2].metric(
        "High-risk cycles",
        int(
            (
                history_df["Risk Level"]
                == "HIGH"
            ).sum()
        ),
    )

    st.dataframe(
        history_df,
        width="stretch",
        hide_index=True,
    )

    if len(history_df) >= 2:

        st.line_chart(
            history_df.set_index(
                "Cycle"
            )[
                "Failure Risk (%)"
            ],
            height=250,
        )


# ============================================================
# HOW THE SYSTEM WORKS
# ============================================================



# ============================================================
# CONTINUOUS AUTOMATIC MONITORING LOOP
# ============================================================

if st.session_state.running:

    time.sleep(
        refresh_secs
    )

    st.rerun()