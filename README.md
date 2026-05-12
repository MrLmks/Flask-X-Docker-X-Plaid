Voici le nouveau README.md, prêt à être copié-collé sur GitHub :


# Flask × Docker × Plaid 💳

> Application Fintech de finances personnelles, conteneurisée et sécurisée, connectée aux banques via Plaid.  
> Authentification, dashboard de dépenses, historique et visualisation par catégories.  
> Développée avec Flask, orchestrée par Docker Compose, prête pour un déploiement AWS EC2.

---

## Aperçu

L'application permet à un utilisateur de **créer un compte**, de se **connecter** de manière sécurisée, puis de **lier sa banque** (via Plaid Link). Ses transactions sont automatiquement agrégées et stockées. Il peut alors consulter :

- Un **dashboard** avec un graphique camembert de ses dépenses par catégorie.
- Une page **Balance** avec le solde total, l'historique complet et les logos des commerçants.

L'interface est sobre, responsive et moderne, construite avec HTML/CSS et Chart.js.

---

## Fonctionnalités

- 🔐 **Authentification complète** : inscription, connexion, déconnexion, mots de passe hachés.
- 🔗 **Connexion bancaire** via Plaid Link (sandbox ou production).
- 📊 **Dashboard** : camembert interactif par catégorie, affichant les totaux en dollars.
- 💰 **Balance** : solde total calculé automatiquement, historique des transactions avec logos.
- 🐳 **Conteneurisation** : Docker & Docker Compose, avec un mode développement performant.
- ⚖️ **Nginx** : reverse proxy (round‑robin) en production.
- 🌐 **AWS EC2 ready** : déploiement avec HTTPS (Let's Encrypt / Certbot).
- 🛡️ **Sécurité** : Docker secrets, réseau interne isolé, sessions Flask‑Login, clés secrètes.
- 📈 **Données sandbox** : script SQL de `seed` pour enrichir les catégories de test.

---

## Architecture

```
Internet
    │
    ▼
[ Nginx ] ── réseau public ──────────────────────────
    │
    ├──▶ [ Flask instance 1 ]
    ├──▶ [ Flask instance 2 ]  ── réseau privé ──▶ [ PostgreSQL ]
    └──▶ [ Flask instance 3 ]
```

- Seul Nginx est exposé (ports 80 & 443).
- Flask et PostgreSQL communiquent sur un réseau Docker interne, jamais accessible de l'extérieur.

---

## Stack technique

| Couche            | Technologie                               |
| ----------------- | ----------------------------------------- |
| Backend           | Python 3.12 · Flask                       |
| Banking API       | Plaid API (sandbox & production)          |
| Authentification  | Flask-Login · Werkzeug (hashage)          |
| Frontend          | HTML5 · CSS3 · Chart.js · Plaid Link JS   |
| Base de données   | PostgreSQL 17                             |
| Conteneurisation  | Docker · Docker Compose · Watch (dev)     |
| Reverse proxy     | Nginx (round‑robin load balancing)        |
| Cloud             | AWS EC2 · Ubuntu · Let's Encrypt · Certbot|
| Versionning       | Git · GitHub                              |

---

## Structure du projet

```
Flask-X-Docker-X-Plaid/
├── app/
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/
│   │       ├── dashboard-graph.js
│   │       └── plaid-connect.js
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── balance.html
│   │   ├── login.html
│   │   └── register.html
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── plaid_client.py
│   └── utils.py
├── nginx/
│   └── nginx.conf
├── postgres/
│   ├── init.sql
│   └── seed.sql
├── secrets/                  # ⚠️ local uniquement
│   ├── db_user
│   ├── db_password
│   └── db_password.example
├── docker-compose.yml        # Production
├── docker-compose.dev.yml    # Développement (Watch)
├── Dockerfile
├── Dockerfile.dev
├── .env.example
├── requirements.txt
└── README.md
```

---

## Démarrage rapide

### Prérequis

- Docker & Docker Compose
- Un compte développeur Plaid (gratuit, sandbox)
- Git

### 1. Cloner le dépôt

```bash
git clone https://github.com/MrLmks/Flask-X-Docker-X-Plaid.git
cd Flask-X-Docker-X-Plaid
```

### 2. Fichier d'environnement

```bash
cp .env.example .env
```

Remplissez vos clés Plaid et votre `FLASK_SECRET_KEY` dans le `.env`.

### 3. Secrets Docker (base de données)

```bash
mkdir -p secrets
echo "votre_utilisateur" > secrets/db_user
echo "votre_mot_de_passe" > secrets/db_password
```

> Les dossiers `secrets/` et `.env` sont déjà dans `.gitignore`. Ils ne seront jamais versionnés.

### 4. Lancer l'application (développement)

```bash
docker compose -f docker-compose.dev.yml up --build
```

Ouvrez `http://localhost:5001`.

### 5. Créer un compte et lier une banque

- Allez sur `/register` pour créer un utilisateur.
- Connectez‑vous.
- Sur le Dashboard, cliquez sur « Connect To Your Bank » pour ouvrir Plaid Link (utilisez les identifiants sandbox : `user_good` / `pass_good`).
- Lancez l'import des transactions :

```bash
curl http://localhost:5001/api/fetch_transaction
```

### 6. (Optionnel) Enrichir les catégories

```bash
docker compose -f docker-compose.dev.yml exec -T db psql -U admin -d fxdxp_db < postgres/seed.sql
```

Rechargez le dashboard, le camembert affichera des catégories variées.

---

## Roadmap

- ✅ Authentification (register, login, logout, sessions)
- ✅ Dashboard avec camembert
- ✅ Page Balance (solde + historique + logos)
- ✅ Import des transactions Plaid
- ✅ Script de `seed` pour les données sandbox
- ✅ Mode développement avec Docker Compose Watch
- ✅ Architecture Nginx + réseaux isolés
- 🔜 Déploiement AWS EC2 & HTTPS (Let's Encrypt)
- 🔜 Renouvellement automatique des certificats TLS
- 🔜 Tests unitaires et d'intégration

---

## Sécurité

- **Docker secrets** : les credentials de la base de données sont injectés via `/run/secrets/`, jamais dans les variables d'environnement.
- **Isolation réseau** : Flask et PostgreSQL vivent sur un réseau Docker interne, inaccessibles depuis l'extérieur.
- **Nginx** : seul point d'entrée public (ports 80/443).
- **TLS** : chiffrement de tout le trafic en production via Let's Encrypt.
- **Mots de passe** : hashés avec `scrypt` (Werkzeug).
- **`.gitignore`** : `.env` et `secrets/` exclus du versionnement.

---

## Licence

Ce projet est sous licence MIT – voir le fichier [LICENSE](LICENSE).

---

## Auteur

**Raphael** – [@MrLmks](https://github.com/MrLmks)
DevOps Enthusiast · Building in public
