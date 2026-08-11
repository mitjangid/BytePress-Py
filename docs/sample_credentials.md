# Headlines News Portal - Demo Account Credentials & Database Connection

This document contains all pre-seeded demo user accounts and live cloud database credentials for local testing and demonstration.

---

## 1. Demo User Accounts (Pre-Seeded in Database)

| Role | Username | Password | Email | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Super Admin** | `admin` | `admin123` | `admin@headlines.example.com` | Full administrative control over users, roles, categories, site settings, and database backups |
| **Managing Editor** | `editor_jane` | `pass123` | `jane.smith@headlines.example.com` | Can approve, publish, schedule, archive articles, assign co-authors, and flag breaking news |
| **Executive Editor** | `editor_marcus` | `pass123` | `marcus.chen@headlines.example.com` | Editorial review authority for Technology & Future Sciences |
| **Tech Reporter** | `author_bob` | `pass123` | `bob.miller@headlines.example.com` | Technology correspondent (Drafts, submits for review, manages own author profile) |
| **Capitol Reporter** | `author_sarah` | `pass123` | `sarah.jenkins@headlines.example.com` | Washington D.C. Bureau Chief covering Capitol Hill and economic policy |
| **Financial Analyst** | `author_david` | `pass123` | `david.ross@headlines.example.com` | Financial Markets Analyst covering global trade and green energy |
| **Foreign Correspondent** | `author_elena` | `pass123` | `elena.rostova@headlines.example.com` | Foreign Correspondent reporting from European and Asian capitals |

---

## 2. Live Cloud Database Connection (Aiven PostgreSQL)

- **Database Engine:** PostgreSQL 16
- **Host:** `pg-3f442cf2-headlines-news.l.aivencloud.com`
- **Port:** `11139`
- **Database Name:** `defaultdb`
- **Username:** `avnadmin`
- **Password:** `<redacted>`
- **SSL Mode:** `require`

### Connection String:
```text
postgres://avnadmin:<redacted>@pg-3f442cf2-headlines-news.l.aivencloud.com:11139/defaultdb?sslmode=require
```

---

## 3. How to Test User Roles Locally

1. Open **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)** in your browser.
2. Log in using `admin` / `admin123` to access full system configuration and user management.
3. Log out and sign in as `editor_jane` / `pass123` to test editorial approval workflows, breaking news toggles, and scheduled publishing.
4. Sign in as `author_bob` / `pass123` to test article drafting and submission for editorial review.
