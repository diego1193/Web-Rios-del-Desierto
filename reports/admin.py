from django.contrib import admin
from .models import Purchase

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('client', 'purchase_date', 'amount', 'description')
    list_filter = ('purchase_date', 'client')
    search_fields = ('client__first_name', 'client__last_name', 'client__document_number', 'description')
    date_hierarchy = 'purchase_date'
    readonly_fields = ('created_at',)
