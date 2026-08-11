# Headlines News Portal - Third-Party Integrations & Configuration Guide

This guide details all third-party services, environment keys, and operational setup required for full production features.

---

## 1. GeoIP Location Auto-Detection (MaxMind GeoLite2)

Headlines uses `django-ipware` alongside MaxMind GeoLite2 to automatically resolve a visitor's IP address to their state and city.

### Setup Instructions:
1. Create a free account at [MaxMind GeoLite2](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data).
2. Download the `GeoLite2-City.mmdb` database file.
3. Place the `.mmdb` file in the project directory: `d:\Projects\Python\Headlines\geoip\GeoLite2-City.mmdb`.
4. Add the following setting to `config/settings.py` (or `.env`):
   ```python
   GEOIP_PATH = BASE_DIR / 'geoip'
   ```

---

## 2. Cloud Media Storage (S3 / DigitalOcean Spaces / MinIO)

By default, Headlines stores uploaded images locally in `/media/`. To scale to cloud media storage without code changes:

### Environment Settings (`.env`):
```ini
MEDIA_STORAGE_BACKEND=s3
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_S3_REGION_NAME=us-east-1
AWS_S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com # Optional for S3-compatible services
```

---

## 3. Email & Newsletter Digest Dispatch (SMTP / SendGrid / Postmark)

To enable double opt-in email verification and Celery newsletter digest dispatches:

### Environment Settings (`.env`):
```ini
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your_sendgrid_api_key
DEFAULT_FROM_EMAIL=Headlines Newsroom <newsletter@yourdomain.com>
```

---

## 4. Background Workers (Celery & Redis)

Scheduled article publishing, sitemap rebuilding, and digest sending run via Celery:

### Starting Celery Worker:
```bash
celery -A config worker --loglevel=info
```

### Starting Celery Beat Scheduler:
```bash
celery -A config beat --loglevel=info
```

---

## 5. Web Push Notifications (VAPID Keys Setup)

To send instant browser push notifications for breaking news:
1. Generate VAPID key pairs using `webpush` CLI or `pywebpush`:
   ```bash
   pip install pywebpush
   vapid --gen
   ```
2. Store keys in `.env`:
   ```ini
   VAPID_PUBLIC_KEY=your_public_key
   VAPID_PRIVATE_KEY=your_private_key
   VAPID_ADMIN_EMAIL=admin@yourdomain.com
   ```

---

## 6. Action Items / Help Required From User

| Action Item | Priority | Purpose | Instructions |
| :--- | :---: | :--- | :--- |
| **MaxMind GeoLite2** | Optional | IP-based local news auto-detection | Download `GeoLite2-City.mmdb` into `geoip/` directory |
| **SMTP Credentials** | Recommended | Send newsletter digests & user notifications | Update `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `.env` |
| **Domain SSL & Nginx** | Production | Secure HTTPS traffic and static asset serving | Follow [`docs/deployment_guide.md`](./deployment_guide.md) |
