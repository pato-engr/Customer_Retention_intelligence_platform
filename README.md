# Customer Retention Intelligence Platform

A business-focused machine-learning application that converts customer churn
probability into risk segmentation, estimated monthly revenue exposure and a
recommended retention action.

## Why this project matters

A basic churn model answers:

> Is this customer likely to leave?

A retention intelligence product must also help answer:

- Which customers should the retention team contact first?
- How much monthly revenue is exposed?
- What customer characteristics may require attention?
- What action should be tested?
- How concentrated is risk across the assessed portfolio?

This project demonstrates the transition from a notebook model to a usable
decision-support application.

## Key capabilities

- Individual churn-risk assessment
- Low, medium and high-risk segmentation
- Probability-weighted monthly revenue at risk
- Transparent rule-based retention signals
- Recommended retention actions
- Persistent SQLite assessment history
- Portfolio dashboard
- Contract-level risk analysis
- JSON API endpoint
- Health endpoint
- Docker and Gunicorn deployment
- Input validation and automated tests

## Technology

- Python
- Flask
- Scikit-learn
- Pandas
- SQLite
- Chart.js
- HTML and CSS
- Docker
- Gunicorn
- Pytest

## Architecture

```text
Customer profile
      ↓
Input validation
      ↓
Saved Scikit-learn pipeline
      ↓
Churn probability
      ↓
Risk segmentation
      ↓
Retention explanation and action
      ↓
SQLite assessment history
      ↓
Portfolio dashboard and API
```

## Important model note

The supplied model is a Scikit-learn logistic-regression pipeline trained with
Scikit-learn 1.7.2. The dependency is pinned to that version to avoid
model-persistence incompatibilities.

The rule-based explanation layer is not a replacement for formal feature-level
explainability. It communicates transparent business signals from the submitted
profile. A production version should add validated SHAP explanations,
calibration analysis, drift monitoring, fairness review and intervention
experimentation.

## Local setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Dashboard:

```text
http://127.0.0.1:5000/dashboard
```

Health:

```text
http://127.0.0.1:5000/health
```

## API

```http
POST /api/v1/assessments
Content-Type: application/json
```

The JSON body uses the same fields as the assessment form.

## Tests

```powershell
pytest
```

## Portfolio presentation

### Problem

Subscription businesses lose recurring revenue when at-risk customers are not
identified and contacted early enough.

### Solution

A customer-retention decision-support platform that estimates churn risk,
segments the customer, calculates revenue exposure and recommends a next action.

### Business value

- Helps prioritise retention outreach
- Connects prediction probability to revenue impact
- Creates a record of assessed customers
- Provides portfolio-level management visibility
- Establishes a foundation for measuring intervention outcomes

### Future production roadmap

- Batch customer scoring
- CRM integration
- Intervention outcome tracking
- A/B testing of retention offers
- SHAP explanations
- Probability calibration
- Model and data drift monitoring
- Authentication and role-based access
- PostgreSQL
- Scheduled scoring jobs
- Customer-level audit trail

## Author

Patrick Andrawus Kumba  
Machine Learning Engineer | Applied AI and Operational Intelligence Systems
