# Headlines News Portal - API Documentation

## Overview

The Headlines REST API provides read-only JSON endpoints for mobile apps, progressive web applications (PWA), and third-party syndication.

Base URL: `/api/v1/`

---

## Endpoints Summary

| Endpoint | Method | Description | Query Parameters |
| :--- | :--- | :--- | :--- |
| `/api/v1/articles/` | `GET` | List published articles | `category`, `location`, `tag`, `page`, `page_size` |
| `/api/v1/articles/<slug>/` | `GET` | Get single article details | None |
| `/api/v1/articles/breaking/` | `GET` | Get breaking news articles | `limit` |
| `/api/v1/articles/trending/` | `GET` | Get trending news articles | `limit` |
| `/api/v1/categories/` | `GET` | List hierarchical categories | `parent` |
| `/api/v1/locations/` | `GET` | List states and cities | `type` (`STATE` or `CITY`) |
| `/api/v1/search/` | `GET` | Full-text search articles | `q`, `category`, `location`, `from_date`, `to_date` |
| `/api/v1/homepage/` | `GET` | Get dynamic homepage blocks configuration & articles | None |

---

## Sample Request & Response

### `GET /api/v1/articles/breaking/`
**Response (200 OK)**:
```json
{
  "count": 2,
  "results": [
    {
      "id": 102,
      "title": "Major Policy Announcement Released Today",
      "slug": "major-policy-announcement-released-today",
      "summary": "Officials have confirmed the implementation of new national guidelines.",
      "published_at": "2026-08-11T10:30:00Z",
      "primary_category": {
        "id": 4,
        "name": "Politics",
        "slug": "politics"
      },
      "author": {
        "id": 12,
        "name": "Jane Doe",
        "avatar": "/media/avatars/jane_doe.webp"
      },
      "main_image": {
        "url": "/media/assets/2026/08/policy_announcement.webp",
        "alt_text": "Press conference stage with flags"
      },
      "is_breaking": true,
      "reading_time_minutes": 3
    }
  ]
}
```

---

## Authentication & Rate Limiting

- **Public Endpoints**: Read-only endpoints do not require authentication headers.
- **Rate Limiting**: Public API endpoints are throttled to 100 requests per minute per IP address. Rate limit status headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`) are returned with every response.
