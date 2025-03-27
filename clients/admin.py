from django.contrib import admin
from .models import DocumentType, Client

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'document_type', 'document_number', 'email', 'phone_number')
    list_filter = ('document_type', 'city')
    search_fields = ('first_name', 'last_name', 'document_number', 'email')
