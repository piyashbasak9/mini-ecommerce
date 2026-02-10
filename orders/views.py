from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer, CreateOrderSerializer
from users.permissions import IsCustomer

class OrderListView(generics.ListAPIView):
    """List user's orders"""
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderCreateView(APIView):
    """Create a new order from cart"""
    permission_classes = [IsCustomer]
    
    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        
        if not cart_items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Collect all products with insufficient stock
        insufficient_stock_items = []
        
        for cart_item in cart_items:
            product = cart_item.product
            quantity = cart_item.quantity
            
            # Check if stock is available
            if not product.is_available(quantity):
                insufficient_stock_items.append({
                    'product_name': product.name,
                    'requested_quantity': quantity,
                    'available_stock': product.stock
                })
        
        # If any product has insufficient stock, return error with details
        if insufficient_stock_items:
            return Response(
                {
                    'error': 'Insufficient stock for some items',
                    'insufficient_items': insufficient_stock_items,
                    'message': 'Please update your cart quantities or remove unavailable items'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate total if all items are available
        total_amount = 0
        order_items_data = []
        
        for cart_item in cart_items:
            product = cart_item.product
            quantity = cart_item.quantity
            
            item_total = product.price * quantity
            total_amount += item_total
            
            order_items_data.append({
                'product': product,
                'quantity': quantity,
                'price': product.price
            })
        
        # Create order
        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            shipping_address=serializer.validated_data.get('shipping_address', ''),
            payment_method=serializer.validated_data.get('payment_method', 'COD')
        )
        
        # Create order items and update stock
        for item_data in order_items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            
            # Reduce product stock
            product.reduce_stock(quantity)
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=item_data['price']
            )
        
        # Clear cart
        cart_items.delete()
        
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

class OrderDetailView(generics.RetrieveAPIView):
    """Retrieve order details"""
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderCancelView(generics.UpdateAPIView):
    """Cancel an order (only if pending)"""
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, status='pending')
    
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        
        # Restock items
        for item in order.items.all():
            item.product.increase_stock(item.quantity)
        
        order.status = 'cancelled'
        order.save()
        
        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_200_OK
        )