from django.contrib import admin
from .models import Profile, Vendor, Pseudonym

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'user__email', 'bio')

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_id')
    search_fields = ('name', 'client_id')

@admin.register(Pseudonym)
class PseudonymAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor', 'pseudonym')
    search_fields = ('user__username', 'vendor__name', 'pseudonym')
    list_filter = ('vendor',)