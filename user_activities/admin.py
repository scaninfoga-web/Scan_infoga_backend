from django.contrib import admin
from .models import UserActivity

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('email', 'api_called', 'activity_time')
    list_filter = ('api_called', 'activity_time')
    search_fields = ('email', 'api_called')
    readonly_fields = ('activity_time',)