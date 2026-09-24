\# AgentTwinDefect AI



\## An Agentic Digital Twin Platform for Real-Time Hidden Defect Prediction in Smart Manufacturing



\---



\## Project Information



\*\*Project Title:\*\*  

AgentTwinDefect AI: An Agentic Digital Twin Platform for Real-Time Hidden Defect Prediction in Smart Manufacturing



\*\*Course:\*\*  

SOA Programming and Microservices



\*\*Course Code:\*\*  

24SDCS03



\*\*Project Review:\*\*  

Review-II



\*\*Department:\*\*  

Department of Computer Science and Engineering



\*\*Campus:\*\*  

KLH CSE Bowrampet Campus



\*\*Guide:\*\*  

Dr. Srikanth Cherukuvada  

Assistant Professor  

Department of Computer Science and Engineering  

KLH CSE Bowrampet Campus



\---



\## Team Members



| S. No. | Name | Roll Number |

|---|---|---|

| 1 | S. Sushmita | 2420090076 |

| 2 | P. Goda Sahasra | 2420090128 |

| 3 | K. Amulya | 2420090132 |



\---



\# 1. Project Overview



AgentTwinDefect AI is an AI-enabled Digital Twin platform designed for smart manufacturing.



The project addresses an important problem in manufacturing:



> Manufacturing systems can monitor machine conditions and predict failures or defects, but prediction alone does not provide sufficient support for understanding possible causes, evaluating corrective actions, and deciding what action should be taken.



AgentTwinDefect AI combines:



\- Predictive Machine Learning

\- Digital Twin representation

\- What-if simulation

\- Scenario comparison

\- Agentic decision support

\- Continuous monitoring

\- Interactive visualization



The central idea of the project is:



```text

Predict

&#x20;  ↓

Simulate

&#x20;  ↓

Compare

&#x20;  ↓

Decide

2\. Problem Statement



Modern smart manufacturing systems generate large volumes of data from sensors, machines, and production processes.



Although Machine Learning and Digital Twin technologies can be used for monitoring and prediction, these capabilities are often implemented separately. Existing systems may detect anomalies or predict failures but provide limited support for identifying probable causes and evaluating corrective actions before applying them to the physical process.



The key problem addressed by AgentTwinDefect AI is:



The absence of an integrated intelligent framework that can continuously monitor manufacturing processes, predict emerging problems, evaluate possible corrective actions using a Digital Twin, and recommend an appropriate intervention.



The project therefore connects:



Manufacturing Data

&#x20;      ↓

Prediction

&#x20;      ↓

Digital Twin

&#x20;      ↓

What-if Simulation

&#x20;      ↓

Scenario Comparison

&#x20;      ↓

Agentic Decision

3\. Project Motivation



A prediction system may tell an operator:



Machine Failure Risk = HIGH



However, the operator may still need to determine:



What caused the increased risk?

Which machine parameter should be changed?

Will changing that parameter reduce the risk?

Which possible change is safer?

Which intervention should be considered?



AgentTwinDefect AI attempts to address this decision gap.



Instead of stopping at:



Prediction → Alert



the project extends the workflow to:



Prediction

&#x20;   ↓

Virtual Intervention

&#x20;   ↓

Scenario Evaluation

&#x20;   ↓

Decision Support

4\. Project Objectives



The main objectives are:



Develop an AI-based machine-condition monitoring system.

Predict machine failure using machine operating parameters.

Calculate machine failure probability and risk level.

Represent the current machine condition using a Digital Twin.

Perform what-if simulations without changing the physical machine.

Generate multiple possible parameter-change scenarios.

Compare scenarios using predicted risk, risk reduction, cost, and constraints.

Implement an agentic decision-support layer.

Continuously process simulated machine observations.

Provide an interactive dashboard for monitoring and analysis.

5\. Project Architecture

&#x20;                        AI4I DATASET

&#x20;                             |

&#x20;                             v

&#x20;                       DATA LOADER

&#x20;                             |

&#x20;                             v

&#x20;                  MACHINE CONDITION DATA

&#x20;                             |

&#x20;                             v

&#x20;                    RANDOM FOREST MODEL

&#x20;                             |

&#x20;                             v

&#x20;                  MACHINE FAILURE RISK

&#x20;                             |

&#x20;                             v

&#x20;                      DIGITAL TWIN

&#x20;                             |

&#x20;                   +---------+---------+

&#x20;                   |         |         |

&#x20;                   v         v         v

&#x20;                Scenario   Scenario   Scenario

&#x20;                   |         |         |

&#x20;                   +---------+---------+

&#x20;                             |

&#x20;                             v

&#x20;                    SCENARIO ENGINE

&#x20;                             |

&#x20;                             v

&#x20;                   AGENTIC DECISION LAYER

&#x20;                             |

&#x20;            +----------------+----------------+

&#x20;            |                |                |

&#x20;            v                v                v

&#x20;      NO ACTION          RECOMMEND         ESCALATE

&#x20;            |

&#x20;            v

&#x20;                    STREAMLIT DASHBOARD

6\. End-to-End Workflow



The complete implementation follows:



AI4I Machine Data

&#x20;       ↓

Data Validation

&#x20;       ↓

Feature Selection

&#x20;       ↓

Random Forest Prediction

&#x20;       ↓

Failure Probability

&#x20;       ↓

Digital Twin Machine State

&#x20;       ↓

What-if Scenario Generation

&#x20;       ↓

Scenario Risk Evaluation

&#x20;       ↓

Scenario Comparison

&#x20;       ↓

Agentic Decision

&#x20;       ↓

Dashboard Visualization

&#x20;       ↓

Next Machine Observation

&#x20;       ↓

Repeat

7\. Current Implementation



The current executable prototype uses the:



AI4I 2020 Predictive Maintenance Dataset



The dataset is used to demonstrate the machine-condition monitoring and failure-prediction part of the overall AgentTwinDefect AI architecture.



The current implementation predicts:



Machine Failure



rather than a specific product-defect category.



The architecture can be extended later with additional manufacturing quality-defect datasets.



8\. Dataset

AI4I 2020 Predictive Maintenance Dataset



The AI4I dataset contains machine operating parameters and failure information.



The project uses the following five primary machine-condition parameters:



1\. Air temperature \[K]

2\. Process temperature \[K]

3\. Rotational speed \[rpm]

4\. Torque \[Nm]

5\. Tool wear \[min]

Target

Machine failure



The target indicates whether a machine failure occurred.



Dataset Size

10,000 records



The dataset contains significantly more normal observations than failure observations.



Therefore, model evaluation considers:



Accuracy

Precision

Recall

F1 Score

Confusion Matrix



rather than relying only on accuracy.



9\. Why These Features Are Used



The predictive model uses:



Air temperature

Process temperature

Rotational speed

Torque

Tool wear



These variables represent important machine operating and condition measurements.



The following columns are not used as the primary model inputs:



UDI

Product ID

TWF

HDF

PWF

OSF

RNF



The failure-mode columns are kept outside the primary prediction features to avoid target-related information leakage.



10\. Technology Stack

Technology	Purpose

Python	Main programming language

Pandas	Data loading, cleaning and processing

Scikit-learn	Machine Learning

Random Forest Classifier	Machine failure prediction

Streamlit	Interactive monitoring dashboard

Matplotlib/Streamlit Charts	Data visualization

Git	Version control

GitHub	Source-code repository and project submission

AI4I Dataset	Predictive-maintenance machine data

VS Code	Development environment

11\. Software Architecture



The project is organized into modular Python components.



agenttwindefect/

│

├── agenttwindefect/

│   ├── \_\_init\_\_.py

│   ├── agent.py

│   ├── data\_loader.py

│   ├── defect\_model.py

│   ├── digital\_twin.py

│   ├── live\_stream.py

│   ├── pipeline.py

│   ├── scenario\_engine.py

│   └── validation.py

│

├── data/

│   └── ai4i.csv

│

├── dashboard.py

│

└── README.md

12\. Module Description

12.1 data\_loader.py

Purpose



Loads and validates the AI4I dataset.



Responsibilities

Locate the dataset.

Load the CSV file using Pandas.

Validate required columns.

Validate machine-condition values.

Validate the Machine failure target.

Define the model features.

Provide the dataset to other modules.

Main components

FEATURE\_COLUMNS

TARGET\_COLUMN

load\_dataset()

13\. defect\_model.py

Machine Failure Prediction Model



The file contains the:



MachineFailureModel



The model uses:



RandomForestClassifier



from Scikit-learn.



Model Input

Air temperature

Process temperature

Rotational speed

Torque

Tool wear

Model Output

Machine failure prediction

Failure probability

Failure risk percentage

Risk status

Model Evaluation



The implementation calculates:



Accuracy

Precision

Recall

F1 Score

Confusion Matrix

Classification Report

Feature Importance

Class Imbalance



The AI4I dataset contains relatively few failure observations compared with normal observations.



The model therefore uses:



class\_weight="balanced"



to give additional importance to the minority failure class during training.



14\. digital\_twin.py

Data-Driven Digital Twin



The Digital Twin module represents the machine's current operating state.



The machine state contains:



Air temperature

Process temperature

Rotational speed

Torque

Tool wear



The state is represented using:



ProcessState



The Digital Twin supports:



Current state assessment

What-if simulation

Failure-risk comparison

Risk-level classification

15\. What-if Simulation



The Digital Twin allows virtual changes to selected machine parameters.



For example:



Current state:



Rotational speed = 1551 rpm



A virtual scenario can test:



Rotational speed = 1451 rpm



The physical machine is not changed.



The predictive model evaluates:



Before:

Failure Risk = X%



After:

Failure Risk = Y%



The system can then calculate the change in risk.



This allows possible interventions to be evaluated virtually before any real machine modification.



16\. scenario\_engine.py



The Scenario Engine generates and evaluates multiple virtual machine-parameter changes.



Example scenarios:



Rotational speed -200 rpm

Rotational speed -100 rpm

Rotational speed +100 rpm

Rotational speed +200 rpm



Similar virtual changes are generated for selected parameters such as:



Air temperature

Process temperature

Torque



Each scenario is evaluated using:



Predicted failure probability

Predicted failure risk

Risk change

Risk reduction

Adjustment cost

Constraint validity

Decision score



The resulting scenarios are compared and passed to the agentic decision layer.



17\. validation.py



The validation module checks whether machine states and proposed parameter changes satisfy predefined constraints.



Examples include:



Temperature limits

Speed limits

Torque limits

Tool-wear limits



The validation layer helps prevent invalid virtual machine states.



A proposed scenario can be marked:



VALID



or:



REJECTED



depending on whether it satisfies the defined constraints.



18\. agent.py

Agentic Decision Layer



The agentic layer is implemented as a rule-based decision engine in the current prototype.



It evaluates:



Current failure probability

&#x20;       +

Candidate scenarios

&#x20;       +

Risk reduction

&#x20;       +

Adjustment cost

&#x20;       +

Constraint validity



The agent then produces a policy-based decision.



Decision Types

NO\_ACTION\_NEEDED

RECOMMEND

AUTO\_ACT

ESCALATE

NO\_ACTION\_NEEDED



The current risk is low and no sufficiently useful intervention is identified.



RECOMMEND



A virtual intervention provides sufficient improvement and should be reviewed by an operator.



AUTO\_ACT



A virtual intervention satisfies the predefined automatic-action policy.



In the current prototype, this does not physically control a machine.



ESCALATE



The situation requires human engineering review.



19\. Important Note About the Agent



The current agentic layer is:



Rule-Based Decision Engine



It is not currently an LLM-based agent.



The agent performs task-oriented decision-making using predefined:



Risk thresholds

Cost thresholds

Scenario scores

Constraint checks



An LLM-based reasoning agent can be considered as future work.



20\. pipeline.py



The pipeline module demonstrates the complete end-to-end workflow.



It:



Loads the AI4I dataset.

Trains the Random Forest model.

Creates the Digital Twin.

Creates the agent.

Creates machine states.

Predicts failure risk.

Generates what-if scenarios.

Compares scenarios.

Produces an agentic decision.

21\. dashboard.py



The Streamlit dashboard provides the main user interface.



The dashboard displays:



Current Machine State

Cycle

Failure Risk

Risk Level

Prediction

Model Confidence

Machine Input Signals

Air temperature

Process temperature

Rotational speed

Torque

Tool wear

Machine Health

Machine status

Failure probability

Risk category

Prediction

Agentic Decision

NO\_ACTION\_NEEDED

RECOMMEND

AUTO\_ACT

ESCALATE

Digital Twin



The dashboard displays the virtual scenarios generated by the Digital Twin.



Model Evidence



The dashboard displays:



Accuracy

Precision

Recall

F1 Score

Feature Importance

Monitoring History



The dashboard stores and displays previous machine cycles and failure-risk values.



22\. Continuous Monitoring



The dashboard provides:



Run

Pause

Reset

Run



Starts continuous machine-observation processing.



The system automatically performs:



Read observation

&#x20;      ↓

Predict

&#x20;      ↓

Digital Twin

&#x20;      ↓

Scenario simulation

&#x20;      ↓

Agent decision

&#x20;      ↓

Dashboard update

&#x20;      ↓

Read next observation

&#x20;      ↓

Repeat

Pause



Stops processing new observations while keeping the current dashboard state.



Reset



Resets:



Dataset position

Monitoring history

Current decision

Running state

23\. Simulated Sensor Stream



The current implementation does not connect to a physical industrial sensor.



Instead, the AI4I CSV records are processed sequentially to simulate incoming machine observations.



Therefore:



AI4I CSV

&#x20;  ↓

Record 1

&#x20;  ↓

Record 2

&#x20;  ↓

Record 3

&#x20;  ↓

...



acts as a simulated sensor stream.



This allows continuous monitoring behavior to be demonstrated without requiring physical manufacturing equipment.



24\. Model Performance



The Random Forest model is evaluated using a stratified train-test split.



The current test split contains:



2,000 test observations



The observed confusion matrix is:



\[\[1927,    5],

&#x20;\[  29,   39]]



The project therefore reports:



Accuracy

Precision

Recall

F1 Score



The failure class is more difficult to detect than the normal class, so accuracy should not be interpreted alone.



The current implementation does not claim perfect failure detection.



25\. Project Novelty



The main contribution of AgentTwinDefect AI is not simply the use of Random Forest.



The main contribution is the integration of:



Predictive AI

&#x20;     +

Digital Twin

&#x20;     +

What-if Simulation

&#x20;     +

Scenario Comparison

&#x20;     +

Agentic Decision Support



The system moves from:



Prediction Only



toward:



Prediction

&#x20;   ↓

Virtual Intervention

&#x20;   ↓

Scenario Evaluation

&#x20;   ↓

Scenario Comparison

&#x20;   ↓

Agentic Decision



The key project concept is:



Prediction identifies the risk, the Digital Twin evaluates possible virtual interventions, and the agentic layer supports the decision about what action should be considered.



26\. Relation to the Base Paper



The project is based on the concepts presented in:



Dai et al. (2025)



"Generative and Predictive AI for Digital Twin Systems in Manufacturing."



The base paper presents an AI-enabled Digital Twin architecture for manufacturing and discusses Predictive AI and Generative AI while identifying Agentic AI as a future extension.



The base paper demonstrates AI-enabled Digital Twin concepts and predictive defect detection in a welding context.



AgentTwinDefect AI extends the architecture toward agentic decision support:



Predictive AI

&#x20;     ↓

Digital Twin

&#x20;     ↓

What-if Simulation

&#x20;     ↓

Scenario Comparison

&#x20;     ↓

Agentic Decision



The current implementation adapts the concept to machine-condition monitoring using the AI4I predictive-maintenance dataset.



It is therefore an implementation and extension of the AI-enabled Digital Twin concept rather than a direct reproduction of the base paper's welding dataset and model.



27\. Research Gap



The project addresses the gap between:



Prediction



and:



Decision-making



The intended integrated workflow is:



Monitor

&#x20;  ↓

Predict

&#x20;  ↓

Diagnose / Analyze

&#x20;  ↓

Simulate

&#x20;  ↓

Compare

&#x20;  ↓

Recommend



The project focuses particularly on connecting predictive machine learning with Digital Twin what-if simulation and agentic decision support.



28\. Significance



The project is intended to support:



Early Detection



Identify potential machine-failure risks before failure occurs.



Decision Support



Provide possible actions rather than only producing an alert.



What-if Analysis



Evaluate possible parameter changes virtually.



Reduced Trial-and-Error



Allow possible interventions to be evaluated before considering physical implementation.



Smart Manufacturing



Provide a modular architecture that can be extended with additional machines, sensors, models and production lines.



29\. Complete Technology Stack

Programming Language

&#x20;       |

&#x20;       +-- Python



Data Processing

&#x20;       |

&#x20;       +-- Pandas



Machine Learning

&#x20;       |

&#x20;       +-- Scikit-learn

&#x20;       +-- Random Forest Classifier



Digital Twin

&#x20;       |

&#x20;       +-- Python

&#x20;       +-- Data-driven machine-state representation



Scenario Engine

&#x20;       |

&#x20;       +-- Python

&#x20;       +-- Pandas



Agentic Layer

&#x20;       |

&#x20;       +-- Python

&#x20;       +-- Rule-based decision policies



Dashboard

&#x20;       |

&#x20;       +-- Streamlit



Dataset

&#x20;       |

&#x20;       +-- AI4I 2020 Predictive Maintenance Dataset



Development

&#x20;       |

&#x20;       +-- VS Code



Version Control

&#x20;       |

&#x20;       +-- Git

&#x20;       +-- GitHub

30\. Requirements



Recommended environment:



Python 3.10+



Required Python packages:



pandas

scikit-learn

streamlit

31\. Installation

Step 1: Clone the repository

git clone <YOUR\_GITHUB\_REPOSITORY\_URL>



Example:



git clone https://github.com/your-username/agenttwindefect.git

Step 2: Enter the project folder

cd agenttwindefect

Step 3: Create a virtual environment



Windows:



python -m venv .venv



Activate it:



.venv\\Scripts\\activate



If PowerShell is being used:



.\\.venv\\Scripts\\Activate.ps1

Step 4: Upgrade pip

python -m pip install --upgrade pip

Step 5: Install dependencies

pip install pandas scikit-learn streamlit



Or:



python -m pip install pandas scikit-learn streamlit

32\. Dataset Setup



Make sure the AI4I dataset is placed at:



agenttwindefect/

│

├── data/

│   └── ai4i.csv



The final path should be:



data/ai4i.csv



The application automatically locates the dataset relative to the project directory.



33\. Verify Dataset Loading



Run:



python -m agenttwindefect.data\_loader



Expected output includes:



AI4I DATASET LOADED SUCCESSFULLY



and:



Dataset shape: (10000, ...)



The command also displays the selected machine features and machine-failure counts.



34\. Test the Machine Failure Model



Run:



python -m agenttwindefect.defect\_model



This will:



Load the dataset.

Train the Random Forest.

Evaluate the model.

Print accuracy.

Print precision.

Print recall.

Print F1 score.

Print feature importance.

Print the classification report.

Print the confusion matrix.

Generate a sample prediction.

35\. Test the Digital Twin



Run:



python -m agenttwindefect.digital\_twin



This demonstrates:



Current Machine State

&#x20;       ↓

Current Failure Risk

&#x20;       ↓

Virtual Parameter Change

&#x20;       ↓

New Failure Risk

&#x20;       ↓

Risk Difference

36\. Test the Scenario Engine



Run:



python -m agenttwindefect.scenario\_engine



This generates multiple what-if scenarios and compares their:



Failure Risk

Risk Reduction

Adjustment Cost

Constraint Status

Decision Score

37\. Test the Agent



Run:



python -m agenttwindefect.agent



This demonstrates the agentic decision process.



The output may contain:



NO\_ACTION\_NEEDED

RECOMMEND

AUTO\_ACT

ESCALATE



depending on the machine state and scenario results.



38\. Run the Complete Pipeline



Run:



python -m agenttwindefect.pipeline



The pipeline demonstrates:



Dataset

&#x20;  ↓

Model

&#x20;  ↓

Digital Twin

&#x20;  ↓

Scenarios

&#x20;  ↓

Agent

39\. Run the Streamlit Dashboard



From the project root:



python -m streamlit run dashboard.py



Alternatively:



streamlit run dashboard.py



The terminal will provide a local address similar to:



http://localhost:8501



Open that address in a browser.



40\. Dashboard Usage



After opening the dashboard:



Step 1



Press:



Run

Step 2



The system automatically processes machine observations.



Step 3



For every observation:



Machine Input

&#x20;    ↓

Random Forest

&#x20;    ↓

Failure Risk

&#x20;    ↓

Digital Twin

&#x20;    ↓

What-if Scenarios

&#x20;    ↓

Agent

&#x20;    ↓

Dashboard

Step 4



Press:



Pause



to stop the continuous monitoring.



Step 5



Press:



Run



again to continue.



Step 6



Press:



Reset



to restart the monitoring sequence.



41\. Recommended Run Order



For development and testing:



python -m agenttwindefect.data\_loader



Then:



python -m agenttwindefect.defect\_model



Then:



python -m agenttwindefect.digital\_twin



Then:



python -m agenttwindefect.scenario\_engine



Then:



python -m agenttwindefect.agent



Then:



python -m agenttwindefect.pipeline



Finally:



python -m streamlit run dashboard.py

42\. Git and GitHub Commands



Initialize Git if required:



git init



Check repository status:



git status



Add project files:



git add .



Commit:



git commit -m "Implement AgentTwinDefect AI Review-II prototype"



Add the GitHub repository:



git remote add origin <YOUR\_GITHUB\_REPOSITORY\_URL>



Push:



git branch -M main

git push -u origin main



For future updates:



git add .

git commit -m "Update AgentTwinDefect AI implementation"

git push

43\. Project Folder Structure

agenttwindefect/

│

├── agenttwindefect/

│   ├── \_\_init\_\_.py

│   │

│   ├── agent.py

│   │   └── Agentic decision layer

│   │

│   ├── data\_loader.py

│   │   └── AI4I dataset loading and validation

│   │

│   ├── defect\_model.py

│   │   └── Random Forest machine-failure prediction

│   │

│   ├── digital\_twin.py

│   │   └── Data-driven Digital Twin

│   │

│   ├── live\_stream.py

│   │   └── Stream-related module

│   │

│   ├── pipeline.py

│   │   └── End-to-end pipeline

│   │

│   ├── scenario\_engine.py

│   │   └── What-if scenario generation and comparison

│   │

│   └── validation.py

│       └── Machine-state and parameter validation

│

├── data/

│   └── ai4i.csv

│

├── dashboard.py

│   └── Streamlit monitoring interface

│

└── README.md

44\. Limitations



The current prototype has several limitations.



1\. Simulated Data Stream



The dashboard currently uses sequential AI4I CSV records instead of physical sensor data.



2\. Data-Driven Digital Twin



The current Digital Twin is data-driven and does not contain a physics-based simulation model.



3\. Machine Failure Target



The current implementation predicts machine failure using AI4I rather than a detailed hidden product-defect taxonomy.



4\. Rule-Based Agent



The current agentic layer uses predefined decision policies rather than an LLM-based autonomous agent.



5\. No Physical Machine Control



The current prototype does not directly control manufacturing equipment.



6\. Dataset Imbalance



Failure observations are much less frequent than normal observations, which affects failure-class prediction performance.



45\. Future Scope



Future versions can extend the system with:



Real-time IoT sensor integration.

Physical manufacturing-machine connectivity.

Physics-based Digital Twin models.

Explainable AI.

Root-cause analysis.

Context-aware decision-making.

LLM-based agentic reasoning.

Multi-agent architecture.

Real-time corrective-action optimization.

Industrial control-system integration.

Additional manufacturing quality datasets.

Advanced deep-learning models.

Edge computing and cloud deployment.

Real production-line validation.

46\. Safety Considerations



AgentTwinDefect AI is currently a research prototype and decision-support system.



The current:



AUTO\_ACT



decision is a virtual policy decision only.



It does not physically modify a machine.



Any real-world deployment would require:



Industrial safety validation

Sensor validation

Control-system integration

Human approval

Fail-safe mechanisms

Controlled testing

Manufacturing-domain validation

47\. Base Paper



The project is based on:



Dai et al. (2025)



Generative and Predictive AI for Digital Twin Systems in Manufacturing



Frontiers in Artificial Intelligence



DOI:



10.3389/frai.2025.1655470

48\. Project Contribution



The project contribution can be summarized as:



Machine Monitoring

&#x20;      ↓

Predictive AI

&#x20;      ↓

Failure Risk

&#x20;      ↓

Digital Twin

&#x20;      ↓

What-if Simulation

&#x20;      ↓

Scenario Comparison

&#x20;      ↓

Agentic Decision Support



The central contribution is the integration of prediction, virtual intervention testing, quantitative scenario comparison, and agentic decision support.



49\. One-Line Project Definition



AgentTwinDefect AI is a data-driven agentic Digital Twin platform that predicts machine failure risk, evaluates possible virtual interventions, compares their outcomes, and provides decision support for smart manufacturing.



50\. Viva Summary



If asked to explain the project in a few sentences:



“AgentTwinDefect AI is an agentic Digital Twin platform for smart manufacturing. We use the AI4I predictive-maintenance dataset and a Random Forest model to predict machine failure risk from machine-condition parameters. Our Digital Twin represents the current machine state and performs what-if simulations of possible parameter changes. The Scenario Engine compares these virtual interventions using risk, risk reduction, cost and constraints. Finally, the agentic decision layer produces a policy-based decision such as no action, recommend, auto-act or escalate. The complete workflow is demonstrated through a Streamlit dashboard with continuous simulated machine-data processing.”



51\. Core Concept

&#x20;                   AGENTTWINDEFECT AI



&#x20;                        MACHINE DATA

&#x20;                             |

&#x20;                             v

&#x20;                      PREDICTIVE AI

&#x20;                             |

&#x20;                             v

&#x20;                      FAILURE RISK

&#x20;                             |

&#x20;                             v

&#x20;                      DIGITAL TWIN

&#x20;                             |

&#x20;                             v

&#x20;                     WHAT-IF SIMULATION

&#x20;                             |

&#x20;                             v

&#x20;                   SCENARIO COMPARISON

&#x20;                             |

&#x20;                             v

&#x20;                    AGENTIC DECISION

&#x20;                             |

&#x20;                             v

&#x20;                     DECISION SUPPORT

Predict → Simulate → Compare → Decide

Team



S. Sushmita — 2420090076

P. Goda Sahasra — 2420090128

K. Amulya — 2420090132



Under the Guidance of



Dr. Srikanth Cherukuvada

Assistant Professor

Department of Computer Science and Engineering

KLH CSE Bowrampet Campus

