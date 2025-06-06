from django.db import models
from django.contrib.auth import get_user_model
import json

User = get_user_model()

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    # We'll store email separately for quick and seperated lookups
    email = models.EmailField()
    api_called = models.CharField(max_length=255)
    activity_time = models.DateTimeField(auto_now_add=True)
    request_payload = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-activity_time']
        verbose_name_plural = 'User Activities'
    
    def __str__(self):
        return f"{self.email} - {self.api_called} - {self.activity_time}"