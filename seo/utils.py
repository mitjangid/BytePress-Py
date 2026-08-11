import json
from django.utils.html import mark_safe

def generate_schema_json_ld(article, request=None):
    """
    Generates valid Schema.org NewsArticle + BreadcrumbList JSON-LD payload.
    """
    domain = request.build_absolute_uri('/')[:-1] if request else "https://headlines.example.com"
    article_url = f"{domain}/article/{article.slug}/"
    image_url = f"{domain}{article.main_image.file.url}" if (article.main_image and article.main_image.file) else f"{domain}/static/images/default_news.jpg"

    schema_data = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "NewsArticle",
                "@id": article_url,
                "headline": article.title,
                "description": article.summary,
                "url": article_url,
                "datePublished": article.published_at.isoformat() if article.published_at else article.created_at.isoformat(),
                "dateModified": article.updated_at.isoformat(),
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": article_url
                },
                "image": [image_url],
                "author": {
                    "@type": "Person",
                    "name": article.author.display_name,
                    "url": f"{domain}/author/{article.author.username}/"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "Headlines",
                    "url": domain,
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{domain}/static/images/logo.png"
                    }
                },
                "articleSection": article.primary_category.name
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": domain
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": article.primary_category.name,
                        "item": f"{domain}/category/{article.primary_category.slug}/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": article.title,
                        "item": article_url
                    }
                ]
            }
        ]
    }
    return mark_safe(json.dumps(schema_data, indent=2))
