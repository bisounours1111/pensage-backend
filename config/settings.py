import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration de base pour l'application"""
    
    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Ollama / IA
    OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
    OLLAMA_API_KEY = os.getenv('OLLAMA_API_KEY')  # Optionnel pour Ollama Cloud
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'gpt-oss:120b')
    
    @staticmethod
    def validate():
        """Valider que toutes les configurations essentielles sont présentes"""
        required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            raise ValueError(f"Variables d'environnement manquantes: {', '.join(missing)}")
