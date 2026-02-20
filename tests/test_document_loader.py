"""Tests for document loaders."""
import json
import os
import tempfile
import pytest
from app.document_loader import load_pdf, load_json, load_questions


def test_load_json_simple():
    """Test loading a simple JSON file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        data = {"key1": "value1", "key2": "value2"}
        json.dump(data, f)
        temp_path = f.name
    
    try:
        result = load_json(temp_path)
        assert "key1" in result
        assert "value1" in result
        assert "key2" in result
        assert "value2" in result
    finally:
        os.unlink(temp_path)


def test_load_questions_list():
    """Test loading questions from a list JSON."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        questions = ["Question 1?", "Question 2?", "Question 3?"]
        json.dump(questions, f)
        temp_path = f.name
    
    try:
        result = load_questions(temp_path)
        assert len(result) == 3
        assert result[0] == "Question 1?"
        assert result[1] == "Question 2?"
    finally:
        os.unlink(temp_path)


def test_load_questions_dict():
    """Test loading questions from a dict JSON."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        data = {"questions": ["Question 1?", "Question 2?"]}
        json.dump(data, f)
        temp_path = f.name
    
    try:
        result = load_questions(temp_path)
        assert len(result) == 2
        assert "Question 1?" in result
    finally:
        os.unlink(temp_path)


def test_load_questions_invalid():
    """Test loading questions with invalid structure."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        data = {"invalid": "structure"}
        json.dump(data, f)
        temp_path = f.name
    
    try:
        with pytest.raises(ValueError):
            load_questions(temp_path)
    finally:
        os.unlink(temp_path)
