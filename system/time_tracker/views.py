from django.shortcuts import render
from django.http import HttpResponse
from .forms import ChecksForm
from .models import Check, Employee
from pyzbar.pyzbar import decode
from PIL import Image
import os
import cv2
import numpy as np

# Create your views here.
def home(request):
    last_check = Check.objects.last()  # Get the last check record
    context = {
        'last_check': last_check, 
     }
    if request.method == 'POST':
        # I should change the camera to be a logitech camera => argument 1
        form = ChecksForm(request.POST)
        vid = cv2.VideoCapture(0)
        while True:
            success, img = vid.read()
            # I should add a condition to allow only one barcode in  one session: done
            # I should add authentication to verify if this QR code has permission to check: done
            for barcode in decode(img):
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                # argument: image, coordinators, close or not, color, thickness
                cv2.polylines(img, [pts], True, (66, 245, 135), 5)
                myData = barcode.data.decode('utf-8')
                # print(myData)
                try:
                    employee = Employee.objects.get(employee_id=myData)
                    # I should fix the time => it is 4 hours behind the actual time of our timezone
                    check = Check(employee=employee)
                    check.save()
                    vid.release()
                    cv2.destroyAllWindows()
                    last_check = Check.objects.last()  # Get the last check record
                    context = {
                        'last_check': last_check,
                    }
                    return render(request, 'time_tracker/success.html', context)
                except:
                    vid.release()
                    cv2.destroyAllWindows()
                    return render(request, 'time_tracker/failure.html', context)
            cv2.imshow('TimeTracker', img)
            key = cv2.waitKey(1)
            # Check if the 'Esc' key (key code 27) is pressed
            if key == 27:
                break
        # I should add the two commands to close all related windows and release resources: done
        # vid.release()
        # cv2.destroyAllWindows()
    return render(request, 'time_tracker/home.html', context)



    # if request.method == 'POST':
    #     form = ChecksForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         qrcode = form.cleaned_data['qr_code']
    #         d = decode(Image.open(qrcode))
    #         text = d[0].data.decode()
    #         form.instance.employee_id = text
    #         form.save()
    #         return HttpResponse(text)
    # else:
    #     form = ChecksForm()
    #     return render(request, 'time_tracker/home.html', {'form': form})
