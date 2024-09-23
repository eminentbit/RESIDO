from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()
from listing.extras import delete_realtors_listing_data
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', )
    list_display_links = ('id', 'name', 'email', )
    search_fields = ('name', 'email', )
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.save()  # Removed 'using'

    def delete_model(self, request, obj):
        email = obj.email
        obj.delete()  # Removed 'using'
        delete_realtors_listing_data(email)

    def get_queryset(self, request):
        return super().get_queryset(request)  # Removed 'using'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)  # Removed 'using'

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, **kwargs)  # Removed 'using'

admin.site.register(User, UserAdmin)
