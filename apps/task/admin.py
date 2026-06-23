# task/admin.py
from django.contrib import admin
from .models import Task, DeliveryTask,Mechanic,ServiceAdvantage,ServiceTaskDax,ServiceDaxTypes,MaintenanceTaskAssignment,PLU, PartNumber,ServiceTaskDaxInvoiceImage,ServiceTaskDaxCompletionImage,ServiceAdvantageImage,ServiceAdvantageCompletionImage,DeliveryTaskImage,MechanicPartItem,DeliveryNote


admin.site.register(Task)
admin.site.register(DeliveryTask)
admin.site.register(Mechanic) 
admin.site.register(ServiceAdvantage) 
admin.site.register(ServiceTaskDax)
admin.site.register(ServiceDaxTypes)
admin.site.register(PLU)
admin.site.register(MaintenanceTaskAssignment)
admin.site.register(PartNumber)
admin.site.register(ServiceTaskDaxInvoiceImage)
admin.site.register(ServiceTaskDaxCompletionImage)
admin.site.register(ServiceAdvantageImage)
admin.site.register(ServiceAdvantageCompletionImage)
admin.site.register(DeliveryTaskImage)
admin.site.register(MechanicPartItem)
admin.site.register(DeliveryNote)


