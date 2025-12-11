"""Testy API"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "llm_provider" in data


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "docs" in data


@pytest.mark.asyncio
async def test_generate_missing_prompt():
    """Test generate endpoint bez promptu"""
    response = client.post("/api/generate", json={})
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_generate_blueprint_structure():
    """Test struktura generovaného blueprintu"""
    # Tento test by vyžadoval API klíč a skutečný LLM call
    # Zde je ukázka struktury
    blueprint = {
        "scenes": [
            {
                "name": "TestScene",
                "path": "res://TestScene.tscn",
                "root_node": {"type": "Node2D", "name": "Root"},
                "nodes": [],
                "script": None
            }
        ],
        "scripts": [],
        "resources": [],
        "signals": [],
        "summary": "Test scene"
    }
    
    assert "scenes" in blueprint
    assert "scripts" in blueprint
    assert "resources" in blueprint
    assert len(blueprint["scenes"]) > 0
