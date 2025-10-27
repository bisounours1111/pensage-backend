from flask import Blueprint, jsonify
from utils.supabase_client import SupabaseClient

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Endpoint pour vérifier l'état de santé de l'API"""
    try:
        # Tester la connexion Supabase
        client = SupabaseClient.get_client()
        
        return jsonify({
            'status': 'healthy',
            'message': 'API fonctionne correctement',
            'supabase': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': str(e),
            'supabase': 'disconnected'
        }), 500

@health_bp.route('/', methods=['GET'])
def root():
    """Endpoint racine"""
    return jsonify({
        'message': 'Bienvenue sur l\'API PENSAGA',
        'version': '1.0.0',
        'endpoints': {
            'health': '/health',
            'api': '/api'
        }
    }), 200

