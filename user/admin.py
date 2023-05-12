from django.contrib import admin
from .models import CustomUser, GoogleCredentials, Order, OrderItems


admin.site.register(CustomUser)
admin.site.register(GoogleCredentials)
admin.site.register(Order)
admin.site.register(OrderItems)