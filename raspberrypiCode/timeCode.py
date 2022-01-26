
import cv2, numpy as np
from skimage.metrics import structural_similarity as compare_ssim

cap = cv2.VideoCapture(0)
tempImg = []
imgs = []

while True:
    status, frame = cap.read()
    if status:
        imgs.append(frame)
        if len(imgs) > 1:
            _imgs = imgs
            _imgs.append(frame)
            
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
