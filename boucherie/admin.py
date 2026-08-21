from django.contrib import admin
from .models import Avis, Contact


@admin.register(Avis)
class AvisAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'rating', 'created_at', 'is_approved')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('name', 'email', 'message')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject','message', 'created_at', 'is_treated')
    list_filter = ('subject', 'is_treated', 'created_at')
    search_fields = ('name', 'email', 'phone', 'company', 'message')
    list_editable = ('is_treated',)