import time
from django.shortcuts import redirect, render
from django.http import Http404, HttpResponse
from .forms import ChecksForm
from .models import Check, Employee
from pyzbar.pyzbar import decode
from PIL import Image
import os
import cv2
# import numpy as np
from django.http import StreamingHttpResponse

# Create your views here.
def home(request):
    last_check = Check.objects.last()  # Get the last check record
    context = {
        'last_check': last_check, 
     }
    if request.method == 'POST':
        time.sleep(3)
        form = ChecksForm(request.POST)
        vid = cv2.VideoCapture(0)
        while True:
            success, img = vid.read()
            # I should add a condition to allow only one barcode in  one session: done
            # I should add authentication to verify if this QR code has permission to check: done
            for barcode in decode(img):
                # pts = np.array([barcode.polygon], np.int32)
                # pts = pts.reshape((-1, 1, 2))
                # # argument: image, coordinators, close or not, color, thickness
                # cv2.polylines(img, [pts], True, (66, 245, 135), 5)
                myData = barcode.data.decode('utf-8')
                try:
                    employee = Employee.objects.get(employee_id=myData)
                    # I should fix the time => it is 4 hours behind the actual time of our timezone
                    check = Check(employee=employee)
                    check.save()
                    vid.release()
                    cv2.destroyAllWindows()
                    return redirect('success')
                except:
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
        # I should add the two commands to close all related windows and release resources: done
        # vid.release()
        # cv2.destroyAllWindows()
    return render(request, 'time_tracker/home.html', context)

def success(request):
    last_check = Check.objects.last()  # Get the last check record
    context = {
        'last_check': last_check,
    }
    return render(request, "time_tracker/success.html", context)


def failure(request):
    last_check = Check.objects.last()  # Get the last check record
    context = {
        'last_check': last_check,
    }
    return render(request, "time_tracker/failure.html", context)

# version2
# camera = cv2.VideoCapture(0)
# def gen_frames():
#     while True:
#         success, frame = camera.read()  # Read the camera frame
#         if not success:
#             break
#         else:
#             ret, encoded_frame = cv2.imencode('.jpg', frame)
#             decoded_frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)  # Convert the encoded frame back to an image
#             for barcode in decode(decoded_frame):
#                 pts = np.array([barcode.polygon], np.int32)
#                 pts = pts.reshape((-1, 1, 2))
#                 cv2.polylines(decoded_frame, [pts], True, (66, 245, 135), 5)
#                 myData = barcode.data.decode('utf-8')
#                 print(myData)
#             ret, modified_frame = cv2.imencode('.jpg', decoded_frame)  # Encode the modified frame back to bytes
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + modified_frame.tobytes() + b'\r\n')  # Concatenate the modified frame and show the result

# def video_feed(request):
#     # Set the content type header
#     response = StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
#     return response

# def index(request):
#     return render(request, 'time_tracker/index.html')


# version3
# camera = cv2.VideoCapture(0)
# from django.http import HttpResponse
# def video_feed(request):
#     def gen_frames():
#         while True:
#             success, frame = camera.read()  # Read the camera frame
#             if not success:
#                 break

#             ret, encoded_frame = cv2.imencode('.jpg', frame)
#             decoded_frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)  # Convert the encoded frame back to an image

#             barcodes = decode(decoded_frame)  # Decode barcodes in the frame
#             for barcode in barcodes:
#                 pts = np.array([barcode.polygon], np.int32)
#                 pts = pts.reshape((-1, 1, 2))
#                 cv2.polylines(decoded_frame, [pts], True, (66, 245, 135), 5)
#                 myData = barcode.data.decode('utf-8')
#                 print(myData)
#                 try:
#                     employee = Employee.objects.get(employee_id=myData)
#                     check = Check(employee=employee)
#                     check.save()
#                     last_check = Check.objects.last()  # Get the last check record
#                     context = {
#                         'last_check': last_check,
#                     }
#                     camera.release()
#                     cv2.destroyAllWindows()
#                     return False
#                 except Employee.DoesNotExist:
#                     pass

#             ret, modified_frame = cv2.imencode('.jpg', decoded_frame)  # Encode the modified frame back to bytes
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + modified_frame.tobytes() + b'\r\n')  # Yield the modified frame
    
#     if not gen_frames():
#         return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
#     return HttpResponse('yes')

