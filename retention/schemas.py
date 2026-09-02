from __future__ import annotations

from dataclasses import dataclass
from typing import Any


ALLOWED_VALUES = {
    "gender": {"Male", "Female"},
    "SeniorCitizen": {"Yes", "No"},
    "Partner": {"Yes", "No"},
    "Dependents": {"Yes", "No"},
    "PhoneService": {"Yes", "No"},
    "MultipleLines": {"Yes", "No", "No phone service"},
    "InternetService": {"DSL", "Fiber optic", "No"},
    "OnlineSecurity": {"Yes", "No", "No internet service"},
    "OnlineBackup": {"Yes", "No", "No internet service"},
    "DeviceProtection": {"Yes", "No", "No internet service"},
    "TechSupport": {"Yes", "No", "No internet service"},
    "StreamingTV": {"Yes", "No", "No internet service"},
    "StreamingMovies": {"Yes", "No", "No internet service"},
    "Contract": {"Month-to-month", "One year", "Two year"},
    "PaperlessBilling": {"Yes", "No"},
    "PaymentMethod": {
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)",
    },
}


@dataclass(frozen=True)
class CustomerInput:
    customer_reference: str
    model_features: dict[str, Any]


def _required_text(payload: dict[str, Any], name: str) -> str:
    value = str(payload.get(name, "")).strip()
    if not value:
        raise ValueError(f"{name} is required.")
    return value


def _choice(payload: dict[str, Any], name: str) -> str:
    value = _required_text(payload, name)
    if value not in ALLOWED_VALUES[name]:
        raise ValueError(f"{name} contains an unsupported value.")
    return value


def _integer(
    payload: dict[str, Any],
    name: str,
    *,
    minimum: int,
    maximum: int,
) -> int:
    try:
        value = int(payload.get(name, ""))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a whole number.") from exc

    if value < minimum or value > maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}.")

    return value


def _number(
    payload: dict[str, Any],
    name: str,
    *,
    minimum: float,
    maximum: float,
) -> float:
    try:
        value = float(payload.get(name, ""))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric.") from exc

    if value < minimum or value > maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}.")

    return value


def parse_customer_input(payload: dict[str, Any]) -> CustomerInput:
    reference = str(payload.get("customer_reference", "")).strip()
    customer_reference = reference or "Anonymous customer"

    features = {
        "gender": _choice(payload, "gender"),
        "SeniorCitizen": _choice(payload, "SeniorCitizen"),
        "Partner": _choice(payload, "Partner"),
        "Dependents": _choice(payload, "Dependents"),
        "tenure": _integer(payload, "tenure", minimum=0, maximum=100),
        "PhoneService": _choice(payload, "PhoneService"),
        "MultipleLines": _choice(payload, "MultipleLines"),
        "InternetService": _choice(payload, "InternetService"),
        "OnlineSecurity": _choice(payload, "OnlineSecurity"),
        "OnlineBackup": _choice(payload, "OnlineBackup"),
        "DeviceProtection": _choice(payload, "DeviceProtection"),
        "TechSupport": _choice(payload, "TechSupport"),
        "StreamingTV": _choice(payload, "StreamingTV"),
        "StreamingMovies": _choice(payload, "StreamingMovies"),
        "Contract": _choice(payload, "Contract"),
        "PaperlessBilling": _choice(payload, "PaperlessBilling"),
        "PaymentMethod": _choice(payload, "PaymentMethod"),
        "MonthlyCharges": _number(
            payload,
            "MonthlyCharges",
            minimum=0,
            maximum=100000,
        ),
        "TotalCharges": _number(
            payload,
            "TotalCharges",
            minimum=0,
            maximum=10000000,
        ),
    }

    return CustomerInput(
        customer_reference=customer_reference,
        model_features=features,
    )
