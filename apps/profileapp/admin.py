from django.contrib import admin
from .models import (
    Document, ReportIssue, VisaDetails, Vehicle, VehicleAssignment, 
    VehicleIssue, DailyOdometerReading, TemporaryVehicleHistory, 
    TemporaryVehicleImage, ReportIssueMedia, VehicleImage, VehicleIssueImage
)

# Register your models here.
admin.site.register(VisaDetails)
admin.site.register(Document)
admin.site.register(Vehicle)
admin.site.register(VehicleAssignment)
admin.site.register(DailyOdometerReading)
admin.site.register(TemporaryVehicleHistory)
admin.site.register(ReportIssue)
admin.site.register(TemporaryVehicleImage)
admin.site.register(ReportIssueMedia)
admin.site.register(VehicleImage)
admin.site.register(VehicleIssue)
admin.site.register(VehicleIssueImage)



