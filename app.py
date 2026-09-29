# from __future__ import annotations

# import os
# from pathlib import Path

# from flask import Flask

# from retention.config import Config
# from retention.db import init_database
# from retention.routes import web


# def create_app(config: type[Config] = Config) -> Flask:
#     app = Flask(__name__)
#     app.config.from_object(config)

#     Path(app.instance_path).mkdir(parents=True, exist_ok=True)
#     init_database(app.config["DATABASE_PATH"])

#     app.register_blueprint(web)

#     return app


# app = create_app()


# if __name__ == "__main__":
#     port = int(os.getenv("PORT", "5000"))
#     app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])
from __future__ import annotations

import os

from flask import Flask

from retention.config import Config
from retention.db import init_database
from retention.routes import web


def create_app(config: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    init_database(app.config["DATABASE_PATH"])

    app.register_blueprint(web)

    return app


app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=app.config["DEBUG"])