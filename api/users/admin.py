from django.contrib import admin
from .models import BpUser

@admin.register(BpUser)
class BpUserAdmin(admin.ModelAdmin):
    pass