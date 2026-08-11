# Headlines News Portal - Deployment & Operations Guide

## 1. Production Overview

Headlines is deployed using Docker and Docker Compose on standard Linux VPS environments (Ubuntu 22.04 / 24.04 LTS recommended).

### Services Stack
- **`nginx`**: Front-facing reverse proxy, SSL termination, static/media file serving.
- **`web`**: Gunicorn WSGI server running Django application container.
- **`db`**: PostgreSQL 16 database server.
- **`redis`**: Cache store, session backend, and Celery message broker.
- **`celery_worker`**: Asynchronous task worker for background jobs.
- **`celery_beat`**: Scheduled task scheduler (article publishing, sitemap regeneration).

---

## 2. Environment Configuration (`.env`)

Create a production `.env` file in the root directory:

```ini
DEBUG=False
SECRET_KEY=your-production-secret-key-min-50-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_ENGINE=django.db.backends.postgresql
DB_NAME=headlines_db
DB_USER=headlines_user
DB_PASSWORD=your_secure_password
DB_HOST=db
DB_PORT=5432

REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1

MEDIA_STORAGE_BACKEND=local
```

---

## 3. Deployment Steps

### Step 1: Clone Repository & Configure Environment
```bash
git clone https://github.com/your-org/headlines.git
cd headlines
cp .env.example .env
# Edit .env with production credentials
```

### Step 2: Build & Launch Docker Containers
```bash
docker compose -f docker-compose.yml up -d --build
```

### Step 3: Run Database Migrations & Create Superuser
```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py collectstatic --no-input
```

### Step 4: Seed Initial Data (Optional)
```bash
docker compose exec web python manage.py seed_data
```

---

## 4. Nginx Production Reverse Proxy Config

Example Nginx server block configuration (`/etc/nginx/sites-available/headlines`):

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    client_max_body_size 20M;

    location /static/ {
        alias /var/www/headlines/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /media/ {
        alias /var/www/headlines/mediafiles/;
        expires 7d;
        add_header Cache-Control "public, no-transform";
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 5. Maintenance Commands

- **Backup Database**:
  ```bash
  docker compose exec db pg_dump -U headlines_user headlines_db > backup_$(date +%Y%m%d).sql
  ```
- **View Container Logs**:
  ```bash
  docker compose logs -f web celery_worker
  ```
