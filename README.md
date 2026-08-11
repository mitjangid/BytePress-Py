# Headlines 📰
> Open-Source, Lightweight, High-Performance Python & Django News Portal CMS

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Django 5.x](https://img.shields.io/badge/django-5.x-green.svg)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Headlines is a production-ready, open-source News Portal CMS built with **Django 5.x**, **PostgreSQL**, **Redis**, **Celery**, **HTMX**, **Alpine.js**, and **Tailwind CSS**. It provides digital newsrooms, publishers, and multi-author blogs with enterprise-grade publishing workflows without SaaS vendor lock-in or complex single-page app bloat.

---

## ⚡ Core Features

- 👤 **Granular RBAC**: 6 Pre-configured roles (Super Admin, Admin, Editor, Author, Moderator, Subscriber).
- 📰 **Editorial Workflow Engine**: `Draft` -> `Pending Review` -> `Published` -> `Archived` state machine with mandatory alt-text validation and revision snapshots.
- ⏰ **Scheduled Publishing**: Background Celery Beat scheduler for automated timed publication.
- 🏷️ **Hierarchical Taxonomy**: Multi-level categories powered by MPTT + State/City geographical news filtering.
- 📍 **Auto Local News Detection**: Client IP GeoIP auto-detection via `django-ipware` + MaxMind GeoLite2.
- 🚀 **SEO Optimization**: Auto-slugs, automatic 301 redirect manager for changed slugs, Schema.org JSON-LD tags, dynamic XML sitemaps, editable `robots.txt`.
- 🖼️ **Media Processing**: Auto Pillow/django-imagekit image compression & WebP format conversion + YouTube/Vimeo embed parser.
- 💬 **Interactive Reader Frontend**: Threaded HTMX comments with moderation queue and anti-spam heuristics, light/dark mode toggle via Alpine.js.
- 🎛️ **Dynamic Homepage Layout**: Admin-configurable content blocks (`HomepageLayout` model) allowing instant rearrangement without deploys.

---

## 📚 Project Documentation

All system documentation is stored inside the [`docs/`](./docs) directory:

| Document | Description |
| :--- | :--- |
| 📋 [**Feature List**](./docs/features.md) | Exhaustive breakdown of features per Django app |
| 🗓️ [**Sprint Roadmap**](./docs/sprints_plan.md) | Agile 9-sprint development plan & deliverables |
| 🏗️ [**Architecture Guide**](./docs/architecture.md) | Technical stack diagram, database ERD, caching & Celery design |
| 🔐 [**Permissions Matrix**](./docs/permissions_matrix.md) | Comprehensive mapping of roles to Django model permissions |
| 🐳 [**Deployment Guide**](./docs/deployment_guide.md) | Production setup with Docker Compose, Nginx, Gunicorn, SSL |
| 🔌 [**API Documentation**](./docs/api_docs.md) | DRF REST API endpoints for headless and PWA integration |
| 🔑 [**Third-Party Setup**](./docs/third_party_setup.md) | GeoIP setup, SMTP email credentials, S3 storage, and VAPID push keys |
| 🔑 [**Sample Credentials**](./docs/sample_credentials.md) | Demo user accounts (Admin, Editor, Author) and Aiven Postgres DB connection |
| 🌐 [**User URLs & Credentials**](./docs/user_urls_and_credentials.md) | Role-wise accessible routes, portals, and login credentials |
| 📋 [**User Features Breakdown**](./docs/user_features_breakdown.md) | Role-by-role (User by User) comprehensive feature specification breakdown |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, Django 5.x
- **Database**: PostgreSQL 16 (Full-Text Search via GIN index)
- **Cache & Message Broker**: Redis 7
- **Task Queue**: Celery + Celery Beat
- **Frontend**: Django Templates + HTMX + Alpine.js + Tailwind CSS
- **Media**: Pillow + `django-imagekit` + WebP conversion
- **Containerization**: Docker & Docker Compose

---

## 🚀 Quickstart with Docker

```bash
# 1. Clone repository
git clone https://github.com/your-org/headlines.git
cd headlines

# 2. Copy environment file
cp .env.example .env

# 3. Build & start services
docker compose up -d --build

# 4. Apply database migrations
docker compose exec web python manage.py migrate

# 5. Create superuser account
docker compose exec web python manage.py createsuperuser

# 6. Seed demo content (categories, locations, sample articles)
docker compose exec web python manage.py seed_data
```

Access the portal at `http://localhost:8000` and the Admin dashboard at `http://localhost:8000/admin/`.

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).
