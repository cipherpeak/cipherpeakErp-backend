from django.db import models
from apps.authapp.models import Employee
from django.contrib.postgres.fields import ArrayField

class Task(models.Model):
    TASK_STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('paused', 'Paused'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned'),
        ('on_hold', 'On Hold'),
    ]
    
    TASK_TYPE_CHOICES = [
        ('mechanic', 'Mechanic'),
        ('delivery', 'Delivery'),
        ('office', 'Office'),
        ('service', 'Service/Detailing'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    ICON_TYPE_CHOICES = [
        ('delivery', 'Delivery'),
        ('office', 'Office'),
        ('service', 'Service'),
        ('mechanic', 'Mechanic'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    icon_type = models.CharField(max_length=20, choices=ICON_TYPE_CHOICES, default='nothing') 
    is_maintenance = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.employee:
            return f"{self.employee.employeeId}"
        elif self.is_maintenance:
            return "Maintenance Task"
        else:
            return f"Task #{self.id}"
        
    @property
    def percentage_completed(self):
        if self.status in ['not_started', 'paused']:
            return 0
        elif self.status in ['in_progress', 'on_hold']:
            return 50
        elif self.status in ['completed', 'delivered', 'returned']:
            return 100
        return 0
# ____________________________________________________________
       


class DeliveryTask(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='delivery_details')
    DeliveryId = models.CharField(max_length=255,blank=True, null=True)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_phone = models.CharField(max_length=255, blank=True, null=True)
    delivery_location = models.TextField(blank=True, null=True)
    delivery_notes = models.TextField(blank=True, null=True)
    task_assign_datetime = models.DateTimeField(blank=True, null=True)
    task_start_datetime = models.DateTimeField(blank=True, null=True)
    task_completed_date = models.DateField(blank=True, null=True)
    task_completed_time = models.TimeField(blank=True, null=True)
    status_of_delivery = models.CharField(max_length=255, null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)
    due_time = models.TimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Delivery - {self.customer_name}"


class DeliveryTaskImage(models.Model):
    delivery_task = models.ForeignKey(DeliveryTask, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='task_progress_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Delivery Task {self.delivery_task.id}"


class DeliveryNote(models.Model):
    delivery_task = models.ForeignKey(DeliveryTask, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Delivery Note - {self.delivery_task.customer_name}"      
          
# ____________________________________________________________
    

class PartNumber(models.Model):
    part_number = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.part_number} - {self.item}"


class Mechanic(models.Model):    
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='mechanic_details')
    heading = models.CharField(max_length=255,blank=True, null=True)
    Site_number = models.CharField(max_length=255,blank=True, null=True)
    bay_number = models.CharField(max_length=255, blank=True, null=True)
    Machine_type = models.CharField(max_length=255, blank=True, null=True)
    Machine_serial_number = models.CharField(max_length=255, blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)
    spare_part_details = models.TextField(blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    completion_image = models.ImageField(upload_to='mechanic_task_images/', blank=True, null=True)
    completion_remarks = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Mechanic Task - {self.task.id if self.task else 'No Task'}"


class MechanicPartItem(models.Model):
    """Separate table to store multiple part numbers with quantities for a mechanic task"""
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name='part_items')
    part_number = models.ForeignKey(PartNumber, on_delete=models.CASCADE, related_name='mechanic_items')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['mechanic', 'part_number']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.part_number.part_number} x{self.quantity} for {self.mechanic}"

class MaintenanceTaskAssignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='maintenance_assignments')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='maintenance_tasks_worked')
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.employee.employeeId} - {self.task} ({self.started_at})"        
# ____________________________________________________________
    


class PLU(models.Model):
    plu = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    sub_service = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.plu} - {self.category}"


class ServiceAdvantage(models.Model):

    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='advantage_details')
    detailing_site = models.CharField(max_length=255, blank=True, null=True)
    plu = models.ForeignKey(PLU, on_delete=models.SET_NULL, blank=True, null=True, related_name='service_tasks')
    chassis_number = models.CharField(max_length=255, blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    completion_remarks = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Advantage Task - {self.task.id if self.task else 'No Task'}"    

class ServiceAdvantageImage(models.Model):
    advantage_service = models.ForeignKey(ServiceAdvantage, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='advantage_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Advantage Service {self.advantage_service.id}"

class ServiceAdvantageCompletionImage(models.Model):
    advantage_service = models.ForeignKey(ServiceAdvantage, on_delete=models.CASCADE, related_name='completion_images')
    image = models.ImageField(upload_to='advantage_task_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Completion Image for Advantage Service {self.advantage_service.id}"
# ____________________________________________________________


class ServiceTaskDax(models.Model):

    INVOICE_STATUS_CHOICES = [
        ('invoice_received', 'Invoice Received'),
        ('pr_received', 'PR Received'),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='service_dax_tasks')
    detailing_site = models.CharField(max_length=50, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True, help_text="Additional materials used or other notes")
    chassis_no = models.CharField(max_length=100, blank=True, null=True)
    vehicle_model = models.CharField(max_length=100, blank=True, null=True)
    invoice_status = models.CharField(max_length=20, choices=INVOICE_STATUS_CHOICES, blank=True, null=True)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    completion_remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "DAX Service - " + str(self.task.id if self.task else 'No Task')



class ServiceTaskDaxCompletionImage(models.Model):
    dax_service = models.ForeignKey(ServiceTaskDax, on_delete=models.CASCADE, related_name='completion_images')
    image = models.ImageField(upload_to='dax_completion_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Completion Image for Dax Service {self.dax_service.id}"


class ServiceTaskDaxInvoiceImage(models.Model):
    dax_service = models.ForeignKey(ServiceTaskDax, on_delete=models.CASCADE, related_name='invoice_images')
    image = models.ImageField(upload_to='invoice_pr_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice Image for Dax Service {self.dax_service.id}"


class ServiceDaxTypes(models.Model):
    dax_service = models.ForeignKey(ServiceTaskDax, on_delete=models.CASCADE, related_name='service_dax_types')
    service_type = models.CharField(max_length=50, blank=True, null=True)
    service_sub_type = models.CharField(max_length=20, blank=True, null=True)
    level = models.CharField(max_length=10, blank=True, null=True)
    layers = models.CharField(max_length=10,blank=True,null=True)
    roll_meter = models.CharField(max_length=255, blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "DAX Service Type - " + str(self.dax_service.id if self.dax_service else 'No DAX Service') 
