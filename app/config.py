import json
import logging
from flask import current_app

def configure_app(app):
    # Load configuration
    try:
        with open('instance/config.json', 'r') as file:
            config = json.load(file)
            app.config['TARGET_SERVER'] = config["target_server"]
            app.config['PROXY_PORT'] = config["port"]
            app.config['AUTH_TOKEN'] = config["auth_token"]
            app.config['HEADERS'] = {
                "Authorization": f"Bearer {config['auth_token']}",
                "Content-Type": "application/json"
            }
            app.logger.info("Configuration loaded successfully.")
    except FileNotFoundError:
        app.logger.error("Configuration file 'config.json' not found.")
        raise
    except KeyError as e:
        app.logger.error(f"Missing required configuration key: {e}")
        raise

    # Configure logging
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s [%(levelname)s] %(message)s")
    app.logger = logging.getLogger(__name__)

