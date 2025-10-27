# Placer vos modèles de données ici
# Exemple d'utilisation avec Pydantic pour la validation des données

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ExampleModel(BaseModel):
    """Modèle exemple pour la validation des données"""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Exemple",
                "description": "Ceci est un exemple"
            }
        }

