"""
CampusPulse AI Backend - Flask Application Factory
"""

import os
import warnings

# Suppress multiprocessing resource_tracker warnings (from dependencies like transformers)
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """Flask application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Ensure UTF-8 JSON formatting
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False
    
    # Setup logger
    logger = setup_logger('campuspulse')
    
    # Avoid duplicate startup logs in debug reloader
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process
    
    if should_log_startup:
        logger.info("=" * 50)
        logger.info("CampusPulse AI Backend starting...")
        logger.info("=" * 50)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register simulation runner cleanup handlers
    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()
    if should_log_startup:
        logger.info("Registered simulation cleanup handlers")
    
    # Request/Response logging middleware
    @app.before_request
    def log_request():
        logger = get_logger('campuspulse.request')
        logger.debug(f"Request: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            logger.debug(f"Request body: {request.get_json(silent=True)}")
    
    @app.after_request
    def log_response(response):
        logger = get_logger('campuspulse.request')
        logger.debug(f"Response: {response.status_code}")
        return response
    
    # Register blueprints
    from .api import graph_bp, simulation_bp, report_bp, notice_bp
    app.register_blueprint(notice_bp, url_prefix='/api/notice')
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    
    # Health check
    @app.route('/health')
    def health():
        upload_folder = app.config['UPLOAD_FOLDER']
        try:
            os.makedirs(upload_folder, exist_ok=True)
            uploads_writable = os.access(upload_folder, os.W_OK)
        except OSError:
            uploads_writable = False

        status = 'ok' if uploads_writable else 'degraded'
        payload = {
            'status': status,
            'service': 'CampusPulse AI Backend',
            'checks': {'uploads_writable': uploads_writable},
            'features': {
                'gemma_4_configured': bool(Config.GEMINI_API_KEY),
                'gemma_model': Config.GEMMA_MODEL,
                'simulation_llm_configured': bool(Config.LLM_API_KEY),
                'simulation_zep_configured': bool(Config.ZEP_API_KEY),
            },
        }
        return payload, 200 if uploads_writable else 503
    
    if should_log_startup:
        logger.info("CampusPulse AI Backend ready")
    
    return app
