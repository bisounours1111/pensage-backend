import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration de base pour l'application Flask"""
    
    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    @staticmethod
    def validate():
        """Valider que toutes les configurations essentielles sont présentes"""
        required_vars = ['SUPABASE_URL', 'SUPABASE_KEY']
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            raise ValueError(f"Variables d'environnement manquantes: {', '.join(missing)}")

