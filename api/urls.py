from django.urls import path
from .views import ArticleListView, ArticleDetailView, CategoryListView, LocationListView

app_name = 'api'

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('locations/', LocationListView.as_view(), name='location_list'),
]
