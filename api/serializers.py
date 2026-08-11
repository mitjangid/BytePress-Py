from rest_framework import serializers
from articles.models import Article, Tag
from taxonomy.models import Category, Location
from accounts.models import User
from media_lib.models import MediaAsset

class UserPublicSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='display_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'avatar', 'bio', 'is_verified_author']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'slug', 'location_type', 'state_code']


class MediaAssetSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = MediaAsset
        fields = ['id', 'title', 'url', 'alt_text', 'caption', 'width', 'height']

    def get_url(self, obj):
        if obj and obj.file:
            return obj.file.url
        return None


class ArticleListSerializer(serializers.ModelSerializer):
    primary_category = CategorySerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    author = UserPublicSerializer(read_only=True)
    main_image = MediaAssetSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'summary', 'primary_category', 'location',
            'main_image', 'published_at', 'is_breaking', 'is_featured',
            'is_trending', 'is_editors_pick', 'author', 'reading_time_minutes', 'views_count'
        ]


class ArticleDetailSerializer(ArticleListSerializer):
    co_authors = UserPublicSerializer(many=True, read_only=True)
    secondary_categories = CategorySerializer(many=True, read_only=True)

    class Meta(ArticleListSerializer.Meta):
        fields = ArticleListSerializer.Meta.fields + ['content', 'co_authors', 'secondary_categories', 'updated_at']
