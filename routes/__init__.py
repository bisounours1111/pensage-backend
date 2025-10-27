def register_routes(app):
    """Enregistrer tous les routers de routes"""
    
    # Importer les routers
    from .health import health_router
    from .api import api_router
    from .ia import ia_router
    
    # Enregistrer les routers
    app.include_router(health_router)
    app.include_router(api_router, prefix='/api', tags=['API'])
    app.include_router(ia_router, prefix='/ia', tags=['IA'])

