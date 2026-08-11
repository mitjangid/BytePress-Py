from .models import SiteSetting
from taxonomy.models import Category, Location
from taxonomy.services import detect_user_location
from articles.models import Article, ArticleStatus

def site_settings_processor(request):
    """
    Injects site_settings, active categories, breaking news ticker stories,
    and user location context across all templates.
    """
    site_settings = SiteSetting.load()
    nav_categories = Category.objects.filter(is_active=True, parent__isnull=True).prefetch_related('children')
    locations = Location.objects.filter(is_active=True, parent__isnull=True).prefetch_related('children')
    
    breaking_news = Article.objects.filter(
        status=ArticleStatus.PUBLISHED,
        is_breaking=True
    ).order_by('-published_at')[:5]

    current_location = detect_user_location(request)

    return {
        'site_settings': site_settings,
        'nav_categories': nav_categories,
        'nav_locations': locations,
        'breaking_news_ticker': breaking_news,
        'current_location': current_location,
    }
