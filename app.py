from flask import Flask, jsonify
from flask_cors import CORS
from config.settings import Config
from routes import register_routes

def create_app():
    """Factory function pour créer l'application Flask"""
    
    # Initialiser Flask
    app = Flask(__name__)
    
    # Charger la configuration
    app.config.from_object(Config)
    
    # Valider la configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Erreur de configuration: {e}")
        print("Assurez-vous d'avoir créé un fichier .env avec les variables nécessaires")
    
    # Configurer CORS
    CORS(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Enregistrer les routes
    register_routes(app)
    
    # Gestionnaire d'erreurs global
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Route non trouvée',
            'message': 'L\'endpoint demandé n\'existe pas'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Erreur interne du serveur',
            'message': 'Une erreur est survenue'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )

