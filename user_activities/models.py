# from django.db import models
# from django.contrib.auth import get_user_model
# import json

# User = get_user_model()

# class UserActivity(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
#     # We'll store email separately for quick and seperated lookups
#     email = models.EmailField()
#     api_called = models.CharField(max_length=255)
#     activity_time = models.DateTimeField(auto_now_add=True)
#     request_payload = models.JSONField(default=dict, blank=True)
    
#     class Meta:
#         ordering = ['-activity_time']
#         verbose_name_plural = 'User Activities'
    
#     def __str__(self):
#         return f"{self.email} - {self.api_called} - {self.activity_time}"

from django.db import models
from custom_auth.models import CustomUser as User

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    email = models.EmailField()
    api_called = models.CharField(max_length=255)
    activity_time = models.DateTimeField(auto_now_add=True)
    request_payload = models.JSONField(default=dict, blank=True)

    # New fields
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device = models.CharField(max_length=255, null=True, blank=True)
    browser = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=50, null=True, blank=True)
    longitude = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-activity_time']
        verbose_name_plural = 'User Activities'

    def __str__(self):
        return f"{self.email} - {self.api_called} - {self.activity_time}"
