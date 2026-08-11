# Headlines News Portal - User URLs & Login Credentials Guide

This guide provides a comprehensive catalog of all access URLs, portals, login details, and accessible routes for every user role in the Headlines CMS ecosystem.

---

## 1. Global Portal Access Points

- **Reader Front-End Portal:** [http://127.0.0.1:8080/](http://127.0.0.1:8080/)
- **CMS Admin & Editorial Login:** [http://127.0.0.1:8080/admin/login/](http://127.0.0.1:8080/admin/login/)
- **Language Switcher Endpoint:** [http://127.0.0.1:8080/i18n/setlang/](http://127.0.0.1:8080/i18n/setlang/)
- **REST API Base URL:** [http://127.0.0.1:8080/api/v1/](http://127.0.0.1:8080/api/v1/)
- **XML Sitemap:** [http://127.0.0.1:8080/sitemap.xml](http://127.0.0.1:8080/sitemap.xml)
- **Robots.txt:** [http://127.0.0.1:8080/robots.txt](http://127.0.0.1:8080/robots.txt)

---

## 2. Role-by-Role Credentials & Accessible URLs

### 👑 1. Super Admin & Admin Users
- **Login URL:** [http://127.0.0.1:8080/admin/login/](http://127.0.0.1:8080/admin/login/)
- **Credentials:**
  - **Username:** `admin`
  - **Password:** `admin123`
  - **Email:** `admin@headlines.example.com`
- **Accessible URLs & Management Dashboards:**
  - Full Admin Dashboard: `/admin/`
  - User & Role Management: `/admin/accounts/user/`
  - Category Tree Management: `/admin/taxonomy/category/`
  - Location Hierarchy (State/City): `/admin/taxonomy/location/`
  - Site Settings (Logo, Colors, Socials): `/admin/core/sitesetting/`
  - Homepage Dynamic Layout Builder: `/admin/core/homepagelayout/`
  - 301 Redirects Manager: `/admin/seo/redirect/`
  - Database Backups / System Check: `/admin/`

---

### 📝 2. Editors (Managing & Executive Editors)
- **Login URL:** [http://127.0.0.1:8080/admin/login/](http://127.0.0.1:8080/admin/login/)
- **Credentials:**
  - **Username:** `editor_jane` | **Password:** `pass123`
  - **Username:** `editor_marcus` | **Password:** `pass123`
- **Accessible URLs & Management Dashboards:**
  - Article Editorial Queue: `/admin/articles/article/`
  - Pending Review Filter: `/admin/articles/article/?status__exact=PENDING_REVIEW`
  - Published Articles: `/admin/articles/article/?status__exact=PUBLISHED`
  - Media Library Uploads: `/admin/media_lib/mediaasset/`
  - Article Revisions & Rollbacks: `/admin/articles/articlerevision/`
  - State Transition Logs: `/admin/articles/articlestatelog/`
  - Comment Moderation Queue: `/admin/engagement/comment/`

---

### ✍️ 3. Authors & Journalists
- **Login URL:** [http://127.0.0.1:8080/admin/login/](http://127.0.0.1:8080/admin/login/)
- **Credentials:**
  - **Username:** `author_bob` | **Password:** `pass123` (Tech Reporter)
  - **Username:** `author_sarah` | **Password:** `pass123` (Capitol Reporter)
  - **Username:** `author_david` | **Password:** `pass123` (Financial Analyst)
  - **Username:** `author_elena` | **Password:** `pass123` (Foreign Correspondent)
- **Accessible URLs & Management Dashboards:**
  - Article Drafting & Submission: `/admin/articles/article/add/`
  - Own Draft Stories: `/admin/articles/article/`
  - Media Asset Upload: `/admin/media_lib/mediaasset/add/`
  - Public Author Profile Page: `/author/<username>/` (e.g. `/author/author_bob/`)

---

### 🛡️ 4. Moderators
- **Login URL:** [http://127.0.0.1:8080/admin/login/](http://127.0.0.1:8080/admin/login/)
- **Credentials:**
  - **Username:** `moderator_user` | **Password:** `pass123`
- **Accessible URLs & Management Dashboards:**
  - Comment Moderation Queue: `/admin/engagement/comment/`
  - Pending Moderation Comments: `/admin/engagement/comment/?status__exact=PENDING`
  - Flagged Spam Queue: `/admin/engagement/comment/?status__exact=FLAGGED`

---

### 🙋‍♂️ 5. Subscribers & Readers (Authenticated)
- **Login URL:** [http://127.0.0.1:8080/admin/login/](http://127.0.0.1:8080/admin/login/)
- **Accessible Front-End URLs:**
  - Homepage & Breaking Ticker: `/`
  - Interactive Article View: `/article/<slug>/`
  - Saved Bookmarks List: `/bookmark/toggle/<slug>/`
  - Multilingual Language Switcher: `/i18n/setlang/`
  - Live Comment Posting: `/comment/post/<slug>/`

---

### 🌐 6. Guests & Unauthenticated Visitors
- **Accessible Public URLs:**
  - Homepage: `/`
  - Category Landing Pages: `/category/technology/`, `/category/politics/`, `/category/world/`
  - State & City News Pages: `/location/california/`, `/location/san-francisco/`
  - Full-Text Search: `/search/?q=<query>`
  - REST API Endpoints: `/api/v1/articles/`, `/api/v1/categories/`, `/api/v1/locations/`
