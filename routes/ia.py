from fastapi import APIRouter, HTTPException
import httpx
from utils.supabase_client import SupabaseClient

ia_router = APIRouter()

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gpt-oss:20b"

@ia_router.get('/generate_pitch_idea')
async def async_generate_pitch_idea():
    """Génère une idée de pitch via Ollama"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OLLAMA_URL, 
                json={"model": OLLAMA_MODEL, "prompt": "Generate a pitch idea for a new startup."}
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Erreur Ollama: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
