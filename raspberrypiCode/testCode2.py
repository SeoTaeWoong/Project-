
import cv2, numpy as np
import cvlib as cv
from skimage.metrics import structural_similarity as compare_ssim
cap = cv2.VideoCapture(0)
tempImg = []
imgs = []
cnt= 0
while True:
    status, frame = cap.read()
    
    if status:
        faces, confidences = cv.detect_face(frame)
        
        for (x, y, x2, y2), conf in zip(faces, confidences):
            
            img_size = (128,128)
            img = frame[y-20:y2+20,x-20:x2+20].copy()
            frame_resized = cv2.resize(img, img_size, interpolation=cv2.INTER_AREA) 

            imgs.append(frame_resized)
            if len(imgs) > 1:
                
                grays = []
                for i, img in enumerate(imgs) :
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    grays.append(gray)
                
                
                (score, diff) = compare_ssim(grays[0], grays[1], full=True)
                diff = (diff * 255).astype("uint8")
    
                if score < 0.65:
                    print(f"Similarity: {score:.5f}")
                    del(imgs[0])
                else:
                    del(imgs[1])
                    
                cv2.rectangle(frame, (x-20, y-20), (x2+20, y2+20), (0, 255, 0), 2)
                    
            
        
                
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
