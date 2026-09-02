from __future__ import annotations

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from retention.model_service import model_service
from retention.repository import (
    dashboard_summary,
    latest_assessments,
    save_assessment,
)
from retention.schemas import parse_customer_input


web = Blueprint("web", __name__)


@web.get("/")
def home():
    return render_template("index.html")


@web.post("/assess")
def assess_customer():
    try:
        customer = parse_customer_input(request.form.to_dict())
        assessment = model_service.assess(
            model_path=current_app.config["MODEL_PATH"],
            features=customer.model_features,
        )

        assessment_id = save_assessment(
            database_path=current_app.config["DATABASE_PATH"],
            customer=customer,
            assessment=assessment,
        )

        return redirect(url_for("web.assessment_result", assessment_id=assessment_id))

    except (ValueError, FileNotFoundError) as exc:
        flash(str(exc), "error")
        return redirect(url_for("web.home"))


@web.get("/assessment/<int:assessment_id>")
def assessment_result(assessment_id: int):
    records = latest_assessments(
        database_path=current_app.config["DATABASE_PATH"],
        limit=200,
    )

    record = next(
        (item for item in records if int(item["id"]) == assessment_id),
        None,
    )

    if record is None:
        return render_template(
            "error.html",
            title="Assessment not found",
            message="The requested retention assessment does not exist.",
        ), 404

    return render_template("result.html", assessment=record)


@web.get("/dashboard")
def dashboard():
    summary = dashboard_summary(current_app.config["DATABASE_PATH"])
    recent = latest_assessments(
        database_path=current_app.config["DATABASE_PATH"],
        limit=30,
    )

    return render_template(
        "dashboard.html",
        summary=summary,
        recent=recent,
    )


@web.post("/api/v1/assessments")
def api_assessment():
    payload = request.get_json(silent=True) or {}

    try:
        customer = parse_customer_input(payload)
        assessment = model_service.assess(
            model_path=current_app.config["MODEL_PATH"],
            features=customer.model_features,
        )

        assessment_id = save_assessment(
            database_path=current_app.config["DATABASE_PATH"],
            customer=customer,
            assessment=assessment,
        )

        return jsonify(
            {
                "assessment_id": assessment_id,
                "customer_reference": customer.customer_reference,
                "prediction": assessment.prediction,
                "risk_level": assessment.risk_level,
                "churn_probability": assessment.churn_probability,
                "retention_probability": assessment.retention_probability,
                "estimated_monthly_revenue_at_risk": (
                    assessment.estimated_monthly_revenue_at_risk
                ),
                "primary_driver": assessment.primary_driver,
                "recommended_action": assessment.recommended_action,
                "driver_summary": assessment.driver_summary,
            }
        ), 201

    except (ValueError, FileNotFoundError) as exc:
        return jsonify({"error": str(exc)}), 400


@web.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "customer-retention-intelligence",
    }
