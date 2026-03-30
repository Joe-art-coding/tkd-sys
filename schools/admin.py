from django.contrib import admin
from .models import School

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'monthly_fee', 'phone', 'is_active']
    list_editable = ['monthly_fee']
    search_fields = ['name', 'code']