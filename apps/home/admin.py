from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(AttendanceCheck)
admin.site.register(BreakTimer)
admin.site.register(BreakHistory)
admin.site.register(Leave)
admin.site.register(CompanyAnnouncement)
admin.site.register(ExtendBreak)
admin.site.register(LeaveAttachment)
admin.site.register(LeaveSignature)
admin.site.register(LeaveBalance)