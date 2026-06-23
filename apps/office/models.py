from django.db import models

from apps.authapp.models import Employee



class Note(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('completed', 'Completed')],
        default='pending'
    )
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.employee.employee_name}"


class Meeting(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    agenda = models.TextField(blank=True, null=True)
    
    created_by = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='created_meetings'
    )
    
    attendees = models.ManyToManyField(
        Employee, 
        related_name='meetings'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.title} on {self.date}"