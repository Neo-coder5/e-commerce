
from django.db import models
from .product import Product
from django.core.validators import RegexValidator

from django.contrib.auth import get_user_model

User = get_user_model()

phone_regex = RegexValidator(
    regex=r'^\+998\d{9}',
    message="Phone number must be entered in the format: '+998xxxxxxxxx'."

)

class Order(models.Model):
    PENDING = 'Pending'
    PROCESSING = 'Processing'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELLED = 'Canceled'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delived'),
        (CANCELLED, 'Canceled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,

    )
    phone_number = models.CharField(validators=[phone_regex], max_length=13, blank=True, null=True)

    def set_status(self, new_status):
        if new_status not in dict(self.STATUS_CHOICES):
            raise ValueError("Invalid status")
        self.status = new_status
        self.save()

    def is_transition_allowed(self, new_status):
        allowed_transitions = {
            self.PENDING: [self.PROCESSING, self.CANCELLED],
            self.PROCESSING: [self.SHIPPED, self.CANCELLED],
            self.SHIPPED: [self.DELIVERED, self.CANCELLED],
        }

        return new_status in allowed_transitions.get(new_status, [])

    def __str__(self):
        return f"Order({self.product.name} by {self.customer.username})"