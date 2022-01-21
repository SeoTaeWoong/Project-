import cv2 # opencv 사용
import numpy as np

def grayscale(img): # 흑백이미지로 변환
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

def canny(img, low_threshold, high_threshold): # Canny 알고리즘
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size): # 가우시안 필터
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices, color3=(255,255,255), color1=255): # ROI 셋팅

    mask = np.zeros_like(img) # mask = img와 같은 크기의 빈 이미지
    
    if len(img.shape) > 2: # Color 이미지(3채널)라면 :
        color = color3
    else: # 흑백 이미지(1채널)라면 :
        color = color1
        
    # vertices에 정한 점들로 이뤄진 다각형부분(ROI 설정부분)을 color로 채움 
    cv2.fillPoly(mask, vertices, color)
    
    # 이미지와 color로 채워진 ROI를 합침
    ROI_image = cv2.bitwise_and(img, mask)
    return ROI_image

def draw_lines(img, lines, color=[255, 0, 0], thickness=2): # 선 그리기
    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, thickness)

def draw_fit_line(img, lines, color=[255, 0, 0], thickness=2): # 대표선 그리기
        cv2.line(img, (lines[0], lines[1]), (lines[2], lines[3]), color, thickness)

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap): # 허프 변환
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    #line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    #draw_lines(line_img, lines)

    return lines

def weighted_img(img, initial_img, α=1, β=1., λ=0.): # 두 이미지 operlap 하기
    return cv2.addWeighted(initial_img, α, img, β, λ)

def get_fitline(img, f_lines): # 대표선 구하기   
    lines = np.squeeze(f_lines)
    lines = lines.reshape(lines.shape[0]*2,2)
    rows,cols = img.shape[:2]
    output = cv2.fitLine(lines,cv2.DIST_L2,0, 0.01, 0.01)
    vx, vy, x, y = output[0], output[1], output[2], output[3]
    x1, y1 = int(((img.shape[0]-1)-y)/vy*vx + x) , img.shape[0]-1
    x2, y2 = int(((img.shape[0]/2+100)-y)/vy*vx + x) , int(img.shape[0]/2+100)
    
    
    result = [x1,y1,x2,y2]
    return result

def get_point(img, f_lines): # 대표선 구하기   
    lines = np.squeeze(f_lines)
    lines = lines.reshape(lines.shape[0]*2,2)
    rows,cols = img.shape[:2]
    output = cv2.fitLine(lines,cv2.DIST_L2,0, 0.01, 0.01)
    vx, vy, x, y = output[0], output[1], output[2], output[3]
    x1, y1 = int(((img.shape[0]-1)-y)/vy*vx + x) , img.shape[0]-1
    x2, y2 = int(((img.shape[0]/2+20)-y)/vy*vx + x) , int(img.shape[0]/2+20)
    
    
    result = [x1,y1,x2,y2]
    return result, x2


cam = cv2.VideoCapture(0)
cnt = 0
while True:
    ret, frame = cam.read()
    if ret:
        
        if cnt == 0:
            print(frame)
            print("------------------------")
            frame1 = cv2.imread('slope_test.jpg') # 이미지 읽기
            print(frame1)
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            
        height, width = frame.shape[:2] # 이미지 높이, 너비
        gray_img = grayscale(frame) # 흑백이미지로 변환
        blur_img = gaussian_blur(gray_img, 3) # Blur 효과
        canny_img = canny(blur_img, 70, 210) # Canny edge 알고리즘
        vertices = np.array([[(50,height),(width/2-45, height/2+60), (width/2+45, height/2+60), (width-50,height)]], dtype=np.int32)
        ROI_img = region_of_interest(canny_img, vertices) # ROI 설정
        line_arr = hough_lines(ROI_img, 1, 1 * np.pi/180, 30, 10, 20) # 허프 변환
        line_arr = np.squeeze(line_arr)
        
        height1, width1 = frame.shape[:2] # 이미지 높이, 너비
        gray_img1 = grayscale(frame1) # 흑백이미지로 변환
        blur_img1 = gaussian_blur(gray_img1, 3) # Blur 효과
        canny_img1 = canny(blur_img1, 70, 210) # Canny edge 알고리즘
        vertices1 = np.array([[(50,height1),(width1/2-45, height1/2+60), (width1/2+45, height1/2+60), (width1-50,height1)]], dtype=np.int32)
        ROI_img1 = region_of_interest(canny_img1, vertices1) # ROI 설정
        line_arr1 = hough_lines(ROI_img1, 1, 1 * np.pi/180, 30, 10, 20) # 허프 변환
        line_arr1 = np.squeeze(line_arr1)
        
        print(line_arr[:,0])
        print("------------------------------------------------")
        print(line_arr1[:,0])
        
        slope_degree = (np.arctan2(line_arr[:,1] - line_arr[:,3], line_arr[:,0] - line_arr[:,2]) * 180) / np.pi
        break
        
cam.release()
cv2.destroyAllWindows()
        