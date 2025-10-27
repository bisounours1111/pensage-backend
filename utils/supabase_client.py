from supabase import create_client, Client
from config.settings import Config

class SupabaseClient:
    """Client Supabase singleton pour gérer les connexions à la base de données"""
    
    _instance: Client = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Récupérer l'instance du client Supabase"""
        if cls._instance is None:
            if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
                raise ValueError("Les configurations Supabase ne sont pas définies")
            
            cls._instance = create_client(
                Config.SUPABASE_URL,
                Config.SUPABASE_KEY
            )
        
        return cls._instance

# Instance globale facile à importer
supabase = SupabaseClient.get_client()

