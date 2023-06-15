from django.shortcuts import render
from django.http import HttpResponse
from .forms import ChecksForm
from .models import Checks
from pyzbar.pyzbar import decode
from PIL import Image
import os
import cv2
import numpy as np

# Create your views here.
def home(request):
    if request.method == 'POST':
        # I should change the camera to be a logitech camera => argument 1
        form = ChecksForm(request.POST)
        vid = cv2.VideoCapture(0)
        while True:
            success, img = vid.read()
            # I should add a condition to allow only one barcode in  one session
            # I should add authentication to verify if this QR code has permission to check
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                print(myData)
                # I should fix the time => it is 4 hours behind the actual time of our timezone
                if form.is_valid():
                    form.instance.employee_id = myData
                    form.save()
                pts = np.array([barcode.polygon], np.int32)
                pts = pts.reshape((-1, 1, 2))
                # argument: image, coordinators, close or not, color, thickness
                cv2.polylines(img, [pts], True, (66, 245, 135), 5)
            cv2.imshow('TimeTracker', img)
            key = cv2.waitKey(1)
            # Check if the 'Esc' key (key code 27) is pressed
            if key == 27:
                break
        vid.release()
        cv2.destroyAllWindows()
            # I should add the two commands to close all related windows and release resources
    return render(request, 'time_tracker/home.html')


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
