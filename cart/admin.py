from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity', 'total_price', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__email', 'product__name']
    readonly_fields = ['created_at', 'updated_at']