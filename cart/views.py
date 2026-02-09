from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Cart
from .serializers import CartSerializer, CartUpdateSerializer
from users.permissions import IsCustomer

class CartListView(generics.ListCreateAPIView):
    """View and add items to cart"""
    serializer_class = CartSerializer
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)
        
        # Check if item already exists in cart
        cart_item = Cart.objects.filter(
            user=self.request.user,
            product=product
        ).first()
        
        if cart_item:
            # Update quantity if item exists
            cart_item.quantity += quantity
            if product.is_available(cart_item.quantity):
                cart_item.save()
            else:
                raise ValidationError(
                    f'Cannot add {quantity} more items. Only {product.stock - cart_item.quantity + quantity} available.'
                )
        else:
            # Create new cart item
            serializer.save(user=self.request.user)

class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View, update or remove cart item"""
    serializer_class = CartUpdateSerializer
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CartSerializer(instance)
        return Response(serializer.data)

class ClearCartView(generics.DestroyAPIView):
    """Clear entire cart"""
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(
            {'message': 'Cart cleared successfully'},
            status=status.HTTP_200_OK
        )