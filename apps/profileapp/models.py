from django.db import models
from apps.authapp.models import Employee

# Create your models here.
class VisaDetails(models.Model):
    DOCUMENT_TYPES = [
        ('visa_copy', 'Visa Photo Copy'),
        ('labour_card', 'Labour Card Copy'),
        ('passport_copy', 'Passport Copy'),
        ('emirates_id', 'Emirates ID Copy'),
        ('work_permit', 'Work Permit Copy'),
    ]

    employee = models.OneToOneField(
        Employee, 
        on_delete=models.CASCADE, 
        related_name='visa_details'
    )
    
    visa_expiry_date = models.DateField(blank=True, null=True)
    emirates_id_number = models.CharField(max_length=100, blank=True, null=True)
    emirates_id_expiry = models.DateField(blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    

    def __str__(self):
        return f"Visa Details - {self.employee.employeeId}"

    def get_pending_documents(self):
        """Get list of pending documents"""
        pending_docs = []
        document_fields = {
            'visa_copy': 'Visa Photo Copy',
            'labour_card': 'Labour Card Copy', 
            'passport_copy': 'Passport Copy',
            'emirates_id': 'Emirates ID Copy',
            'work_permit': 'Work Permit Copy',
        }
        
        for doc_type, doc_name in document_fields.items():
            if not self.documents.filter(document_type=doc_type).exists():
                pending_docs.append(doc_name)
                
        return pending_docs


class Document(models.Model):
    DOCUMENT_TYPES = [
        ('visa_copy', 'Visa Photo Copy'),
        ('labour_card', 'Labour Card Copy'),
        ('passport_copy', 'Passport Copy'),
        ('emirates_id', 'Emirates ID Copy'),
        ('work_permit', 'Work Permit Copy'),
    ]

    visa_details = models.ForeignKey(
        VisaDetails, 
        on_delete=models.CASCADE, 
        related_name='documents'
    )
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_file = models.FileField(
        upload_to='employee_documents/',
        max_length=255
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.visa_details.employee.employeeId}"
    


class Vehicle(models.Model):

    FUEL_TYPES = [
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('cng', 'CNG'),
    ]
    
    vehicle_number = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=60,null=True,blank=True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPES)
    insurance_expiry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.vehicle_number} - {self.model}"


class VehicleImage(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='vehicles/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Image for {self.vehicle.vehicle_number}"


class VehicleAssignment(models.Model):
    STATUS_CHOICES = [
        ('current_vehicle', 'Current Vehicle'),
        ('temporary_vehicle', 'Temporary Vehicle'),
    ]
    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name='vehicle_assignment'
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        related_name='assignments',
        null=True,
        blank=True
    )
    current_vehicle_assigned_date = models.DateField(null=True, blank=True)  
    current_vehicle_assigned_time = models.TimeField(null=True, blank=True)  
    current_vehicle_ending_date = models.DateField(null=True, blank=True)  
    current_vehicle_ending_time = models.TimeField(null=True, blank=True)  
    temporary_vehicle_number = models.CharField(max_length=50, null=True, blank=True)
    temporary_vehicle_model = models.CharField(max_length=50, null=True, blank=True)
    temporary_vehicle_type = models.CharField(max_length=50, null=True, blank=True)
    temporary_vehicle_fuel_type = models.CharField(max_length=50, null=True, blank=True)
    temporary_vehicle_insurance_expiry_date = models.CharField(max_length=50, null=True, blank=True)

    temporary_vehicle_assigned_date = models.CharField(max_length=100, null=True, blank=True)  
    temporary_vehicle_assigned_time = models.CharField(max_length=100, null=True, blank=True)  
    temporary_vehicle_ending_date = models.CharField(max_length=100, null=True, blank=True)  
    temporary_vehicle_ending_time = models.CharField(max_length=100, null=True, blank=True)  
    
    note = models.TextField(blank=True, null=True, help_text="Additional notes for temporary vehicle assignment")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Location where temporary vehicle is assigned")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='current_vehicle')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.employee.employeeId} - {self.vehicle.vehicle_number if self.vehicle else 'No Vehicle'}"


class TemporaryVehicleImage(models.Model):
    assignment = models.ForeignKey(
        VehicleAssignment,
        on_delete=models.CASCADE,
        related_name='temporary_images'
    )
    image = models.ImageField(upload_to='temporary_vehicles/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.assignment.employee.employeeId}"
    


class TemporaryVehicleHistory(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='temporary_vehicle_history'
    )
    
    # Temporary vehicle details (stored permanently)
    vehicle_number = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=50, null=True, blank=True)
    fuel_type = models.CharField(max_length=50, null=True, blank=True)
    insurance_expiry_date = models.CharField(max_length=50, null=True, blank=True)
    vehicle_image = models.ImageField(upload_to='temporary_vehicles_history/', null=True, blank=True)
        
    # Assignment details
    assigned_date = models.DateField(null=True, blank=True)
    assigned_time = models.TimeField(null=True, blank=True)
    ending_date = models.DateField(null=True, blank=True)
    ending_time = models.TimeField(null=True, blank=True)
    
    # Additional info
    note = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
            ('expired', 'Auto-Expired'),
        ],
        default='completed'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-ending_date', '-ending_time']
        verbose_name_plural = 'Temporary Vehicle Histories'
    
    def __str__(self):
        return f"{self.employee.employeeId} - {self.vehicle_number} ({self.assigned_date} to {self.ending_date})"




class VehicleIssue(models.Model):
    ISSUE_STATUS = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('ignored', 'Ignored'),
    ]
    
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='issues'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,null=True)
    reported_by = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reported_vehicle_issues'
    )
    reported_date = models.DateField()
    status = models.CharField(max_length=20, choices=ISSUE_STATUS, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-reported_date']
    
    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.title}"


class VehicleIssueImage(models.Model):
    issue = models.ForeignKey(
        VehicleIssue,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='vehicle_issue/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.issue.title}"


class DailyOdometerReading(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        related_name='odometer_readings'
    )
    reading_date = models.DateField()
    start_km = models.DecimalField(max_digits=10, decimal_places=2)
    end_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-reading_date']
        unique_together = ['vehicle', 'reading_date']
    
    def __str__(self):
        return f"{self.vehicle.vehicle_number} - {self.reading_date}: {self.start_km}km"
    




class ReportIssue(models.Model):
    date = models.CharField(max_length=255)
    time = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    issue_category = models.CharField(
        max_length=50, 
        blank=True,
        null=True
    )
    custom_issue_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='reported_issues',
        null=True,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Report Issue"
        verbose_name_plural = "Report Issues"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report from {self.date} at {self.location} by {self.employee}"

class ReportIssueMedia(models.Model):
    report = models.ForeignKey(
        ReportIssue,
        on_delete=models.CASCADE,
        related_name='media_files'
    )
    media_file = models.FileField(upload_to='reports/media/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Report Issue Media"
        verbose_name_plural = "Report Issue Media"

    def __str__(self):
        return f"Media for Report {self.report.id}"


