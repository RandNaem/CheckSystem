from django.contrib import admin
from .models import Employee, Check, InOut
from import_export.admin import ImportExportModelAdmin

# Register your models here.

class InOutAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('employee', 'check_date', 'checkIn_time', 'checkOut_time',)

admin.site.register(Employee)
admin.site.register(Check)
admin.site.register(InOut, InOutAdmin)
