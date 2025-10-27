from flask import Blueprint, jsonify, request
from utils.supabase_client import supabase

api_bp = Blueprint('api', __name__)

@api_bp.route('/example', methods=['GET'])
def get_example():
    """Exemple d'endpoint GET"""
    try:
        # Exemple de requête Supabase
        # response = supabase.table('your_table').select("*").execute()
        
        return jsonify({
            'message': 'Endpoint exemple GET',
            'data': []
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@api_bp.route('/example', methods=['POST'])
def create_example():
    """Exemple d'endpoint POST"""
    try:
        data = request.get_json()
        
        # Exemple d'insertion dans Supabase
        # response = supabase.table('your_table').insert(data).execute()
        
        return jsonify({
            'message': 'Ressource créée avec succès',
            'data': data
        }), 201
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@api_bp.route('/example/<int:id>', methods=['GET'])
def get_example_by_id(id):
    """Exemple d'endpoint GET avec paramètre"""
    try:
        # Exemple de requête avec filtre
        # response = supabase.table('your_table').select("*").eq('id', id).execute()
        
        return jsonify({
            'message': f'Ressource avec ID {id}',
            'data': {}
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@api_bp.route('/example/<int:id>', methods=['PUT'])
def update_example(id):
    """Exemple d'endpoint PUT"""
    try:
        data = request.get_json()
        
        # Exemple de mise à jour dans Supabase
        # response = supabase.table('your_table').update(data).eq('id', id).execute()
        
        return jsonify({
            'message': f'Ressource {id} mise à jour',
            'data': data
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

@api_bp.route('/example/<int:id>', methods=['DELETE'])
def delete_example(id):
    """Exemple d'endpoint DELETE"""
    try:
        # Exemple de suppression dans Supabase
        # response = supabase.table('your_table').delete().eq('id', id).execute()
        
        return jsonify({
            'message': f'Ressource {id} supprimée'
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

