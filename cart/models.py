from django.db import models
from users.models import User
from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f'{self.user.email} - {self.product.name}'
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    def save(self, *args, **kwargs):
        # Check stock availability before adding to cart
        if not self.product.is_available(self.quantity):
            raise ValueError(f'Only {self.product.stock} items available in stock')
        super().save(*args, **kwargs)