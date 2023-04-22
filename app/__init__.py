from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Create the Flask application
app = Flask(__name__)

# Configure the Flask application
app.config.from_object("app.config.Config")

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Load environment variables
load_dotenv()

# Setup the database
@app.before_first_request
def setup():
    # delete the database file if it exists currently
    if os.path.exists("app/app.db"):
        os.remove("app/app.db")

    # create the database and the db table
    db.create_all()


# Import routing, models, and start the app
from app import views, models
