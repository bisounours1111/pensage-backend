from flask import Blueprint

def register_routes(app):
    """Enregistrer tous les blueprints de routes"""
    
    # Importer les blueprints
    from .health import health_bp
    from .api import api_bp
    
    # Enregistrer les blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

