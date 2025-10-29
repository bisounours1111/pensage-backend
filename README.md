# PENSAGA Backend — FastAPI + Supabase

API backend du projet PENSAGA, construite avec FastAPI, Supabase et Stripe.

## ⚙️ Prérequis

- Python 3.9+
- pip
- Accès Supabase (URL + Anon key)
- Clé Stripe (si paiement activé)
- Optionnel sur Windows: WSL ou PowerShell (exécution de scripts)

## 🚀 Installation et démarrage

1) Cloner le dépôt et se placer dans le dossier

```bash
git clone <URL_DU_REPO>
cd back-end
```

2) Créer et activer l’environnement virtuel

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3) Installer les dépendances

```bash
pip install -r requirements.txt
```

4) Configurer les variables d’environnement

Créer un fichier `.env` à la racine de `back-end/` (à partir d’un modèle si disponible) et remplir au minimum:

```
SUPABASE_URL=https://votre-projet.supabase.co
SUPABASE_KEY=cle_anon_supabase
...
```

5) Lancer l’API en développement

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

L’API est disponible sur `http://localhost:8000`.

6) Production (exemple Uvicorn workers)

## 📚 Documentation interactive

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## 📁 Structure du projet

```
back-end/
├── app.py
├── requirements.txt
├── config/
├── routes/
├── models/
└── utils/
```

## ✅ Vérification rapide

```bash
curl http://localhost:8000/health
```

Vous devez obtenir un statut « ok ».

## 🤝 Contribution

1. Créer une branche de fonctionnalité
2. Commiter et pousser
3. Ouvrir une Pull Request

## 📄 Licence

Copyright (c) 2025 Yanis DAÏ, Enzo Gérardot, Carla Dupont, Théo Sauval

Ce projet a été réalisé dans un cadre strictement pédagogique dans le cadre du hackathon Ynov 2025.  
Conformément à l'article 1.4 du règlement intérieur Ynov, les droits patrimoniaux et moraux
demeurent la propriété exclusive de ses auteurs.

Toute utilisation, reproduction, modification, diffusion ou exploitation, totale ou partielle, du code
en dehors du cadre d'évaluation pédagogique est strictement interdite sans l'accord écrit
préalable des auteurs.
