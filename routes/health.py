from fastapi import APIRouter, HTTPException
from utils.supabase_client import SupabaseClient

health_router = APIRouter()

@health_router.get('/health')
async def health_check():
    """Endpoint pour vérifier l'état de santé de l'API"""
    try:
        # Tester la connexion Supabase
        client = SupabaseClient.get_client()
        
        return {
            'status': 'healthy',
            'message': 'API fonctionne correctement',
            'supabase': 'connected'
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'status': 'unhealthy',
                'message': str(e),
                'supabase': 'disconnected'
            }
        )

@health_router.get('/')
async def root():
    """Endpoint racine"""
    return {
        'message': 'Bienvenue sur l\'API PENSAGA',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'api': '/api'
        }
    }

