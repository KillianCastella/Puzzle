import cv2
import numpy as np
	
def readAndShowRGBImage():
    imgRGB = cv2.imread("img/1.png",cv2.IMREAD_UNCHANGED)
    if imgRGB is None:
        print("erreur ouverture fichier")
        return 0
    imgray = cv2.cvtColor(imgRGB,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(contours)
    cv2.drawContours(imgRGB, contours, -1, (0,0,255), 3)
    cv2.imshow("Piece2", imgRGB)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    readAndShowRGBImage()


