# Portfolio — Lazaki Chelsoube

Portfolio personnel en deux parties :
- **backend/** — API Django + Django REST Framework (contenu géré depuis l'admin)
- **frontend/** — site statique (HTML/CSS/JS) qui consomme l'API

## 1. Lancer le backend

```bash
cd backend
python -m venv env
# Windows : env\Scripts\activate
# Mac/Linux : source env/bin/activate
pip install -r requirements.txt

python manage.py migrate          # crée la base + pré-remplit ton profil et tes compétences
python manage.py createsuperuser  # crée ton compte admin
python manage.py runserver
```

- API disponible sur : http://127.0.0.1:8000/api/
- Admin disponible sur : http://127.0.0.1:8000/admin/

Depuis l'admin, tu peux dès maintenant :
- modifier ton **Profil** (bio, liens, photo, CV)
- ajouter/modifier tes **Compétences**
- ajouter tes **Réalisations** (projets) avec image, description, liens
- ajouter des **Collaborations**
- consulter les **Messages** reçus via le formulaire de contact

## 2. Lancer le frontend

Ouvre `frontend/index.html` avec l'extension **Live Server** de VS Code
(clic droit → "Open with Live Server"), ou n'importe quel serveur statique.

Le frontend appelle l'API sur `http://127.0.0.1:8000/api` (voir la constante
`API_BASE` en haut de `frontend/js/main.js`). Si tu changes l'adresse ou le
port du backend, mets à jour cette constante.

## 3. Prochaines étapes suggérées

- Ajoute 2-3 projets réels depuis l'admin (`/admin/portfolio/project/add/`)
- Ajoute ta photo de profil
- Renseigne ton lien LinkedIn / Behance dans le Profil si tu en crées un
- Avant mise en ligne : change `SECRET_KEY`, passe `DEBUG = False` et
  restreins `CORS_ALLOW_ALL_ORIGINS` dans `backend/config/settings.py`
