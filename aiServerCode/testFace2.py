import cv2
import cvlib as cv
from tensorflow.keras.models import load_model
cap = cv2.VideoCapture(0)
i = 1260;
cnt = 0

model = load_model("mnist_member_model.h5")

while True:
    try:
        ret, frame = cap.read() 
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 얼굴 찾기
            faces, confidences = cv.detect_face(frame)
            for (x, y, x2, y2), conf in zip(faces, confidences):
                '''dst = frame[y-20:y2+20,x-20:x2+20].copy()
                if cnt%3 == 0:
                    cv2.imwrite('./JangYungDae/JangYungDae'+str(i)+'.jpg',dst)
                    i+=1
                cnt+=1'''


            		# 얼굴위치 bbox 그리기
                cv2.rectangle(frame, (x-20, y-20), (x2+20, y2+20), (0, 255, 0), 2)
                
            		# 확률 출력하기
                cv2.putText(frame, str(conf), (x,y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
                print(x,x2,"   /   ", y,y2)
                
            # 영상 출력
            
            cv2.imshow('result',frame)
                
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except:
        pass

cap.release()
cv2.destroyAllWindows()        