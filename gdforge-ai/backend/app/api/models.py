"""Datové modely pro API"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class GenerateRequest(BaseModel):
    """Request pro generování Installer.gd"""

    prompt: str = Field(
        ...,
        description="Přirozený jazyk popis herní architektury",
        example="Vytvoř mi level pro plošinovku. Chci scénu 'Level1' s TileMapou, hráčem..."
    )
    project_root: str = Field(
        default="scenes",
        description="Kořenový adresář pro vytváření souborů",
        example="res://scenes"
    )
    format: Optional[str] = Field(
        default="gdscript",
        description="Formát výstupu: 'gdscript' nebo 'json'",
        example="gdscript"
    )


class GenerateResponse(BaseModel):
    """Response po generování"""

    success: bool = Field(
        ...,
        description="Zda se generování povedlo"
    )
    blueprint: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Strukturovaný plán (blueprint)"
    )
    installer_code: Optional[str] = Field(
        default=None,
        description="Vygenerovaný GDScript kód"
    )
    filename: Optional[str] = Field(
        default=None,
        description="Doporučené jméno souboru"
    )
    message: Optional[str] = Field(
        default=None,
        description="Statusová zpráva nebo chyba"
    )
    error: Optional[str] = Field(
        default=None,
        description="Detaily chyby pokud došlo k selhání"
    )


class HealthResponse(BaseModel):
    """Response pro health check"""

    status: str = Field(
        ...,
        description="Status aplikace",
        example="healthy"
    )
    version: str = Field(
        ...,
        description="Verze aplikace"
    )
    llm_provider: str = Field(
        ...,
        description="Konfigurovaný LLM provider"
    )
