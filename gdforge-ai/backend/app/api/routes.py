"""Hlavní API routes"""

from fastapi import APIRouter, HTTPException, status
from app.api.models import GenerateRequest, GenerateResponse, HealthResponse
from app.services.llm_provider import get_llm_provider
from app.services.gdscript_generator import GDScriptGenerator
from app.core.config import settings
from app.core.exceptions import GDForgeException, LLMException, GenerationException
import re

router = APIRouter()
generator = GDScriptGenerator()


def _generate_filename(scene_name: str) -> str:
    """Generuje bezpečné jméno souboru"""
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', scene_name)
    return f"{safe_name}_Installer.gd"


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        llm_provider=settings.llm_provider
    )


@router.post("/generate", response_model=GenerateResponse)
async def generate_installer(request: GenerateRequest):
    """
    Generuje Installer.gd ze zadaného promptu

    Proces:
    1. Analýza promptu pomocí LLM → strukturovaný blueprint
    2. Validace blueprintu
    3. Generování GDScript Installer.gd
    4. Vrácení kódu k stažení
    """
    try:
        # 1. Analýza promptu
        llm_provider = get_llm_provider()
        blueprint = await llm_provider.analyze_prompt(request.prompt)

        # 2. Generování GDScript
        installer_code = generator.generate(blueprint, request.project_root)

        # 3. Generování jména souboru
        scene_names = [s.get("name", "Scene") for s in blueprint.get("scenes", [])]
        filename = _generate_filename(scene_names[0] if scene_names else "Project")

        return GenerateResponse(
            success=True,
            blueprint=blueprint if request.format == "json" else None,
            installer_code=installer_code,
            filename=filename,
            message=f"Successfully generated installer for {len(blueprint.get('scenes', []))} scenes"
        )

    except LLMException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except GenerationException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except GDForgeException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}"
        )


@router.post("/generate/json", response_model=dict)
async def generate_blueprint(request: GenerateRequest):
    """Generuje pouze blueprint (JSON) bez GDScript kódu"""
    try:
        llm_provider = get_llm_provider()
        blueprint = await llm_provider.analyze_prompt(request.prompt)

        return {
            "success": True,
            "blueprint": blueprint
        }
    except LLMException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {str(e)}"
        )


def _generate_filename(scene_name: str) -> str:
    """Generuje filename z názvu scény"""
    # Odstraň speciální znaky
    clean_name = re.sub(r"[^a-zA-Z0-9]", "_", scene_name)
    clean_name = re.sub(r"_+", "_", clean_name).strip("_")
    return f"setup_{clean_name}.gd"
