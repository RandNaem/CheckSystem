import time
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from .forms import ChecksForm
from .models import Check, Employee
from pyzbar.pyzbar import decode
from PIL import Image
import os
import cv2
from django.http import StreamingHttpResponse

# Create your views here.
def home(request):
    # last check record
    last_check = Check.objects.last()
    context = {
        'last_check': last_check, 
     }
    if request.method == 'POST':
        form = ChecksForm(request.POST)
        vid = cv2.VideoCapture(0)
        # for external camera 
        # vid = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        while True:
            success, img = vid.read()
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                # authentication to verify if this QR code has permission to check
                try:
                    employee = Employee.objects.get(employee_id=myData)
                    check = Check(employee=employee)
                    check.save()
                    # allow only one barcode in  one session & close all related windows and release resources
                    vid.release()
                    cv2.destroyAllWindows()
                    return redirect('success')
                except:
                    # allow only one barcode in  one session & close all related windows and release resources
                    vid.release()
                    cv2.destroyAllWindows()
                    return redirect('failure')
            # Create a named window, set properties, and move it to the desired position
            cv2.namedWindow('TimeTracker', cv2.WINDOW_NORMAL | cv2.WINDOW_FULLSCREEN)
            cv2.setWindowProperty('TimeTracker', cv2.WND_PROP_TOPMOST, 1)
            cv2.moveWindow('TimeTracker', 400, 200)

            # Disable window closing and set default size
            cv2.setWindowProperty('TimeTracker', cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_NORMAL)
            cv2.imshow('TimeTracker', img)
            key = cv2.waitKey(1)
            # Check if the 'Esc' key (key code 27) is pressed
            if key == 27:
                break
    return render(request, 'time_tracker/home.html', context)

def success(request):
    # last check record
    last_check = Check.objects.last()
    context = {
        'last_check': last_check,
    }
    return render(request, "time_tracker/success.html", context)

def failure(request):
    # last check record
    last_check = Check.objects.last()
    context = {
        'last_check': last_check,
    }
    return render(request, "time_tracker/failure.html", context)