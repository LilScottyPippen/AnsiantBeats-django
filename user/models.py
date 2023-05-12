from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from index.models import Beat


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = CustomUserManager()

    def __str__(self):
        return f'Email: {self.email} | Username: {self.username}'


class GoogleCredentials(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    id_token = models.CharField(max_length=255)
    email = models.EmailField(blank=True)

    def __str__(self):
        return f'Email: {self.email}'


class OrderItems(models.Model):
    beat = models.OneToOneField(Beat, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=20)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.beat} | {self.transaction_id}'


STATUS_CHOICES = (
    ("COMPLETED", "Completed"),
    ("IN_PROGRESS", "In Progress"),
)


class Order(models.Model):
    order_item = models.ForeignKey(OrderItems, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return f"Order: {self.order_item.transaction_id}"




