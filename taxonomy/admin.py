from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Category, Location

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'slug', 'is_active', 'display_order', 'created_at')
    list_display_links = ('indented_title',)
    list_editable = ('is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'parent', 'icon', 'description')}),
        ('Display & Visibility', {'fields': ('is_active', 'display_order')}),
        ('SEO Overrides', {'fields': ('meta_title', 'meta_description')}),
    )

@admin.register(Location)
class LocationAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title', 'slug', 'location_type', 'state_code', 'is_active')
    list_display_links = ('indented_title',)
    list_editable = ('is_active',)
    list_filter = ('location_type', 'is_active')
    search_fields = ('name', 'slug', 'state_code')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'location_type', 'parent', 'state_code')}),
        ('Coordinates', {'fields': ('latitude', 'longitude')}),
        ('Visibility', {'fields': ('is_active',)}),
    )
