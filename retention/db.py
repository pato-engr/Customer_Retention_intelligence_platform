from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


SCHEMA = """
CREATE TABLE IF NOT EXISTS assessments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_reference TEXT NOT NULL,
    contract TEXT NOT NULL,
    tenure INTEGER NOT NULL,
    monthly_charges REAL NOT NULL,
    total_charges REAL NOT NULL,
    churn_probability REAL NOT NULL,
    prediction TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    estimated_monthly_revenue_at_risk REAL NOT NULL,
    primary_driver TEXT NOT NULL,
    recommended_action TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_assessments_created_at
ON assessments(created_at);

CREATE INDEX IF NOT EXISTS idx_assessments_risk_level
ON assessments(risk_level);
"""


def init_database(database_path: Path) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_path) as connection:
        connection.executescript(SCHEMA)
        connection.commit()


@contextmanager
def database_connection(database_path: Path) -> Iterator[sqlite3.Connection]:
    connection = sqlite3.connect(database_path)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
    finally:
        connection.close()
