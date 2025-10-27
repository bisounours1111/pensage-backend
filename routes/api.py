from fastapi import APIRouter, HTTPException, Body, status
from typing import Dict, Any
from utils.supabase_client import supabase

api_router = APIRouter()

@api_router.get('/example')
async def get_example():
    """Exemple d'endpoint GET"""
    try:
        # Exemple de requête Supabase
        # response = supabase.table('your_table').select("*").execute()
        
        return {
            'message': 'Endpoint exemple GET',
            'data': []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post('/example', status_code=status.HTTP_201_CREATED)
async def create_example(data: Dict[str, Any] = Body(...)):
    """Exemple d'endpoint POST"""
    try:
        # Exemple d'insertion dans Supabase
        # response = supabase.table('your_table').insert(data).execute()
        
        return {
            'message': 'Ressource créée avec succès',
            'data': data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get('/example/{id}')
async def get_example_by_id(id: int):
    """Exemple d'endpoint GET avec paramètre"""
    try:
        # Exemple de requête avec filtre
        # response = supabase.table('your_table').select("*").eq('id', id).execute()
        
        return {
            'message': f'Ressource avec ID {id}',
            'data': {}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put('/example/{id}')
async def update_example(id: int, data: Dict[str, Any] = Body(...)):
    """Exemple d'endpoint PUT"""
    try:
        # Exemple de mise à jour dans Supabase
        # response = supabase.table('your_table').update(data).eq('id', id).execute()
        
        return {
            'message': f'Ressource {id} mise à jour',
            'data': data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete('/example/{id}')
async def delete_example(id: int):
    """Exemple d'endpoint DELETE"""
    try:
        # Exemple de suppression dans Supabase
        # response = supabase.table('your_table').delete().eq('id', id).execute()
        
        return {
            'message': f'Ressource {id} supprimée'
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

