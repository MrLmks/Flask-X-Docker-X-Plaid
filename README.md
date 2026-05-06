# Flask × Docker × Plaid 💳

> A containerized personal finance tracker that connects to your bank account via the Plaid API, aggregates transactions, and delivers automated spending insights — all deployed on AWS EC2 with TLS encryption.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-black?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?logo=postgresql&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-Load%20Balancer-009639?logo=nginx&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazonaws&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

This project is a full-stack DevOps portfolio project built to demonstrate real-world skills across application development, containerization, and cloud deployment.

The application allows users to securely connect their bank account (Revolut, etc.) via **Plaid Link**, retrieve and store their transaction history in **PostgreSQL**, and visualize spending patterns through an interactive dashboard.

### Key features

- 🔗 **Bank connection** via Plaid Link (OAuth flow)
- 📊 **Spending dashboard** with charts by category and over time
- 🗄️ **PostgreSQL** for transaction persistence
- 🔒 **Budget alerts** when a spending category exceeds a defined limit
- 🐳 **Fully containerized** with Docker & Docker Compose
- ⚖️ **Nginx load balancer** distributing traffic across multiple Flask instances
- 🌐 **Deployed on AWS EC2** with HTTPS via Let's Encrypt
- 🔄 **Automatic TLS certificate renewal** via Certbot

---

## Architecture

```
Internet
    │
    ▼
[ Nginx ] ── public network ──────────────────────────
    │                                                  
    ├──▶ [ Flask instance 1 ]  ─┐                     
    ├──▶ [ Flask instance 2 ]  ─┼── private network ──▶ [ PostgreSQL ]
    └──▶ [ Flask instance 3 ]  ─┘                     
```

- **Public network** — only Nginx is exposed to the internet (ports 80 & 443)
- **Private network** — Flask and PostgreSQL communicate internally, never directly reachable from outside

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12 · Flask |
| Banking API | Plaid API (sandbox & production) |
| Frontend | HTML/CSS · Chart.js · Plaid Link JS |
| Database | PostgreSQL 17 |
| Containerization | Docker · Docker Compose |
| Reverse proxy | Nginx (round-robin load balancing) |
| Cloud | AWS EC2 · Ubuntu Server |
| Security | Let's Encrypt · TLS · Docker secrets |
| Version control | Git · GitHub |

---

## Project Structure

```
Flask-X-Docker-X-Plaid/
├── app/
│   ├── templates/          # HTML templates (Jinja2)
│   ├── static/             # CSS, JS, Chart.js assets
│   ├── __init__.py         # Flask app factory
│   ├── routes.py           # Application routes
│   ├── models.py           # Database models
│   └── plaid_client.py     # Plaid API integration
├── nginx/
│   └── nginx.conf          # Nginx load balancer config
├── postgres/
│   └── init.sql            # Database initialization script
├── secrets/                # ⚠️ Local only — never committed to Git
│   ├── db_user             # PostgreSQL username
│   ├── db_password         # PostgreSQL password
│   └── db_password.example # Example file showing expected format
├── Dockerfile              # Production image
├── Dockerfile.dev          # Development image (hot-reload)
├── docker-compose.yml      # Production orchestration
├── docker-compose.dev.yml  # Local development orchestration
├── .env.example            # Environment variables template
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- A free [Plaid developer account](https://dashboard.plaid.com/signup) (sandbox is free, no real bank data needed)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/MrLmks/Flask-X-Docker-X-Plaid.git
cd Flask-X-Docker-X-Plaid
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Open `.env` and fill in your values:

```env
# Flask
FLASK_SECRET_KEY=your_random_secret_key

# Plaid
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_sandbox_secret
PLAID_ENV=sandbox

# Database
POSTGRES_DB=fxdxp-db
```

> ⚠️ Never commit your `.env` file. It is already listed in `.gitignore`.

### 3. Set up Docker secrets

Sensitive credentials (database username and password) are managed via **Docker Compose secrets** — they are injected into containers at runtime via in-memory files and never exposed as environment variables.

```bash
mkdir -p secrets
echo "your_db_username" > secrets/db_user
echo "your_db_password" > secrets/db_password
```

> ⚠️ The `secrets/` folder is listed in `.gitignore` and will never be committed to Git.  
> See `secrets/db_password.example` for the expected file format.

### 4. Run locally (development mode)

```bash
docker compose -f docker-compose.dev.yml up --build
```

The app will be available at `http://localhost:5000` with hot-reload enabled — any change to the Python files restarts Flask automatically, no rebuild needed.

### 5. Run in production mode (local)

```bash
docker compose up --build
```

The full stack starts in the correct order:
1. PostgreSQL starts and becomes healthy
2. Flask starts once PostgreSQL is ready
3. Nginx starts once Flask is healthy and begins load balancing

Access the app at `http://localhost`.

---

## Deployment (AWS EC2)

> 🚧 Work in progress — deployment guide will be added upon completion of Phase 3.

High-level steps:
1. SSH into your EC2 Ubuntu instance
2. Install Docker & Docker Compose
3. Clone this repo
4. Create `.env` and `secrets/` with your production values
5. Run `docker compose up -d`
6. Point your domain to the EC2 public IP
7. Obtain a TLS certificate via Certbot / Let's Encrypt
8. Nginx handles HTTPS termination and redirects HTTP → HTTPS

---

## Roadmap

- [x] Repository setup & project structure
- [x] Flask app — base routes & healthcheck endpoint
- [x] Docker — Dockerfile (prod & dev), hot-reload dev environment
- [x] Docker Compose — full stack with PostgreSQL, Nginx, virtual networks, healthchecks & secrets
- [ ] Flask app — Plaid Link integration & transaction routes
- [ ] PostgreSQL — transaction storage & models
- [ ] Nginx — load balancer with multiple Flask instances
- [ ] AWS EC2 — deployment & HTTPS with Let's Encrypt
- [ ] Automatic TLS certificate renewal

---

## Security

- **Docker Compose secrets** — database credentials are injected at runtime via `/run/secrets/`, never stored in environment variables or committed to Git
- **Network isolation** — Flask and PostgreSQL live on a private internal Docker network, unreachable from the internet
- **Nginx as the only entry point** — only ports 80 and 443 are exposed publicly
- **TLS encryption** — all production traffic is encrypted via Let's Encrypt
- **`.gitignore`** — `.env` and `secrets/` are excluded from version control

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Author

**Raphael** — [@MrLmks](https://github.com/MrLmks)  
DevOps Enthusiast · Building in public
