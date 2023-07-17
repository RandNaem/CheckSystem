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
        conn = sqlite3.connect('C:/Users/randn/OneDrive/שולחן העבודה/CheckSystem/system/db.sqlite3')
        cursor = conn.cursor()
        file['name'] = file['employee'].apply(lambda x: cursor.execute("SELECT employee_name FROM time_tracker_employee WHERE id=?", (x,)).fetchone()[0])
        cursor.close()
        conn.close()
        total_hours = []
        for index, row in file.iterrows():
            start_time = datetime.strptime(row['checkIn_time'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(row['checkOut_time'], '%Y-%m-%d %H:%M:%S')
            duration = (end_time - start_time).total_seconds() / 3600
            total_hours.append('{:02d}:{:02d}'.format(int(duration), int((duration * 60) % 60)))
        file['total'] = total_hours
        file['status'] = file['total'].apply(lambda hours: 'Completed' if (float(hours.split(':')[0]) + float(hours.split(':')[1])/60) > 2 else 'Incomplete')
        def formaty(r):
            hours_num = r.loc['total']
            if (float(hours_num.split(':')[0]) + float(hours_num.split(':')[1])/60) >= 9:
                color = '#CBFFA9'
            else:
                color = '#FF9B9B'
            return ['background-color: {}'.format(color) for i in r]
        newf = file.style.apply(formaty, axis=1)
        # Define the edited file path
        edited_file_path = os.path.splitext(file_path)[0] + '_final.xlsx'
        # Save the edited file  
        newf.to_excel(edited_file_path, index=False)



admin.site.register(Employee)
admin.site.register(Check)
admin.site.register(InOut, InOutAdmin)

