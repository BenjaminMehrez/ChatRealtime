from django.contrib import admin
from .models import LandingPage


# Register your models here.

class LandingPageAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_enabled', 'access_code')

admin.site.register(LandingPage, LandingPageAdmin)
