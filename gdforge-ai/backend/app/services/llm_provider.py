"""Abstraktní rozhraní a implementace LLM poskytovatelů"""

from abc import ABC, abstractmethod
from typing import Optional
import json
from app.core.config import settings
from app.core.exceptions import LLMException


class LLMProvider(ABC):
    """Abstraktní třída pro LLM poskytovatele"""

    @abstractmethod
    async def analyze_prompt(self, user_prompt: str) -> dict:
        """
        Analyzuje uživatelský prompt a vrací strukturovaný plán

        Args:
            user_prompt: Zadání uživatele v přirozeném jazyce

        Returns:
            dict: Strukturovaný plán s informacemi o scénách, skriptech, zdrojích
        """
        pass


class OpenAIProvider(LLMProvider):
    """Implementace pro OpenAI API"""

    def __init__(self, api_key: str = None):
        if not api_key:
            api_key = settings.openai_api_key
        if not api_key:
            raise LLMException("OpenAI API key not configured", "openai")

        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=api_key)
        except ImportError:
            raise LLMException("OpenAI package not installed", "openai")

    async def analyze_prompt(self, user_prompt: str) -> dict:
        """Analyzuje prompt pomocí GPT-4"""
        try:
            system_prompt = """Ty jsi expert na Godot herní vývoj a Infrastructure as Code.
Uživatel ti zadá popis herní architektury, scén nebo logiky.
Vrátíš strukturovaný JSON plán (blueprint) s těmito klíči:

{
    "scenes": [
        {
            "name": "SceneName",
            "path": "res://scenes/SceneName.tscn",
            "root_node": {"type": "Node2D|Control|Node3D", "name": "Root"},
            "nodes": [
                {
                    "name": "NodeName",
                    "type": "Sprite2D|TileMap|CharacterBody2D|atd",
                    "properties": {"rotation": 0.5, "scale": [1, 1]},
                    "children": []
                }
            ],
            "script": "res://scripts/SceneName.gd"
        }
    ],
    "scripts": [
        {
            "path": "res://scripts/ScriptName.gd",
            "class_name": "ClassName",
            "extends": "Node",
            "properties": [{"name": "var_name", "type": "String", "default": ""}],
            "methods": [
                {
                    "name": "method_name",
                    "signature": "func method_name() -> String:",
                    "docstring": "Popis funkce"
                }
            ]
        }
    ],
    "resources": [
        {
            "type": "StandardMaterial3D|NoiseTexture|BoxMesh",
            "path": "res://resources/ResourceName.tres",
            "properties": {}
        }
    ],
    "signals": [
        {
            "scene": "SceneName.tscn",
            "emitter": "NodeName",
            "signal_name": "pressed",
            "receiver": "AnotherNode",
            "handler": "_on_node_pressed"
        }
    ],
    "summary": "Stručný popis toho, co se vytvoří"
}

Vrátíš POUZE validní JSON bez dalšího textu."""

            response = await self.client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            blueprint = json.loads(content)
            return blueprint

        except json.JSONDecodeError as e:
            raise LLMException(f"Invalid JSON response: {str(e)}", "openai")
        except Exception as e:
            raise LLMException(f"API call failed: {str(e)}", "openai")


class AnthropicProvider(LLMProvider):
    """Implementace pro Anthropic Claude API"""

    def __init__(self, api_key: str = None):
        if not api_key:
            api_key = settings.anthropic_api_key
        if not api_key:
            raise LLMException("Anthropic API key not configured", "anthropic")

        try:
            from anthropic import Anthropic
            self.client = Anthropic(api_key=api_key)
        except ImportError:
            raise LLMException("Anthropic package not installed", "anthropic")

    async def analyze_prompt(self, user_prompt: str) -> dict:
        """Analyzuje prompt pomocí Claude"""
        try:
            system_prompt = """Ty jsi expert na Godot herní vývoj a Infrastructure as Code.
Uživatel ti zadá popis herní architektury, scén nebo logiky.
Vrátíš strukturovaný JSON plán (blueprint) s těmito klíči:

{
    "scenes": [
        {
            "name": "SceneName",
            "path": "res://scenes/SceneName.tscn",
            "root_node": {"type": "Node2D|Control|Node3D", "name": "Root"},
            "nodes": [...]
        }
    ],
    "scripts": [...],
    "resources": [...],
    "signals": [...],
    "summary": "..."
}

Vrátíš POUZE validní JSON bez dalšího textu."""

            response = self.client.messages.create(
                model="claude-3-sonnet-20231222",
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )

            content = response.content[0].text
            blueprint = json.loads(content)
            return blueprint

        except json.JSONDecodeError as e:
            raise LLMException(f"Invalid JSON response: {str(e)}", "anthropic")
        except Exception as e:
            raise LLMException(f"API call failed: {str(e)}", "anthropic")


def get_llm_provider() -> LLMProvider:
    """Vrací instanci LLM poskytovatele na základě konfigurace"""
    provider = settings.llm_provider.lower()

    if provider == "openai":
        return OpenAIProvider()
    elif provider == "anthropic":
        return AnthropicProvider()
    else:
        raise LLMException(f"Unknown LLM provider: {provider}")
