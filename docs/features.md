# Headlines News Portal - Feature Specifications

## Overview
Headlines is an open-source, lightweight, high-performance Django 5.x CMS tailored for digital news outlets, publishing organizations, and multi-author publications.

---

## 1. Authentication & Role-Based Access Control (`accounts`)
- **Custom User Model**:
  - Email-based or username-based authentication.
  - Avatar support, bio, social media profiles (Twitter, Facebook, personal website).
  - Verified Author badge.
- **Roles & Permissions**:
  - **Super Admin**: System-wide configuration, database backups, user roles management.
  - **Admin**: User management, category/location hierarchy management, moderation override.
  - **Editor**: Content approval workflow (approve, reject, publish, schedule), breaking news flags, featured news, co-author assignments.
  - **Author / Reporter**: Draft creation, submission for review, personal profile management, personal story analytics.
  - **Moderator**: Reader comment moderation queue, flagging/unflagging comments.
  - **Subscriber / Reader**: Article bookmarking, comment posting, newsletter subscriptions, location preferences.

---

## 2. Taxonomy & Localized News (`taxonomy`)
- **Hierarchical Categories**:
  - Tree-structured categories (e.g. World -> Europe -> UK News) powered by MPTT.
  - Custom category display ordering, icon support, description, and custom SEO title/meta tag fields.
- **State & City Locations**:
  - Two-tier geographical classification: States / Regions and Cities.
  - IP-based auto-detection (`django-ipware` + MaxMind GeoLite2) to prioritize local news on the homepage.
  - Combined filtering: Category + Location combinations (e.g. "Sports in California").

---

## 3. Editorial & Content Management (`articles`)
- **Rich Text Article Editor**:
  - Tiptap / CKEditor integration for rich formatting, inline image drop, blockquotes, code snippets, and embedded videos.
- **Workflow State Management**:
  - States: `Draft` -> `Pending Review` -> `Published` -> `Archived`.
  - Logging of state transitions with author/editor notes and timestamps.
- **Publishing Controls**:
  - Instant publishing or scheduled publishing via Celery Beat tasks.
  - Content flags: `Breaking News` (powers ticker), `Featured`, `Trending`, `Editor's Pick`.
- **Revision History & Rollback**:
  - Auto-saved snapshots on edit with diff visualization and one-click rollback.
- **Multi-Author Support**:
  - Primary author + unlimited co-authors/contributors.
- **Tags & Related Content**:
  - Dynamic Tagging system.
  - Auto-suggested related articles (TF-IDF or shared tag/category algorithm) with manual editor override list.

---

## 4. SEO & Traffic Optimization (`seo`)
- **Slugs & Canonical URLs**:
  - Auto-generated unique slug from title with manual edit capability.
  - Canonical tags for all pages to avoid duplicate content penalties.
- **Automatic 301 Redirect Manager**:
  - Automatically captures old slug when an article or category title is changed and creates a 301 permanent redirect to the new URL.
- **Structured Data (Schema.org)**:
  - Valid JSON-LD injection for `NewsArticle`, `BreadcrumbList`, and `Organization`.
- **XML Sitemaps**:
  - Paginated, auto-generated sitemaps split by content type (`sitemap-articles.xml`, `sitemap-categories.xml`, `sitemap-news-google.xml`).
  - Asynchronous background regeneration via Celery upon publication.
- **Robots.txt & Meta Controls**:
  - Editable `robots.txt` directly from Django admin.
  - Editable per-page Open Graph (OG) and Twitter Card tags.

---

## 5. Media Library & Assets (`media_lib`)
- **Asset Processing Pipeline**:
  - Automatic image resizing, optimization, and WebP format conversion using Pillow/django-imagekit.
- **Accessibility & Compliance**:
  - Hard validation requiring `alt_text` before an article with images can transition to `Published`.
- **Video Embeds**:
  - Automated YouTube & Vimeo URL parser yielding responsive iframe embeds + custom thumbnail generation.

---

## 6. Reader Engagement & Interactivity (`engagement`)
- **Comment System**:
  - Threaded (nested replies) comment section.
  - Moderation queue for pending comments.
  - Basic anti-spam heuristics (link count threshold, duplicate detection, IP rate limiting via `django-ratelimit`).
- **Bookmarks & Saved Reading List**:
  - Readers can bookmark articles for later reading with local storage sync for non-logged-in visitors.
- **Newsletter & Email Digest**:
  - Subscriber registration with double opt-in.
  - Celery-scheduled weekly digest emails generated automatically from top-performing articles.
- **Web Push Notifications**:
  - Web Push service worker integration for breaking news alerts.

---

## 7. Core Site Engine & Admin Dashboard (`core`)
- **Dynamic Homepage Builder (`HomepageLayout`)**:
  - Database-driven block ordering: Hero Banner, Breaking News Ticker, Trending Grid, State News, Category Rows.
  - Drag-and-drop or order-index management in Admin without code deployments.
- **Site Settings Management**:
  - Global settings model: Logo upload, accent colors, header notice, social links, contact email.
- **Custom Admin Dashboard**:
  - Jazzmin theme integration with analytics cards: Pending editorial approvals, top viewed stories, comment queue statistics.

---

## 8. API & Headless Capability (`api`)
- **RESTful Endpoints (Django REST Framework)**:
  - Read-only public API endpoints for articles, categories, search, and RSS feeds.
  - JWT / Token authentication for PWA / Mobile client support.
