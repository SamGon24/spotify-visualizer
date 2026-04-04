from flask import Flask
from flask_cors import CORS
import logging
from .routes import api_bp

def create_app() -> Flask:
    app = Flask(__name__)

    # Setup logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    
    logger.info("🚀 Creating Flask app...")

    # Enable CORS for frontend communication
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://localhost:3000"]}})
    logger.info("✅ CORS enabled for localhost:5173 and localhost:3000")

    app.register_blueprint(api_bp)
    logger.info("✅ API blueprint registered")

    return app
