from django.contrib import admin
from .models import CustomUser, GoogleCredentials


admin.site.register(CustomUser)
admin.site.register(GoogleCredentials)
