from django.db import models
from apps.authapp.models import Employee, Company

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('common', 'Common'),
        ('company', 'Company'),
        ('department', 'Department'),
        ('individual', 'Individual'),
    ]

    recipient = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True, related_name='dashboard_notifications')
    
    # Target fields for group notifications
    target_company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    target_department = models.CharField(max_length=20, choices=Employee.EMPLOYEE_TYPE_CHOICES, null=True, blank=True)
    target_all = models.BooleanField(default=False)  # For common notifications

    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    
    is_read = models.BooleanField(default=False) # Note: For group notifications, this flag might need a separate See/Read model if per-user read status is required.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.notification_type}"
