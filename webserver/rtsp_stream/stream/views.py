import cv2
from django.http import StreamingHttpResponse
from django.shortcuts import render

# RTSP URL
RTSP_URL = "rtsp://admin:L26B425B@10.90.76.101:554/cam/realmonitor?channel=1&subtype=0&proto=Onvif"

def generate_frames():
    cap = cv2.VideoCapture(RTSP_URL)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Encode the frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in byte format
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

def video_feed(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')

def index(request):
    return render(request, 'stream/index.html')
