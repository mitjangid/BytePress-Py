# Headlines News Portal - Development Sprint Plan & Roadmap

## Overview & Sprint Methodology
This roadmap breaks the development of the Headlines News Portal CMS into **9 incremental sprints**. Each sprint delivers a complete, testable layer of functionality, building from core infrastructure up to the reader UI and deployment setup.

---

## Sprint Roadmap Matrix

| Sprint | Focus Area | Primary Deliverables | Key Dependencies |
| :--- | :--- | :--- | :--- |
| **Sprint 0** | Infrastructure & Project Base | Django 5 project init, Dockerfile, `docker-compose.yml`, Tailwind CSS CLI, Postgres/Redis setup | Environment |
| **Sprint 1** | `accounts` App | Custom `User` model, role choices, `Group` permissions setup, user profiles | Django Auth |
| **Sprint 2** | `taxonomy` App | MPTT `Category` & `Location` models, GeoIP auto-detection integration, admin views | `accounts` |
| **Sprint 3** | `media_lib` & `articles` Apps | `MediaAsset` (WebP converter, alt-text rule), `Article` model, workflow state engine, revisions | `accounts`, `taxonomy` |
| **Sprint 4** | `seo` App | Auto-slugs, 301 `Redirect` tracking middleware, Schema.org JSON-LD, Celery sitemap generator | `articles` |
| **Sprint 5** | `engagement` App | HTMX `Comment` system, moderation queue, Akismet-style spam heuristic, `NewsletterSubscriber` | `articles`, `accounts` |
| **Sprint 6** | `core` App | `HomepageLayout` dynamic block manager, `SiteSetting` singleton, Jazzmin dashboard custom analytics | All previous apps |
| **Sprint 7** | Frontend Templates & PWA | Tailwind styling, HTMX live search/comments, Alpine.js dark/light mode toggle, PWA service worker | Frontend static assets |
| **Sprint 8** | `api` App & Seed Command | DRF endpoints, `seed_data` management command, unit testing suite, Docker container verification | End-to-end system |

---

## Detailed Sprint Specifications

### 🚀 Sprint 0: Environment Setup & Project Scaffolding
- Initialize Git repository and `.gitignore`.
- Set up Virtual Environment & `requirements.txt` / `pyproject.toml`:
  - `Django>=5.0`, `psycopg2-binary`, `redis`, `celery`, `django-mptt`, `django-storages`, `Pillow`, `django-imagekit`, `django-autoslug`, `django-ipware`, `django-jazzmin`, `djangorestframework`, `django-ratelimit`.
- Create Django project `config` / `headlines_cms`.
- Create base Docker environment:
  - `docker-compose.yml` defining services: `web` (Django), `db` (PostgreSQL 16), `redis` (Redis 7), `celery_worker`, `celery_beat`, `nginx`.
- Configure Tailwind CSS via standalone CLI or Node asset pipeline.

---

### 👤 Sprint 1: `accounts` App & Permissions Engine
- Scaffold `accounts` app.
- Define custom `User` model inheriting `AbstractUser`.
- Create Role Enum & Django Group signals:
  - Automatically create and assign permissions for standard groups: `Super Admin`, `Admin`, `Editor`, `Author`, `Moderator`, `Subscriber`.
- Implement `UserProfile` model with bio, social media handles, avatar.
- Write tests for custom roles, permissions, and group assignment signals.

---

### 🏷️ Sprint 2: `taxonomy` App & Geolocation Engine
- Scaffold `taxonomy` app.
- Implement `Category` model using `django-mptt` (`TreeForeignKey`, hierarchy level support).
- Implement `Location` model (State -> City hierarchy).
- Integrate `django-ipware` helper service for client IP extraction & MaxMind GeoLite2 lookup.
- Register `CategoryAdmin` and `LocationAdmin` with MPTT tree view in Django admin.

---

### 📰 Sprint 3: `media_lib` & `articles` Core Editorial Engine
- Scaffold `media_lib` app:
  - `MediaAsset` model with automatic Pillow image compression and WebP format conversion.
  - Video embed model and YouTube embed code parser.
- Scaffold `articles` app:
  - `Article` model with state choices (`DRAFT`, `PENDING_REVIEW`, `PUBLISHED`, `ARCHIVED`).
  - Content flags: `is_breaking`, `is_featured`, `is_trending`, `is_editors_pick`.
  - State transition manager with validation enforcing `alt_text` requirement on published media.
  - `ArticleRevision` system saving historical snapshots on save with rollback capability.
  - Tagging model integration.
  - `Celery` task for scheduled article publishing at `scheduled_at` timestamp.

---

### 🔍 Sprint 4: `seo` App & Traffic Engineering
- Scaffold `seo` app.
- Implement auto-slug engine via `django-autoslug` with manual override.
- Implement `Redirect` model and Django middleware for automatic 301 permanent redirect handling when slugs change.
- JSON-LD structured data generator (`NewsArticle`, `BreadcrumbList`, `Organization`).
- Asynchronous sitemap generator task (`Celery`) generating split XML sitemaps (`/sitemap.xml`, `/sitemap-articles.xml`).
- Dynamic `robots.txt` view reading from `SiteSetting`.

---

### 💬 Sprint 5: `engagement` App & Reader Interaction
- Scaffold `engagement` app.
- Implement `Comment` model supporting nested threaded replies.
- Build comment moderation workflow (Pending, Approved, Flagged, Rejected).
- Anti-spam heuristic filter (link count limit, duplicate content check, IP rate limiting via `django-ratelimit`).
- `Bookmark` model for reader saved articles list.
- `NewsletterSubscriber` model with UUID double opt-in verification.
- Celery weekly newsletter digest dispatch task.

---

### 🎛️ Sprint 6: `core` App & Admin Dashboard
- Scaffold `core` app.
- Implement `HomepageLayout` model to allow admins to order, enable/disable layout blocks (Hero, Breaking Ticker, Trending Grid, State Rows).
- Implement `SiteSetting` singleton model (Logo, Favicon, Brand Colors, Contact details, Footer content).
- Customize `django-jazzmin` admin dashboard:
  - Custom stats widgets: Articles Pending Review count, Top 10 Most Viewed Articles, Moderation Queue backlog.

---

### 🎨 Sprint 7: Reader Frontend (HTMX + Alpine.js + Tailwind)
- Design server-rendered responsive templates:
  - Base Layout, Navigation bar with active category dropdowns, Footer, Breaking News Ticker.
  - Homepage powered by `HomepageLayout` configuration.
  - Article Detail page with rich typography, author bio card, social sharing buttons, auto-suggested articles.
  - Category & Location landing pages with filtering combinations.
- Build HTMX interactive features:
  - Dynamic infinite-scroll / pagination.
  - Live search overlay with instant filtering.
  - HTMX inline comment posting without page refresh.
- Implement Alpine.js features:
  - Dark / Light mode toggle with CSS variables and local storage persistence.
  - Mobile drawer menu.
- PWA setup: `manifest.json`, service worker registration, installable web app capability.

---

### 🔌 Sprint 8: `api` App, Seed Command & End-to-End Verification
- Scaffold `api` app using Django REST Framework (DRF):
  - Read-only endpoints for mobile/PWA access: `/api/v1/articles/`, `/api/v1/categories/`, `/api/v1/search/`.
- Create `seed_data` management command (`python manage.py seed_data`):
  - Populates realistic demo categories, states/cities, sample authors, and 20+ sample news articles with images.
- Comprehensive Unit & Integration Test Suite run (`python manage.py test`).
- Final Docker container build & execution check (`docker-compose up --build`).
