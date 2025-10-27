# PENSAGA Backend - FastAPI + Supabase

Backend API construite avec FastAPI et Supabase pour le projet PENSAGA.

> ⚠️ **Migration Flask → FastAPI** : Ce projet a été migré de Flask vers FastAPI. Consultez `MIGRATION_FASTAPI.md` pour plus de détails.

## 🚀 Installation

### Prérequis

- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)
- Un compte Supabase

### Configuration

1. **Cloner le projet** (si ce n'est pas déjà fait)

2. **Créer un environnement virtuel**

```bash
cd back-end
python -m venv venv
```

3. **Activer l'environnement virtuel**

Sur macOS/Linux :

```bash
source venv/bin/activate
```

Sur Windows :

```bash
venv\Scripts\activate
```

4. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

5. **Configurer les variables d'environnement**

Copier le fichier `.env.example` vers `.env` :

```bash
cp .env.example .env
```

Puis modifier `.env` avec vos valeurs Supabase :

```
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_KEY=votre_cle_anon
```

## 🏃‍♂️ Démarrage

### Démarrage rapide

```bash
./start.sh
```

### Mode développement

```bash
python app.py
```

Ou avec uvicorn directement :

```bash
uvicorn app:app --host 0.0.0.0 --port 5000 --reload
```

L'API sera accessible sur `http://localhost:5000`

### Mode production (avec Uvicorn)

```bash
uvicorn app:app --host 0.0.0.0 --port 5000 --workers 4
```

## 📚 Documentation interactive

FastAPI génère automatiquement une documentation interactive de l'API :

- **Swagger UI** : http://localhost:5000/docs
- **ReDoc** : http://localhost:5000/redoc
- **OpenAPI JSON** : http://localhost:5000/openapi.json

## 📁 Structure du projet

```
back-end/
├── app.py                 # Point d'entrée de l'application
├── requirements.txt       # Dépendances Python
├── .env.example          # Template des variables d'environnement
├── .gitignore            # Fichiers à ignorer par Git
├── config/               # Configuration de l'application
│   ├── __init__.py
│   └── settings.py       # Paramètres et variables d'environnement
├── routes/               # Définition des routes/endpoints
│   ├── __init__.py
│   ├── health.py         # Endpoints de santé
│   └── api.py            # Endpoints API principaux
├── models/               # Modèles de données (Pydantic)
│   └── __init__.py
└── utils/                # Utilitaires
    ├── __init__.py
    └── supabase_client.py # Client Supabase
```

## 🔌 Endpoints disponibles

### Health Check

- `GET /health` - Vérifier l'état de l'API et la connexion Supabase
- `GET /` - Informations de base sur l'API

### API Examples

- `GET /api/example` - Récupérer une liste d'exemples
- `POST /api/example` - Créer un nouvel exemple
- `GET /api/example/<id>` - Récupérer un exemple spécifique
- `PUT /api/example/<id>` - Mettre à jour un exemple
- `DELETE /api/example/<id>` - Supprimer un exemple

## 🔧 Utilisation de Supabase

### Exemple de requête SELECT

```python
from utils.supabase_client import supabase

# Récupérer tous les enregistrements
response = supabase.table('ma_table').select("*").execute()
data = response.data

# Récupérer avec un filtre
response = supabase.table('ma_table').select("*").eq('colonne', 'valeur').execute()
```

### Exemple de requête INSERT

```python
data = {
    'nom': 'Exemple',
    'description': 'Ceci est un exemple'
}
response = supabase.table('ma_table').insert(data).execute()
```

### Exemple de requête UPDATE

```python
data = {'description': 'Nouvelle description'}
response = supabase.table('ma_table').update(data).eq('id', 1).execute()
```

### Exemple de requête DELETE

```python
response = supabase.table('ma_table').delete().eq('id', 1).execute()
```

## 📝 Ajouter de nouvelles routes

1. Créer un nouveau fichier dans le dossier `routes/`
2. Créer un APIRouter FastAPI
3. Enregistrer le Router dans `routes/__init__.py`

Exemple :

```python
# routes/mon_endpoint.py
from fastapi import APIRouter

mon_router = APIRouter()

@mon_router.get('/mon-route')
async def ma_fonction():
    return {'message': 'Ça fonctionne!'}
```

```python
# routes/__init__.py
def register_routes(app):
    from .health import health_router
    from .api import api_router
    from .mon_endpoint import mon_router  # Nouvelle import

    app.include_router(health_router)
    app.include_router(api_router, prefix='/api', tags=['API'])
    app.include_router(mon_router, prefix='/api', tags=['Mon Endpoint'])  # Nouveau router
```

## 🎯 Créer des modèles Pydantic

FastAPI utilise Pydantic pour la validation automatique des données :

```python
# models/example.py
from pydantic import BaseModel
from typing import Optional

class ExampleCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ExampleResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True
```

Utilisation dans les routes :

```python
from models.example import ExampleCreate, ExampleResponse

@api_router.post('/example', response_model=ExampleResponse)
async def create_example(data: ExampleCreate):
    # FastAPI valide automatiquement les données
    return {'id': 1, 'name': data.name, 'description': data.description}
```

## 🧪 Tests

Pour tester l'API, vous pouvez utiliser :

- **Documentation interactive FastAPI** (recommandé)

  - Visitez http://localhost:5000/docs
  - Testez directement les endpoints depuis le navigateur

- **curl**

```bash
curl http://localhost:5000/health
```

- **HTTPie**

```bash
http GET http://localhost:5000/health
```

- **Postman** ou **Insomnia** pour une interface graphique

- **Tests automatisés avec pytest**

```bash
pip install pytest httpx
pytest
```

## 🔒 Sécurité

- Ne jamais committer le fichier `.env`
- Utiliser des variables d'environnement pour les secrets
- Valider toutes les entrées utilisateur
- Utiliser HTTPS en production
- Limiter les requêtes (rate limiting) si nécessaire

## ⚡ Avantages de FastAPI

- **Performance** : Un des frameworks Python les plus rapides
- **Documentation automatique** : Swagger UI et ReDoc générés automatiquement
- **Validation automatique** : Grâce à Pydantic
- **Support async natif** : Améliore les performances I/O
- **Type hints** : Meilleure autocomplétion et détection d'erreurs
- **Standards modernes** : OpenAPI, JSON Schema

## 📚 Ressources

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [Documentation Supabase Python](https://supabase.com/docs/reference/python/introduction)
- [Documentation Pydantic](https://docs.pydantic.dev/)
- [Guide de migration Flask → FastAPI](MIGRATION_FASTAPI.md)

## 🤝 Contribution

1. Créer une branche pour votre fonctionnalité
2. Commiter vos changements
3. Pousser vers la branche
4. Créer une Pull Request

## 📄 Licence

À définir selon les besoins du projet.
