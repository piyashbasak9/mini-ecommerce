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
        
        # Calculate total and validate stock
        total_amount = 0
        order_items_data = []
        
        for cart_item in cart_items:
            product = cart_item.product
            quantity = cart_item.quantity
            
            if not product.is_available(quantity):
                return Response(
                    {'error': f'Insufficient stock for {product.name}. Available: {product.stock}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            item_total = product.price * quantity
            total_amount += item_total
            
            order_items_data.append({
                'product': product,
                'quantity': quantity,
                'price': product.price
            })
        
        try:
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
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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