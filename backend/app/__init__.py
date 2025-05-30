from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from app import routes  # Import routes after app is created to avoid circular imports 