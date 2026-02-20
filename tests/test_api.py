"""Tests for FastAPI endpoints."""
import json
import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_endpoint():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_qa_endpoint_invalid_questions_file():
    """Test QA endpoint with invalid questions file type."""
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        f.write(b"not json")
        questions_path = f.name
    
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        f.write(b"fake pdf content")
        doc_path = f.name
    
    try:
        with open(questions_path, 'rb') as qf, open(doc_path, 'rb') as df:
            response = client.post(
                "/qa",
                files={
                    "questions_file": ("questions.txt", qf, "text/plain"),
                    "document_file": ("document.pdf", df, "application/pdf")
                }
            )
            assert response.status_code == 400
    finally:
        os.unlink(questions_path)
        os.unlink(doc_path)


def test_qa_endpoint_invalid_document_file():
    """Test QA endpoint with invalid document file type."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(["Question 1?"], f)
        questions_path = f.name
    
    with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
        f.write(b"not pdf or json")
        doc_path = f.name
    
    try:
        with open(questions_path, 'rb') as qf, open(doc_path, 'rb') as df:
            response = client.post(
                "/qa",
                files={
                    "questions_file": ("questions.json", qf, "application/json"),
                    "document_file": ("document.txt", df, "text/plain")
                }
            )
            assert response.status_code == 400
    finally:
        os.unlink(questions_path)
        os.unlink(doc_path)
