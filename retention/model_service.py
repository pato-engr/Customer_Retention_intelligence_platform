from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import RLock
from typing import Any

import joblib
import pandas as pd


@dataclass(frozen=True)
class RetentionAssessment:
    prediction: str
    churn_probability: float
    retention_probability: float
    risk_level: str
    estimated_monthly_revenue_at_risk: float
    primary_driver: str
    recommended_action: str
    driver_summary: list[str]


class ModelService:
    def __init__(self) -> None:
        self._lock = RLock()
        self._model: Any | None = None
        self._loaded_path: Path | None = None

    def load(self, model_path: Path) -> Any:
        with self._lock:
            if self._model is None or self._loaded_path != model_path:
                if not model_path.exists():
                    raise FileNotFoundError(
                        f"Churn model was not found at {model_path}."
                    )

                self._model = joblib.load(model_path)
                self._loaded_path = model_path

            return self._model

    def assess(
        self,
        *,
        model_path: Path,
        features: dict[str, Any],
    ) -> RetentionAssessment:
        model = self.load(model_path)
        frame = pd.DataFrame([features])

        probability = float(model.predict_proba(frame)[0][1])
        probability = min(max(probability, 0.0), 1.0)

        if probability >= 0.70:
            risk_level = "High"
        elif probability >= 0.40:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        prediction = "Likely to churn" if probability >= 0.50 else "Likely to stay"

        drivers = self._retention_drivers(features)
        primary_driver = drivers[0] if drivers else "No dominant rule-based driver detected"

        recommended_action = self._recommended_action(
            risk_level=risk_level,
            features=features,
        )

        monthly_charges = float(features["MonthlyCharges"])
        revenue_at_risk = monthly_charges * probability

        return RetentionAssessment(
            prediction=prediction,
            churn_probability=round(probability, 6),
            retention_probability=round(1.0 - probability, 6),
            risk_level=risk_level,
            estimated_monthly_revenue_at_risk=round(revenue_at_risk, 2),
            primary_driver=primary_driver,
            recommended_action=recommended_action,
            driver_summary=drivers[:4],
        )

    @staticmethod
    def _retention_drivers(features: dict[str, Any]) -> list[str]:
        drivers: list[str] = []

        if features["Contract"] == "Month-to-month":
            drivers.append("Month-to-month contract increases switching flexibility")

        if int(features["tenure"]) <= 12:
            drivers.append("Short customer tenure indicates an early-lifecycle relationship")

        if features["TechSupport"] == "No":
            drivers.append("No technical-support subscription may reduce service attachment")

        if features["OnlineSecurity"] == "No":
            drivers.append("No online-security service may reduce product stickiness")

        if features["PaymentMethod"] == "Electronic check":
            drivers.append("Electronic-check payment is associated with a higher-risk segment")

        if float(features["MonthlyCharges"]) >= 80:
            drivers.append("High monthly charges may increase price sensitivity")

        if features["Contract"] in {"One year", "Two year"}:
            drivers.append("Long-term contract supports retention")

        if int(features["tenure"]) >= 36:
            drivers.append("Long tenure indicates an established customer relationship")

        return drivers

    @staticmethod
    def _recommended_action(
        *,
        risk_level: str,
        features: dict[str, Any],
    ) -> str:
        if risk_level == "High":
            if features["Contract"] == "Month-to-month":
                return (
                    "Contact within 24 hours and offer a contract-conversion "
                    "or loyalty incentive with a clearly measured retention outcome."
                )

            return (
                "Assign to a retention specialist, review recent service issues "
                "and present a personalised save offer."
            )

        if risk_level == "Medium":
            return (
                "Trigger a proactive service check, collect satisfaction feedback "
                "and offer the most relevant support or product bundle."
            )

        return (
            "Maintain standard engagement, monitor future changes and avoid "
            "unnecessary discounting."
        )


model_service = ModelService()
