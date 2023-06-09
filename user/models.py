from django.db import models
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from index.models import Beat, License
import datetime


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True, null=True)
    avatar = models.URLField(default='https://drive.google.com/uc?id=1-1z39lgGE3Cz2oZyyE9a1t7shD1NTgVe')
    is_registered_via_google = models.BooleanField(default=False)
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


class Order(models.Model):
    transaction_id = models.CharField(max_length=20, null=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=False)

    def __str__(self):
        return f"Order: {self.transaction_id}"


class OrderItems(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    license = models.ForeignKey(License, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=False)

    def __str__(self):
        return f'{self.beat}'

    def sum_amount(self):
        self.amount += self.license.price
        self.save()




