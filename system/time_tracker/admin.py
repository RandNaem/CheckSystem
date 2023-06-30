from django.contrib import admin
from .models import Employee, Check, InOut

# Register your models here.

class InOutAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'check_date', 'checkIn_time', 'checkOut_time',)

admin.site.register(Employee)
admin.site.register(Check)
admin.site.register(InOut, InOutAdmin)
