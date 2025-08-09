# Système de Prise de Notes Collaboratives

Un système de prise de notes collaboratives en temps réel avec Django REST Framework et Vue.js.

## Fonctionnalités

- ✅ Authentification JWT
- ✅ Création et édition de notes
- ✅ Collaboration temps réel via WebSocket
- ✅ Partage de notes avec d'autres utilisateurs
- ✅ Historique des versions
- ✅ Interface utilisateur moderne

## Architecture

### Backend (Django REST Framework)
- **API REST** pour la gestion des notes
- **WebSocket** pour la collaboration temps réel
- **JWT** pour l'authentification
- **Redis** pour les channels WebSocket

### Frontend (Vue.js)
- **Vue 3** avec Composition API
- **TypeScript** pour la sécurité des types
- **Pinia** pour la gestion d'état
- **Vue Router** pour la navigation

## Installation

### Prérequis
- Python 3.8+
- Node.js 16+
- Redis (pour WebSocket)

### Backend
```bash
# Activer l'environnement virtuel
env\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Démarrer le serveur
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Démarrage rapide
```bash
# Windows
start.bat
```

## Utilisation

1. **Connexion** : Utilisez les identifiants créés
2. **Créer une note** : Cliquez sur "Nouvelle Note"
3. **Collaborer** : Ajoutez des collaborateurs via le bouton "+"
4. **Édition temps réel** : Les modifications sont synchronisées automatiquement

## API Endpoints

- `POST /api/token/` - Authentification
- `GET /api/notes/` - Liste des notes
- `POST /api/notes/` - Créer une note
- `PATCH /api/notes/{id}/` - Modifier une note
- `POST /api/notes/{id}/add_collaborator/` - Ajouter un collaborateur
- `GET /api/notes/{id}/versions/` - Historique des versions

## WebSocket

- `ws://localhost:8000/ws/notes/{note_id}/` - Collaboration temps réel

## Technologies

**Backend:**
- Django 5.2.5
- Django REST Framework 3.16.1
- Django Channels 4.3.1
- Redis 6.4.0
- JWT 5.5.1

**Frontend:**
- Vue.js 3
- TypeScript
- Pinia
- Vue Router
- Axios

## Production

Pour la production, configurez :
- Base de données PostgreSQL
- Redis pour les sessions
- Serveur ASGI (Daphne/Uvicorn)
- Reverse proxy (Nginx)
- Variables d'environnement pour les secrets