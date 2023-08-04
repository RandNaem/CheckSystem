from django.contrib import admin
from .models import Employee, Check, InOut
from import_export.admin import ImportExportModelAdmin
import os
from django.conf import settings
import pandas as pd
from datetime import datetime
import sqlite3

# Register your models here.
class InOutAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('employee', 'check_date', 'checkIn_time', 'checkOut_time',)
    list_filter = ('employee', 'check_date',)

    def export_action(self, request, *args, **kwargs):
        try:
            # Call the original export_action method to get the exported file
            response = super().export_action(request, *args, **kwargs)
            if response is not None:
                # Get the file name from the response
                content_disposition = response.get('Content-Disposition')
                if content_disposition is not None:
                    file_name = content_disposition.split('=')[1]
                    # Define the folder path where you want to save the file
                    folder_path = os.path.join(settings.BASE_DIR, 'MonthlyReports')
                    # Create the folder if it doesn't exist
                    os.makedirs(folder_path, exist_ok=True)
                    # Remove invalid characters from the file name
                    file_name = self.clean_file_name(file_name)
                    # Create the file path by combining the folder path and file name
                    file_path = os.path.join(folder_path, file_name)
                    # Save the exported file to the specified folder
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    # Call the editfile function to process the exported file
                    self.editfile(file_path)
        except Exception as e:
            # Handle the exception appropriately, such as logging the error
            # and providing a user-friendly error message
            print(f"Export action failed: {e}")

        return response

    def clean_file_name(self, file_name):
        invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
        cleaned_name = file_name
        for char in invalid_chars:
            cleaned_name = cleaned_name.replace(char, '')

        return cleaned_name
    
    def editfile(self, file_path):
        file = pd.read_excel(file_path)
        conn = sqlite3.connect('C:/Users/randn/Desktop/Projects/CheckSystem/system/db.sqlite3')
        cursor = conn.cursor()
        file['Name'] = file['employee'].apply(lambda x: cursor.execute("SELECT employee_name FROM time_tracker_employee WHERE id=?", (x,)).fetchone()[0])
        file['ID'] = file['employee'].apply(lambda x: cursor.execute("SELECT employee_id FROM time_tracker_employee WHERE id=?", (x,)).fetchone()[0])
        cursor.close()
        conn.close()
        file.drop(['id', 'employee'], axis=1, inplace=True)
        total_hours = []
        extra_hours = []
        shortage_hours = []
        for index, row in file.iterrows():
            start_time = datetime.strptime(row['checkIn_time'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(row['checkOut_time'], '%Y-%m-%d %H:%M:%S')
            duration = (end_time - start_time).total_seconds() / 3600
            extra = max((duration - 9, 0))
            shortage = min((duration - 9, 0))
            total_hours.append('{:02d}:{:02d}'.format(int(duration), int((duration * 60) % 60)))
            extra_hours.append('{:02d}:{:02d}'.format(int(extra), int((extra * 60) % 60)))
            shortage_hours.append('{:02d}:{:02d}'.format(int(shortage), int((shortage * 60) % 60)))
        file['Total'] = total_hours
        file['Status'] = file['Total'].apply(lambda hours: 'Complete' if (float(hours.split(':')[0]) + float(hours.split(':')[1])/60) >= 9 else 'Incomplete')
        file['Overtime'] = extra_hours
        file['Undertime'] = shortage_hours
        # Define the new order of columns
        new_column_order = ['ID', 'Name', 'check_date', 'checkIn_time', 'checkOut_time', 'Total', 'Overtime', 'Undertime', 'Status',]
        # Reindex the DataFrame to change the column order
        newf = file.reindex(columns=new_column_order)
        def formaty(r):
            hours_num = r.loc['Total']
            if (float(hours_num.split(':')[0]) + float(hours_num.split(':')[1])/60) >= 9:
                color = '#ccffcc'
            else:
                color = '#ffcccc'
            return ['background-color: {}'.format(color) for i in r]
        styledf = newf.style.apply(formaty, axis=1)
        # Get the current date in the format YYYY-MM-DD
        current_date = datetime.now().strftime('%Y-%m-%d')
        # Define the edited file path
        edited_file_path = os.path.join(os.path.dirname(file_path), 'Monthly_Report_Final_' + current_date + '.xlsx')
        # Save the edited file  
        styledf.to_excel(edited_file_path, index=False)

class CheckAdmin(admin.ModelAdmin):
    list_display = ('employee', 'check_date', 'check_time',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'employee_id', 'company', 'position', 'staff', 'employment_type',)

admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Check, CheckAdmin)
admin.site.register(InOut, InOutAdmin)

