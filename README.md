# PENSAGA Backend - Flask + Supabase

Backend API construite avec Flask et Supabase pour le projet PENSAGA.

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
SECRET_KEY=votre_cle_secrete_flask
```

## 🏃‍♂️ Démarrage

### Mode développement

```bash
python app.py
```

L'API sera accessible sur `http://localhost:5000`

### Mode production (avec Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

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
2. Créer un Blueprint Flask
3. Enregistrer le Blueprint dans `routes/__init__.py`

Exemple :

```python
# routes/mon_endpoint.py
from flask import Blueprint, jsonify

mon_bp = Blueprint('mon_endpoint', __name__)

@mon_bp.route('/mon-route', methods=['GET'])
def ma_fonction():
    return jsonify({'message': 'Ça fonctionne!'})
```

```python
# routes/__init__.py
def register_routes(app):
    from .health import health_bp
    from .api import api_bp
    from .mon_endpoint import mon_bp  # Nouvelle import

    app.register_blueprint(health_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(mon_bp, url_prefix='/api')  # Nouveau blueprint
```

## 🧪 Tests

Pour tester l'API, vous pouvez utiliser :

- **curl**

```bash
curl http://localhost:5000/health
```

- **HTTPie**

```bash
http GET http://localhost:5000/health
```

- **Postman** ou **Insomnia** pour une interface graphique

## 🔒 Sécurité

- Ne jamais committer le fichier `.env`
- Utiliser des variables d'environnement pour les secrets
- Valider toutes les entrées utilisateur
- Utiliser HTTPS en production
- Limiter les requêtes (rate limiting) si nécessaire

## 📚 Ressources

- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation Supabase Python](https://supabase.com/docs/reference/python/introduction)
- [Documentation Pydantic](https://docs.pydantic.dev/)

## 🤝 Contribution

1. Créer une branche pour votre fonctionnalité
2. Commiter vos changements
3. Pousser vers la branche
4. Créer une Pull Request

## 📄 Licence

À définir selon les besoins du projet.
