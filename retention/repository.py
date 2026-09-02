from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from retention.db import database_connection
from retention.model_service import RetentionAssessment
from retention.schemas import CustomerInput


def save_assessment(
    *,
    database_path: Path,
    customer: CustomerInput,
    assessment: RetentionAssessment,
) -> int:
    features = customer.model_features
    created_at = datetime.now(timezone.utc).isoformat()

    with database_connection(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO assessments (
                customer_reference,
                contract,
                tenure,
                monthly_charges,
                total_charges,
                churn_probability,
                prediction,
                risk_level,
                estimated_monthly_revenue_at_risk,
                primary_driver,
                recommended_action,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                customer.customer_reference,
                features["Contract"],
                features["tenure"],
                features["MonthlyCharges"],
                features["TotalCharges"],
                assessment.churn_probability,
                assessment.prediction,
                assessment.risk_level,
                assessment.estimated_monthly_revenue_at_risk,
                assessment.primary_driver,
                assessment.recommended_action,
                created_at,
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)


def latest_assessments(
    *,
    database_path: Path,
    limit: int = 50,
) -> list[dict[str, Any]]:
    with database_connection(database_path) as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM assessments
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [dict(row) for row in rows]


def dashboard_summary(database_path: Path) -> dict[str, Any]:
    with database_connection(database_path) as connection:
        summary = connection.execute(
            """
            SELECT
                COUNT(*) AS total_assessments,
                SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END) AS high_risk,
                SUM(CASE WHEN risk_level = 'Medium' THEN 1 ELSE 0 END) AS medium_risk,
                SUM(CASE WHEN risk_level = 'Low' THEN 1 ELSE 0 END) AS low_risk,
                COALESCE(SUM(estimated_monthly_revenue_at_risk), 0) AS revenue_at_risk,
                COALESCE(AVG(churn_probability), 0) AS average_probability
            FROM assessments
            """
        ).fetchone()

        risk_rows = connection.execute(
            """
            SELECT risk_level, COUNT(*) AS customers
            FROM assessments
            GROUP BY risk_level
            """
        ).fetchall()

        contract_rows = connection.execute(
            """
            SELECT contract, COUNT(*) AS customers,
                   AVG(churn_probability) AS average_probability
            FROM assessments
            GROUP BY contract
            ORDER BY customers DESC
            """
        ).fetchall()

    risk_distribution = {row["risk_level"]: row["customers"] for row in risk_rows}

    return {
        "total_assessments": int(summary["total_assessments"] or 0),
        "high_risk": int(summary["high_risk"] or 0),
        "medium_risk": int(summary["medium_risk"] or 0),
        "low_risk": int(summary["low_risk"] or 0),
        "revenue_at_risk": round(float(summary["revenue_at_risk"] or 0), 2),
        "average_probability": round(float(summary["average_probability"] or 0), 4),
        "risk_distribution": {
            "High": int(risk_distribution.get("High", 0)),
            "Medium": int(risk_distribution.get("Medium", 0)),
            "Low": int(risk_distribution.get("Low", 0)),
        },
        "contract_performance": [
            {
                "contract": row["contract"],
                "customers": int(row["customers"]),
                "average_probability": round(
                    float(row["average_probability"] or 0) * 100,
                    1,
                ),
            }
            for row in contract_rows
        ],
    }
