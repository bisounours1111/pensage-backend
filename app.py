from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config.settings import Config
from routes import register_routes

def create_app():
    """Factory function pour créer l'application FastAPI"""
    
    app = FastAPI(
        title="API PENSAGA",
        description="API pour PENSAGA",
        version="1.0.0"
    )
    
    try:
        Config.validate()
    except ValueError as e:
        print(f"Erreur de configuration: {e}")
        print("Assurez-vous d'avoir créé un fichier .env avec les variables nécessaires")
    
    # Configuration CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )
    
    # Enregistrer les routes
    register_routes(app)
    
    # Gestionnaires d'erreurs
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        return JSONResponse(
            status_code=404,
            content={
                'error': 'Route non trouvée',
                'message': 'L\'endpoint demandé n\'existe pas'
            }
        )
    
    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc):
        return JSONResponse(
            status_code=500,
            content={
                'error': 'Erreur interne du serveur',
                'message': 'Une erreur est survenue'
            }
        )
    
    return app

# Créer l'instance de l'application
app = create_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        "app:app",
        port=5000,
        reload=True
    )

