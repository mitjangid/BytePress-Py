# Headlines News Portal - Architecture & Technical Design

## 1. System Overview & Technical Stack

Headlines is architected as a modular, lightweight Django 5.x monolith designed for maximum speed, low memory overhead, and SEO dominance.

```
                  +-----------------------------------+
                  |         Nginx (Reverse Proxy)     |
                  +-----------------+-----------------+
                                    |
          +-------------------------+-------------------------+
          |                                                   |
          v                                                   v
+-------------------+                               +-------------------+
|  Django Application|                              |   Static / Media  |
|  (Gunicorn WSGI)  |                              |    Storage        |
+---------+---------+                               +-------------------+
          |
    +-----+--------------------+--------------------+
    |                          |                    |
    v                          v                    v
+-------+                +-----------+       +--------------+
|  PostgreSQL 16         |   Redis   |       | Celery Worker|
|  (Full-Text Search)    |  (Cache)  |       | & Celery Beat|
+-------+                +-----------+       +--------------+
```

---

## 2. Django App Modular Structure

- **`accounts`**: Custom User model, Role choices, Django Permission groups, User Profiles, Author verification.
- **`taxonomy`**: MPTT Category hierarchy tree, State/City Location model, GeoIP service adapter (`django-ipware`).
- **`articles`**: Core `Article` model, workflow state machine (`Draft` -> `Pending Review` -> `Published` -> `Archived`), revision snapshot engine, tagging, co-authorship mapping.
- **`seo`**: Slug auto-generation, automatic 301 `Redirect` tracking middleware, Schema.org JSON-LD structured data generator, XML sitemap engine.
- **`media_lib`**: Asset processing pipeline (Pillow WebP conversion, thumbnail generation, mandatory alt-text validation), video embed parser.
- **`engagement`**: Threaded HTMX `Comment` system, moderation queue, anti-spam rate limiter, newsletter subscription manager, bookmarks.
- **`core`**: Dynamic `HomepageLayout` block configuration, Singleton `SiteSetting` model, customized Jazzmin admin dashboard.
- **`api`**: Django REST Framework endpoints for public JSON feeds, search, and headless/mobile client access.

---

## 3. Database Schema Relationships

### Core Entity Relationships
- **Article -> User (Author)**: `ForeignKey` (Many-to-One)
- **Article -> User (Co-Authors)**: `ManyToManyField`
- **Article -> Category (Primary)**: `ForeignKey` (Many-to-One)
- **Article -> Category (Secondary)**: `ManyToManyField`
- **Article -> Location**: `ForeignKey` (Many-to-One, optional)
- **Article -> MediaAsset**: `ForeignKey` (Main featured image)
- **Comment -> Article**: `ForeignKey` (Many-to-One)
- **Comment -> Comment (Parent)**: `ForeignKey` (Self-referential for threaded replies)

---

## 4. Cache & Performance Strategy

### Redis Caching Architecture
- **Template Fragment Caching**: Header nav, category menus, breaking news ticker, and homepage layout blocks cached in Redis (`cache_page` and `{% cache %}`).
- **Cache Invalidation**: Signal-based cache clearing (`post_save` on `Article`, `Category`, and `HomepageLayout` models invalidates affected cache keys immediately).
- **Session & Rate Limiting Storage**: Redis handles user sessions and rate limiting counters for comment submissions and search requests.

---

## 5. PostgreSQL Full-Text Search

- Uses built-in `SearchVector`, `SearchQuery`, and `SearchRank` on `Article.title`, `Article.summary`, and `Article.content`.
- GIN Index created on search vectors for instant execution without Elasticsearch dependency.

---

## 6. Celery Background Worker Engine

- **Scheduled Publishing**: Celery Beat checks every minute for articles with `status=PUBLISHED` and `scheduled_at <= now()`.
- **Sitemap Regeneration**: Asynchronous sitemap rebuilding when new articles are published.
- **Email Digest Dispatch**: Scheduled sending of newsletter digest emails.
