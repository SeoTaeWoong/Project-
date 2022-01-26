import cv2

camera = cv2.VideoCapture(0)

a= 1

while True:
    success, frame = camera.read()  # read the camera frame
    if not success:
        break
    else:
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        if(a == 1):
            print(buffer)
            a+=1