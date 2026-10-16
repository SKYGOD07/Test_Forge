"""
Unit and Integration Tests for CampusPulse AI Notice-to-Action Service and API
"""

import io
import json
import pytest
from unittest.mock import MagicMock, patch

from app import create_app
from app.services.gemma_service import GemmaService, DEFAULT_SCHEMA, DEMO_SAMPLES


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_notice_health_endpoint(client):
    """Verify notice health endpoint status and metadata"""
    response = client.get('/api/notice/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'service' in data
    assert 'gemma' in data
    assert data['gemma']['engine'] == 'Gemma 4'
    assert 'accepted_formats' in data['gemma']


def test_notice_samples_endpoint(client):
    """Verify samples endpoint returns valid demonstration samples"""
    response = client.get('/api/notice/samples')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['samples']) >= 3
    for s in data['samples']:
        assert 'id' in s
        assert 'title' in s
        assert 'category' in s
        assert 'summary' in s
        assert 'action_items' in s
        assert 'source_evidence' in s


def test_notice_analyze_empty_request_rejected(client):
    """Verify empty input is rejected with 400 Bad Request"""
    response = client.post('/api/notice/analyze', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert "No input provided" in data['error']


def test_notice_analyze_invalid_image_type_rejected(client):
    """Verify invalid file extensions are safely rejected"""
    data = {
        'image': (io.BytesIO(b"fake executable content"), 'malicious.exe')
    }
    response = client.post('/api/notice/analyze', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    res_data = response.get_json()
    assert res_data['success'] is False
    assert "Invalid image format" in res_data['error']


def test_notice_analyze_demo_mode(client):
    """Verify demo mode returns structured result with explicit demo metadata"""
    response = client.post('/api/notice/analyze', json={
        "text": "Campus Hackathon Notice for Gwalior",
        "demo": True
    })
    assert response.status_code == 200
    res_data = response.get_json()
    assert res_data['success'] is True
    assert 'data' in res_data
    assert 'meta' in res_data
    assert res_data['meta']['mode'] == 'demo_simulation'
    
    extracted = res_data['data']
    assert 'title' in extracted
    assert 'category' in extracted
    assert 'action_items' in extracted
    assert isinstance(extracted['action_items'], list)
    assert len(extracted['action_items']) > 0
    assert 'uncertainties' in extracted
    assert 'source_evidence' in extracted


def test_notice_analyze_specific_sample_id(client):
    """Verify request with sample_id returns the matching sample"""
    response = client.post('/api/notice/analyze', json={
        "sample_id": "exam-fee-notice",
        "demo": True
    })
    assert response.status_code == 200
    res = response.get_json()
    assert res['success'] is True
    assert "Examination" in res['data']['title']
    assert res['data']['category'] == 'administrative'


def test_gemma_service_schema_validation_and_cleaning():
    """Verify GemmaService schema normalization, markdown stripping, and list coercion"""
    service = GemmaService(api_key="mock_key")
    
    # 1. Standard markdown code fence
    markdown_json = """```json
    {
        "title": "Robotics Workshop",
        "category": "event",
        "summary": "Hands-on robotics workshop in Lab 4",
        "event_date": "Nov 20, 2026",
        "action_items": [{"task": "RSVP on portal", "priority": "high"}],
        "eligibility": "First year students only"
    }
    ```"""
    
    parsed = service._parse_and_validate(markdown_json)
    assert parsed['title'] == "Robotics Workshop"
    assert parsed['category'] == "event"
    # Coerced string eligibility to list
    assert isinstance(parsed['eligibility'], list)
    assert parsed['eligibility'] == ["First year students only"]
    assert isinstance(parsed['requirements'], list)
    assert parsed['organizer'] is None  # Defaults correctly


def test_gemma_service_mocked_model_call():
    """Verify GemmaService correctly calls Gemini API and returns validated structure"""
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.text = json.dumps({
        "title": "Guest Lecture on AI",
        "category": "academic",
        "summary": "Guest lecture by industry expert.",
        "organizer": "Dept of CS",
        "event_date": "Dec 5, 2026",
        "registration_deadline": "Dec 1, 2026",
        "venue": "Seminar Hall 1",
        "eligibility": ["All students"],
        "requirements": ["Registration slip"],
        "important_dates": [{"label": "Talk", "date": "Dec 5"}],
        "action_items": [{"task": "Register online", "deadline": "Dec 1", "priority": "high"}],
        "contact_information": [{"name_or_dept": "CS Dept", "contact": "cs@itm.edu"}],
        "uncertainties": ["Speaker bio not specified"],
        "source_evidence": ["Guest lecture on AI"]
    })
    mock_client.models.generate_content.return_value = mock_response

    service = GemmaService(api_key="valid_test_key")
    service._client = mock_client

    result = service.analyze_notice(text="Notice: Guest Lecture on AI on Dec 5 at Seminar Hall 1.")
    assert result['success'] is True
    assert result['data']['title'] == "Guest Lecture on AI"
    assert result['meta']['engine'] == "Gemma 4"
    assert result['meta']['mode'] == "live_gemini_api"
    mock_client.models.generate_content.assert_called_once()
