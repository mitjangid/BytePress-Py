# Headlines News Portal - Detailed Permissions Matrix

## 1. Role Definitions

1. **Super Admin**: Complete unrestricted system access.
2. **Admin**: Full content management, user role management, category/location structure control, moderation override.
3. **Editor**: Full editorial review authority, ability to publish/schedule/archive articles, assign co-authors, and flag breaking news.
4. **Author / Reporter**: Ability to draft and submit articles for review, manage personal bio/profile, upload media for own articles.
5. **Moderator**: Reader comment moderation queue, flagging/unflagging comments.
6. **Subscriber / Reader**: Read content, save bookmarks, submit comments (subject to moderation), subscribe to newsletters.

---

## 2. Model Permissions Mapping Table

| Model | Codename | Super Admin | Admin | Editor | Author | Moderator | Subscriber |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| `User` | `add_user` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `User` | `change_user` | ✅ | ✅ | ❌ | Own profile | ❌ | Own profile |
| `User` | `delete_user` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Category` | `add_category` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Category` | `change_category` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Location` | `add_location` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| `Article` | `add_article` | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `Article` | `change_article` | ✅ | ✅ | ✅ | Own Drafts | ❌ | ❌ |
| `Article` | `publish_article` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| `Article` | `delete_article` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| `MediaAsset` | `add_mediaasset` | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| `Comment` | `add_comment` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `Comment` | `moderate_comment` | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| `HomepageLayout` | `change_homepagelayout` | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| `SiteSetting` | `change_sitesetting` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## 3. Custom Permission Codenames

The following custom permissions are defined in Django models:
- `articles.can_publish_article`: Required to change an article state to `PUBLISHED` or set `scheduled_at`.
- `articles.can_manage_featured`: Required to toggle `is_breaking`, `is_featured`, `is_trending`, and `is_editors_pick`.
- `engagement.can_moderate_comments`: Required to approve, reject, or mark comments as spam.
- `core.can_configure_homepage`: Required to alter `HomepageLayout` display order and active blocks.
