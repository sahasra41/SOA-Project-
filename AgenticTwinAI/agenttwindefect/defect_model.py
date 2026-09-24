from pathlib import Path

import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import train_test_split

from .data_loader import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    load_dataset,
)


class MachineFailureModel:
    """
    Random Forest model for predicting machine failure
    from machine operating parameters.
    """

    def __init__(self, random_state=42):
        self.random_state = random_state

        self.model = RandomForestClassifier(
            n_estimators=200,
            random_state=random_state,
            class_weight="balanced",
            n_jobs=-1,
        )

        self.is_trained = False
        self.feature_importances_ = None
        self.metrics = {}

    # ========================================================
    # TRAIN MODEL
    # ========================================================

    def train(self, df=None):

        if df is None:
            df = load_dataset()

        X = df[FEATURE_COLUMNS]
        y = df[TARGET_COLUMN]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=self.random_state,
            stratify=y,
        )

        self.model.fit(X_train, y_train)

        y_pred = self.model.predict(X_test)

        # ----------------------------------------------------
        # Evaluation metrics
        # ----------------------------------------------------

        self.metrics = {
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(
                y_test,
                y_pred,
                zero_division=0,
            ),
            "recall": recall_score(
                y_test,
                y_pred,
                zero_division=0,
            ),
            "f1": f1_score(
                y_test,
                y_pred,
                zero_division=0,
            ),
            "confusion_matrix": confusion_matrix(
                y_test,
                y_pred,
            ),
            "classification_report": classification_report(
                y_test,
                y_pred,
                zero_division=0,
            ),
        }

        self.feature_importances_ = dict(
            zip(
                FEATURE_COLUMNS,
                self.model.feature_importances_,
            )
        )

        self.is_trained = True

        return self.metrics

    # ========================================================
    # PREDICT MACHINE FAILURE
    # ========================================================

    def predict(self, data):

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained before prediction."
            )

        if isinstance(data, dict):
            data = pd.DataFrame([data])

        X = data[FEATURE_COLUMNS]

        prediction = self.model.predict(X)

        probability = self.model.predict_proba(X)

        return prediction, probability

    # ========================================================
    # PREDICT ONE MACHINE STATE
    # ========================================================

    def predict_state(self, state):

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained before prediction."
            )

        if hasattr(state, "to_dict"):
            data = state.to_dict()
        elif isinstance(state, dict):
            data = state
        else:
            data = vars(state)

        df = pd.DataFrame([data])

        X = df[FEATURE_COLUMNS]

        prediction = int(
            self.model.predict(X)[0]
        )

        probabilities = self.model.predict_proba(X)[0]

        # Probability of class 1 = machine failure
        class_probabilities = dict(
            zip(
                self.model.classes_,
                probabilities,
            )
        )

        failure_probability = float(
            class_probabilities.get(1, 0.0)
        )

        return {
            "machine_failure": prediction,
            "failure_probability": failure_probability,
            "failure_risk_percent": failure_probability * 100,
            "status": (
                "FAILURE_RISK"
                if prediction == 1
                else "NORMAL"
            ),
        }

    # ========================================================
    # FEATURE IMPORTANCE
    # ========================================================

    def get_feature_importance(self):

        if not self.is_trained:
            raise RuntimeError(
                "Model must be trained before "
                "getting feature importance."
            )

        return self.feature_importances_

    # ========================================================
    # PRINT MODEL SUMMARY
    # ========================================================

    def print_summary(self):

        if not self.is_trained:
            print("Model has not been trained yet.")
            return

        print("\nMODEL SUMMARY")
        print("=" * 60)

        print("\nFeatures:")
        for feature in FEATURE_COLUMNS:
            print(f"  - {feature}")

        print(f"\nTarget:")
        print(f"  - {TARGET_COLUMN}")

        print("\nEvaluation Metrics:")
        print(
            f"  Accuracy  : "
            f"{self.metrics['accuracy']:.4f}"
        )
        print(
            f"  Precision : "
            f"{self.metrics['precision']:.4f}"
        )
        print(
            f"  Recall    : "
            f"{self.metrics['recall']:.4f}"
        )
        print(
            f"  F1 Score  : "
            f"{self.metrics['f1']:.4f}"
        )

        print("\nFeature Importance:")
        sorted_features = sorted(
            self.feature_importances_.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        for feature, importance in sorted_features:
            print(
                f"  {feature}: "
                f"{importance:.4f}"
            )

        print("\nClassification Report:")
        print(
            self.metrics[
                "classification_report"
            ]
        )

        print("Confusion Matrix:")
        print(
            self.metrics[
                "confusion_matrix"
            ]
        )


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\nTRAINING MACHINE FAILURE MODEL")
    print("=" * 60)

    dataset = load_dataset()

    model = MachineFailureModel()

    metrics = model.train(dataset)

    model.print_summary()

    # Test prediction using first row
    sample = dataset.iloc[0][FEATURE_COLUMNS].to_dict()

    result = model.predict_state(sample)

    print("\nSAMPLE PREDICTION")
    print("=" * 60)

    print(f"Machine failure : {result['machine_failure']}")
    print(
        f"Failure risk    : "
        f"{result['failure_risk_percent']:.2f}%"
    )
    print(f"Status          : {result['status']}")