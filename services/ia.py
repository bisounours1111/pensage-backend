import httpx
from config.settings import Config
from typing import Optional, Dict, Any


async def request_ia(
    prompt: str,
    model: Optional[str] = None,
    timeout: float = 60.0
) -> Dict[str, Any]:
    """
    Effectue une requête asynchrone à l'IA Ollama
    
    Args:
        prompt: Le prompt à envoyer à l'IA
        model: Le modèle à utiliser (par défaut: Config.OLLAMA_MODEL)
        timeout: Timeout en secondes (par défaut: 60s)
    
    Returns:
        Dict contenant la réponse de l'IA
        
    Raises:
        httpx.HTTPError: En cas d'erreur HTTP
        Exception: En cas d'erreur générale
    """
    model = model or Config.OLLAMA_MODEL
    url = f"{Config.OLLAMA_URL}/api/generate"
    
    # Préparer les headers avec la clé API si elle existe
    headers = {"Content-Type": "application/json"}
    if Config.OLLAMA_API_KEY:
        headers["Authorization"] = f"Bearer {Config.OLLAMA_API_KEY}"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        print(response_json.get("response", response_json))
        return response_json