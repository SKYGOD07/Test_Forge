"""
CampusPulse AI - Notice to Action API Blueprint
Exposes endpoints for extracting structured intelligence and action checklists from campus notices
"""

import logging
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from ..services.gemma_service import GemmaService, GemmaAuthError
from ..config import Config

logger = logging.getLogger(__name__)

notice_bp = Blueprint('notice', __name__)
gemma_service = GemmaService()

ALLOWED_MIME_TYPES = {
    'image/png': 'png',
    'image/jpeg': 'jpg',
    'image/jpg': 'jpg',
    'image/webp': 'webp'
}


@notice_bp.route('/health', methods=['GET'])
def health():
    """Return health and configuration status of Gemma 4 service"""
    return jsonify({
        "status": "healthy",
        "service": "CampusPulse AI Notice-to-Action",
        "gemma": gemma_service.get_status()
    })


@notice_bp.route('/samples', methods=['GET'])
def get_samples():
    """Return pre-configured campus notice samples for 1-click judging demo"""
    return jsonify({
        "success": True,
        "samples": gemma_service.get_samples()
    })


@notice_bp.route('/analyze', methods=['POST'])
def analyze_notice():
    """
    Analyze a campus notice via Gemma 4.
    Supports:
      - Multipart form-data with 'image' file and/or 'text'
      - JSON body with 'text' and optional 'demo' flag
    """
    try:
        text_content = None
        image_bytes = None
        mime_type = None
        is_demo = False
        sample_id = None

        # Check Content-Type
        if request.content_type and 'multipart/form-data' in request.content_type:
            text_content = request.form.get('text', '').strip() or None
            is_demo = request.form.get('demo', 'false').lower() == 'true'
            sample_id = request.form.get('sample_id', '').strip() or None

            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
                    
                    if ext not in Config.ALLOWED_IMAGE_EXTENSIONS:
                        return jsonify({
                            "success": False,
                            "error": f"Invalid image format '{ext}'. Allowed: {', '.join(Config.ALLOWED_IMAGE_EXTENSIONS)}"
                        }), 400
                    
                    # Read bytes
                    image_bytes = file.read()
                    if len(image_bytes) > 15 * 1024 * 1024:
                        return jsonify({
                            "success": False,
                            "error": "Image file too large. Maximum size is 15MB."
                        }), 400
                    
                    mime_type = file.mimetype or f"image/{ext}"

        elif request.is_json:
            data = request.get_json(silent=True) or {}
            text_content = (data.get('text') or '').strip() or None
            is_demo = bool(data.get('demo', False))
            sample_id = data.get('sample_id')

        else:
            # Fallback form data
            text_content = request.form.get('text', '').strip() or None
            is_demo = request.form.get('demo', 'false').lower() == 'true'
            sample_id = request.form.get('sample_id')

        if not text_content and not image_bytes and not sample_id:
            return jsonify({
                "success": False,
                "error": "No input provided. Please provide announcement text or upload a notice image."
            }), 400

        result = gemma_service.analyze_notice(
            text=text_content,
            image_bytes=image_bytes,
            mime_type=mime_type,
            is_demo=is_demo,
            sample_id=sample_id
        )

        return jsonify(result), 200

    except GemmaAuthError as e:
        logger.warning("Gemma authentication error: %s", str(e))
        return jsonify({
            "success": False,
            "error": str(e),
            "hint": "Set GEMINI_API_KEY on the server or toggle Demo Mode in the interface to test instantly."
        }), 401

    except ValueError as e:
        logger.warning("Validation error during notice analysis: %s", str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

    except Exception as e:
        logger.error("Unhandled error during notice analysis: %s", str(e), exc_info=True)
        return jsonify({
            "success": False,
            "error": f"Notice analysis failed: {str(e)}"
        }), 500
