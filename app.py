from app import create_app
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = create_app()

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("🎵 SPOTIFY VISUALIZER - BACKEND STARTING 🎵")
    logger.info("=" * 50)
    logger.info("🚀 Server running on http://localhost:5000")
    logger.info("✨ Frontend should be on http://localhost:5173")
    logger.info("=" * 50)
    app.run(debug=True, host="127.0.0.1", port=5000)