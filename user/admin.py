from django.contrib import admin
from django.contrib.auth import get_user_model
User = get_user_model()
from listing.extras import delete_realtors_listing_data
from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email')  # Removed 'password' and added missing comma
    list_display_links = ('id', 'first_name', 'last_name', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.save()

    def delete_model(self, request, obj):
        email = obj.email
        obj.delete()
        delete_realtors_listing_data(email)

    def get_queryset(self, request):
        return super().get_queryset(request)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(User, UserAdmin)
admin.site.register(models.UserProfile)