from django.contrib import admin
from .models import Notification, Announcement


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'priority', 'read', 'actor', 'time')
    search_fields = ('title', 'body', 'actor')
    list_filter = ('read', 'category', 'priority')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'audience', 'pinned', 'status', 'publish_date')
    search_fields = ('title', 'body', 'author')
    list_filter = ('status', 'audience', 'pinned')
