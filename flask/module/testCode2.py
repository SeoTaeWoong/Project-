import cv2

cam = cv2.VideoCapture(0)
cam.set(3,320)
cam.set(4,240)
ret, frame = cam.read()

frame1 = frame
cv2.rectangle(frame1, (120, 120), (160, 160), (0, 255, 0), 4)
dst = cv2.resize(frame1, dsize=(48, 48), interpolation=cv2.INTER_AREA)
dst1 = cv2.resize(frame, dsize=(48, 48), interpolation=cv2.INTER_AREA)
cv2.rectangle(dst1, (18, 24), (24, 32), (255, 0, 0), 1)

#cv2.imshow("?1",frame1)
cv2.imshow("?",dst)
cv2.imshow("?2",dst1)
cv2.waitKey(0)


