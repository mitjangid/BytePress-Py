from django.contrib import admin
from .models import Redirect, SEOOverride

@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'redirect_type', 'hits_count', 'created_at')
    list_filter = ('redirect_type', 'created_at')
    search_fields = ('old_path', 'new_path')
    readonly_fields = ('hits_count', 'created_at')

@admin.register(SEOOverride)
class SEOOverrideAdmin(admin.ModelAdmin):
    list_display = ('canonical_url', 'og_title', 'schema_type', 'no_index')
