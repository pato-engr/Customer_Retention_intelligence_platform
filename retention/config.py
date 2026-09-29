# from __future__ import annotations

# import os
# from pathlib import Path


# BASE_DIR = Path(__file__).resolve().parents[1]


# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
#     DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

#     MODEL_PATH = Path(
#         os.getenv(
#             "MODEL_PATH",
#             BASE_DIR / "model" / "churn_pipeline.pkl",
#         )
#     )

#     DATABASE_PATH = Path(
#         os.getenv(
#             "DATABASE_PATH",
#             BASE_DIR / "instance" / "retention.db",
#         )
#     )

#     MAX_CONTENT_LENGTH = 2 * 1024 * 1024
from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "development-only-change-me")
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

    MODEL_PATH = Path(
        os.getenv(
            "MODEL_PATH",
            BASE_DIR / "model" / "churn_pipeline.pkl",
        )
    )

    if os.getenv("VERCEL"):
        _default_db_path = Path("/tmp/retention.db")
    else:
        _default_db_path = BASE_DIR / "instance" / "retention.db"

    DATABASE_PATH = Path(os.getenv("DATABASE_PATH", _default_db_path))

    MAX_CONTENT_LENGTH = 2 * 1024 * 1024