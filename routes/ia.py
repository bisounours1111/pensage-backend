from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import httpx

from services.ia import request_ia
from config.prompts import (
    CREATE_PITCH, 
    CREATE_SYNOPSIS, 
    CREATE_CHARACTERS, 
    CREATE_EPISODE, 
    FIX_TEXT, 
    REPHRASE_TEXT
)
from config.settings import Config

ia_router = APIRouter()


# Modèles Pydantic pour la validation
class PitchRequest(BaseModel):
    user_request: str

class SynopsisRequest(BaseModel):
    pitch: str

class CharactersRequest(BaseModel):
    pitch: str
    synopsis: str

class EpisodeRequest(BaseModel):
    pitch: str
    synopsis: str
    personnages: str
    numero: int = 1
    episodes_precedents: list[str] = []  # Liste des contenus des épisodes précédents

class FixTextRequest(BaseModel):
    text: str

class RephraseRequest(BaseModel):
    text_complete: str
    text_to_reformulate: str


@ia_router.post('/generate_pitch')
async def generate_pitch(request: PitchRequest):
    """Génère 5 idées de pitch à partir d'une demande utilisateur"""
    try:
        prompt = CREATE_PITCH.format(user_request=request.user_request)
        result = await request_ia(prompt)
        
        return {
            "success": True,
            "model": Config.OLLAMA_MODEL,
            "user_request": request.user_request,
            "pitchs": result.get("response", ""),
            "metadata": {
                "total_duration": result.get("total_duration"),
                "load_duration": result.get("load_duration"),
                "prompt_eval_count": result.get("prompt_eval_count"),
                "eval_count": result.get("eval_count")
            }
        }
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504, 
            detail="Timeout lors de la génération. Le serveur IA met trop de temps à répondre."
        )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503, 
            detail=f"Impossible de se connecter au serveur IA ({Config.OLLAMA_URL}). Vérifiez qu'Ollama est démarré."
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Erreur du serveur IA: {e.response.text}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur lors de la génération: {str(e)}"
        )


@ia_router.post('/generate_synopsis')
async def generate_synopsis(request: SynopsisRequest):
    """Génère un synopsis de 10 lignes à partir d'un pitch"""
    try:
        prompt = CREATE_SYNOPSIS.format(user_request=request.pitch)
        result = await request_ia(prompt)
        
        return {
            "success": True,
            "model": Config.OLLAMA_MODEL,
            "pitch": request.pitch,
            "synopsis": result.get("response", ""),
            "metadata": {
                "total_duration": result.get("total_duration"),
                "eval_count": result.get("eval_count")
            }
        }
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout lors de la génération.")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail=f"Impossible de se connecter au serveur IA ({Config.OLLAMA_URL}).")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ia_router.post('/generate_characters')
async def generate_characters(request: CharactersRequest):
    """Génère 3-5 personnages principaux à partir d'un pitch et synopsis"""
    try:
        prompt = CREATE_CHARACTERS.format(
            pitch=request.pitch,
            synopsis=request.synopsis
        )
        result = await request_ia(prompt)
        
        return {
            "success": True,
            "model": Config.OLLAMA_MODEL,
            "characters": result.get("response", ""),
            "metadata": {
                "total_duration": result.get("total_duration"),
                "eval_count": result.get("eval_count")
            }
        }
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout lors de la génération.")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail=f"Impossible de se connecter au serveur IA ({Config.OLLAMA_URL}).")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ia_router.post('/generate_episode')
async def generate_episode(request: EpisodeRequest):
    """Génère un épisode complet de webtoon (1500-2500 mots)"""
    try:
        # Construire le contexte des épisodes précédents
        contexte_episodes = ""
        if request.episodes_precedents:
            contexte_str = "\n\n---\n\n".join([
                f"Épisode {i+1} :\n{episode}" 
                for i, episode in enumerate(request.episodes_precedents)
            ])
            contexte_episodes = f"Épisodes précédents (pour contexte et cohérence) :\n{contexte_str}\n"
        
        prompt = CREATE_EPISODE.format(
            pitch=request.pitch,
            synopsis=request.synopsis,
            personnages=request.personnages,
            numero=request.numero,
            contexte_episodes=contexte_episodes
        )
        result = await request_ia(prompt, timeout=120.0)  # Timeout plus long pour les épisodes
        
        return {
            "success": True,
            "model": Config.OLLAMA_MODEL,
            "episode_number": request.numero,
            "episode_content": result.get("response", ""),
            "metadata": {
                "total_duration": result.get("total_duration"),
                "eval_count": result.get("eval_count")
            }
        }
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout lors de la génération. Les épisodes peuvent prendre jusqu'à 2 minutes.")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail=f"Impossible de se connecter au serveur IA ({Config.OLLAMA_URL}).")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ia_router.post('/fix_text')
async def fix_text(request: FixTextRequest):
    """Corrige les fautes d'orthographe et de grammaire sans reformuler"""
    try:
        prompt = FIX_TEXT.format(text=request.text)
        result = await request_ia(prompt)
        
        return {
            "success": True,
            "model": Config.OLLAMA_MODEL,
            "original_text": request.text,
            "fixed_text": result.get("response", ""),
            "metadata": {
                "total_duration": result.get("total_duration")
            }
        }
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout lors de la correction.")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail=f"Impossible de se connecter au serveur IA ({Config.OLLAMA_URL}).")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ia_router.post('/rephrase_text')
async def rephrase_text(request: RephraseRequest):
    """Reformule un passage pour le rendre plus fluide"""
    try:
        prompt = REPHRASE_TEXT.format(
            text_complete=request.text_complete,
            text_to_reformulate=request.text_to_reformulate
        )
        result = await request_ia(prompt)
        
        return {
            "success": True,
            "model": Config.OLLAMA_MODEL,
            "original_passage": request.text_to_reformulate,
            "rephrased_text": result.get("response", ""),
            "metadata": {
                "total_duration": result.get("total_duration")
            }
        }
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout lors de la reformulation.")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail=f"Impossible de se connecter au serveur IA ({Config.OLLAMA_URL}).")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))