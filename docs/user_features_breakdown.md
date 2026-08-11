# Headlines News Portal - Role-by-Role Feature Breakdown

This document presents a complete, user-by-user (role-by-role) feature breakdown specifying every capability, permission, and workflow step built into Headlines.

---

## 1. Super Admin Features (`SUPER_ADMIN`)

### System Governance & Administration
- **User & Role Assignment:** Create, modify, suspend, or promote users to any of the 6 roles (`Super Admin`, `Admin`, `Editor`, `Author`, `Moderator`, `Subscriber`).
- **Singleton Site Settings Management:**
  - Dynamic Site Name, Custom Logo upload, Favicon upload.
  - Brand theme colors (`Primary` & `Secondary` accent colors).
  - Footer copyright text and contact email address.
  - Social media URL channels (Twitter/X, Facebook, Instagram, YouTube).
- **Homepage Layout Builder (`HomepageLayout`):**
  - Rearrange homepage content blocks (`Hero Banner`, `Breaking Ticker`, `Category Rows`, `State News`, `Trending Grid`, `Editor Picks`).
  - Set display order, active/inactive state, item counts, and category/location filters per block.
- **301 Permanent Redirect Manager:** Create, track, and monitor permanent HTTP 301 redirects to preserve SEO juice when URLs change.
- **Full Database & Storage Access:** Execute management commands (`seed_data`, `migrate`), database dumps, and media asset storage configurations.

---

## 2. Admin Features (`ADMIN`)

### Content Structure & Moderation Governance
- **Hierarchical Category Tree Management (`django-mptt`):**
  - Create parent and subcategories (e.g. `World` -> `Europe`).
  - Drag-and-drop tree reordering in Django Admin using `DraggableMPTTAdmin`.
  - Assign category display order, icons, and bilingual Hindi names (`name_hi`).
  - Configure per-category SEO Meta Titles and Descriptions.
- **Geographical Location Management:**
  - Two-tier geographical classification (`State / Region` and `City`).
  - Set state codes (e.g., `CA`, `NY`, `TX`, `DC`), coordinates (`latitude`, `longitude`), and Hindi names (`name_hi`).
- **Staff User Supervision:** Review staff profiles, verify author badges (`is_verified_author`), and manage author bio cards.
- **Editorial Overrides:** Override any article status or moderation state across all newsroom authors.

---

## 3. Editor Features (`EDITOR`)

### Editorial Approval & Publishing Workflow
- **Workflow State Machine:**
  - Transition article states: `Draft` -> `Pending Review` -> `Published` -> `Archived`.
  - Record audit log entries in `ArticleStateLog` with reviewer notes.
- **Scheduled Timed Publishing:** Set `scheduled_at` timestamps for automatic publishing via background `Celery Beat` tasks.
- **Content Flags Management:**
  - Toggle `is_breaking` (powers breaking news ticker).
  - Toggle `is_featured` (hero grid prominence).
  - Toggle `is_trending` and `is_editors_pick`.
- **Co-Author & Contributor Assignment:** Attach primary authors and unlimited co-authors to stories.
- **Revision Snapshot Rollback:** View `ArticleRevision` version history for any article and inspect historical text diffs.
- **Bulk Admin Actions:**
  - Bulk publish articles in one click.
  - Bulk submit for editorial review.
  - Bulk archive or toggle breaking news flags.

---

## 4. Author & Reporter Features (`AUTHOR`)

### Story Creation & Personal Analytics
- **Rich Text Content Editor:**
  - Format articles with headings, blockquotes, lists, and inline media embeds.
  - Bilingual fields support: `title_hi`, `summary_hi`, `content_hi` for Hindi / regional reporting.
- **Story Submission:** Save article as `Draft` or submit to editors for `Pending Review`.
- **Media Asset Library Upload:**
  - Upload high-resolution photos with automatic Pillow `.webp` conversion and compression.
  - Required `alt_text` input (validated before story can be published).
- **Personal Profile Management:**
  - Edit bio, profile avatar, Twitter handle, Facebook URL, and personal portfolio website.
- **Story Metrics:** View real-time article view counters (`views_count`) and estimated reading time (`reading_time_minutes`).

---

## 5. Moderator Features (`MODERATOR`)

### Reader Discussion & Spam Prevention
- **Comment Moderation Queue:**
  - Moderate reader comments across states: `Pending Moderation`, `Approved`, `Flagged Spam`, `Rejected`.
- **Anti-Spam Heuristic Inspection:**
  - Review automated spam flags (triggered by excessive external links or suspicious guest submissions).
- **Bulk Moderation Actions:**
  - Bulk approve valid comments or bulk flag spam comments in Django Admin.

---

## 6. Subscriber & Reader Features (`SUBSCRIBER`)

### Interactivity & Personalization
- **Multilingual Language Switcher:** Switch between English, Hindi (`hi`), Marathi (`mr`), Bengali (`bn`), Tamil (`ta`), and Telugu (`te`).
- **HTMX Threaded Comments:** Post comments and reply to nested comment threads live without page refreshes.
- **HTMX Bookmarking:** Save articles to a personal reading list (`Bookmark`).
- **Newsletter Subscription:** Double opt-in newsletter registration for daily digest emails.
- **Dark / Light Mode Toggle:** Smooth Alpine.js theme toggle with local storage persistence.

---

## 7. Guest & Unauthenticated Visitor Features

### News Consumption & Search
- **Responsive Newspaper Layout:** High-density responsive homepage with Breaking News ticker, Hero grid, Trending sidebar, and Category rows.
- **State-Wise Local News Auto-Detection:** Auto-detect client location via `django-ipware` and GeoIP to prioritize local news.
- **Full-Text Search:** Search articles with keyword queries, category filters, and location tags.
- **SEO & Social Sharing:**
  - Valid Schema.org `NewsArticle` & `BreadcrumbList` JSON-LD tags on every story.
  - OpenGraph & Twitter Card previews.
  - RSS Feeds per category and state/city.
  - Installable PWA support (`manifest.json` + `sw.js`).
