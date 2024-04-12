import pytest
from fastapi import FastAPI, Request, HTTPException
from fastapi.testclient import TestClient
from configs.logging import configure_logging, log_requests, validate_headers, configure_app
from unittest.mock import patch, MagicMock

def test_configure_logging():
    with patch('logging.basicConfig') as mock_basicConfig:
        configure_logging()
        mock_basicConfig.assert_called_once()

def test_log_requests():
    app = FastAPI()
    client = TestClient(app)
    request = Request({"type": "http", "method": "GET", "headers": {}, "path": "/"})
    request.state._state = {"app_test": "value"}

    async def call_next(request):
        return 'response'

    response = client.get('/')
    assert response.status_code == 200

def test_validate_headers():
    request = Request({"type": "http", "method": "GET", "headers": {"x-correlation-id": "123", "initiator": "test"}, "path": "/"})
    headers = validate_headers(request)
    assert headers.x_correlation_id == "123"
    assert headers.initiator == "test"

def test_validate_headers_missing_header():
    request = Request({"type": "http", "method": "GET", "headers": {"x-correlation-id": "123"}, "path": "/"})
    with pytest.raises(HTTPException):
        validate_headers(request)

def test_configure_app():
    app = FastAPI()
    with patch.object(app, 'middleware') as mock_middleware, \
         patch.object(app, 'router') as mock_router, \
         patch.object(app, 'openapi') as mock_openapi:
        configure_app(app)
        mock_middleware.assert_called_once_with('http', log_requests)
        assert len(mock_router.dependencies) == 1
        assert mock_openapi.called
