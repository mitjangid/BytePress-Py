from rest_framework import generics
from rest_framework.response import Response
from articles.models import Article, ArticleStatus
from taxonomy.models import Category, Location
from .serializers import ArticleListSerializer, ArticleDetailSerializer, CategorySerializer, LocationSerializer

class ArticleListView(generics.ListAPIView):
    serializer_class = ArticleListSerializer

    def get_queryset(self):
        qs = Article.objects.filter(status=ArticleStatus.PUBLISHED).select_related(
            'primary_category', 'location', 'author', 'main_image'
        )
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(primary_category__slug=category_slug)

        location_slug = self.request.query_params.get('location')
        if location_slug:
            qs = qs.filter(location__slug=location_slug)

        if self.request.query_params.get('breaking') == 'true':
            qs = qs.filter(is_breaking=True)

        if self.request.query_params.get('trending') == 'true':
            qs = qs.order_by('-views_count')
        else:
            qs = qs.order_by('-published_at')

        return qs


class ArticleDetailView(generics.RetrieveAPIView):
    queryset = Article.objects.filter(status=ArticleStatus.PUBLISHED)
    serializer_class = ArticleDetailSerializer
    lookup_field = 'slug'


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class LocationListView(generics.ListAPIView):
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
