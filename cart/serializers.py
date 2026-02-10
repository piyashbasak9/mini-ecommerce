from rest_framework import serializers
from .models import Cart
from products.serializers import ProductSerializer

    
class CartSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_detail', 'quantity', 'total_price', 'created_at']
        read_only_fields = ['created_at']
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value
    
    def validate(self, data):
        return data


class CartUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['quantity']