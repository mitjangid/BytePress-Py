from django.contrib import admin
from .models import HomepageLayout, SiteSetting

@admin.register(HomepageLayout)
class HomepageLayoutAdmin(admin.ModelAdmin):
    list_display = ('display_order', 'title', 'section_type', 'category', 'location', 'item_limit', 'is_active')
    list_display_links = ('title',)
    list_editable = ('display_order', 'is_active', 'item_limit')
    list_filter = ('section_type', 'is_active')
    search_fields = ('title',)

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'primary_color', 'secondary_color')

    def has_add_permission(self, request):
        # Prevent creating multiple instances
        if SiteSetting.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False
