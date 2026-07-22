from django.db import models


class Notification(models.Model):
    category = models.CharField(max_length=50)  # system, leave, attendance, approval, announcement, document
    priority = models.CharField(max_length=20, default='normal')  # normal, high, urgent
    title = models.CharField(max_length=255)
    body = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    actor = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-time']

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    publish_date = models.DateField(blank=True, null=True)
    author = models.CharField(max_length=255, default='System')
    audience = models.CharField(max_length=50, default='all')  # all, engineering, sales, hq
    pinned = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='draft')  # draft, published, archived
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        ordering = ['-publish_date', '-id']

    def __str__(self):
        return self.title
