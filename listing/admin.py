from django.contrib import admin
from .models import Listing


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'realtor', 'title', 'slug', )
    list_display_links = ('id', 'realtor', 'title', 'slug', )
    list_filter = ('realtor', )
    search_fields = ('title', 'description', )
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.save()  # Removed 'using'

    def delete_model(self, request, obj):
        obj.delete()  # Removed 'using'

    def get_queryset(self, request):
        return super().get_queryset(request)  # Removed 'using'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)  # Removed 'using'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, **kwargs)  # Removed 'using'

admin.site.register(Listing, ListingAdmin)