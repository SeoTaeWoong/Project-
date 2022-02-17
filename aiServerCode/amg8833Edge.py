import cv2

class amg8833():
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            print("__new__\n")
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("__init__\n")
            cls._init = True
    
    
    def createAmg8833Edge(self, fileDictQueue):
        while True:
            if fileDictQueue.qsize() !=0:
                try:
                    fileDict = fileDictQueue.get()
                    img = cv2.imread(fileDict["imgPath"], cv2.IMREAD_GRAYSCALE)
                    amgImg = cv2.imread(fileDict["amgPath"])
    
                    amgImg = cv2.resize(amgImg, (320,240), interpolation=cv2.INTER_AREA) 
    
    
                    hist = cv2.equalizeHist(img)
                    canny = cv2.Canny(hist, 60, 150) # 하단 임계값과 상단 임계값은 실험적으로 결정하기
                    blurimg = cv2.blur(canny, (10,10), anchor=(-1,-1), borderType=cv2.BORDER_DEFAULT)
                    dst = cv2.cvtColor(blurimg, cv2.COLOR_GRAY2RGB)
                    dst2 = cv2.addWeighted(dst, 0.7, amgImg, 1.0, 0)
                    cv2.imwrite(fileDict["amgPath"], dst2)
                except :
                    pass
        