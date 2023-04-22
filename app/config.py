import os


class Config:
    CSRF_ENABLED = True

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False