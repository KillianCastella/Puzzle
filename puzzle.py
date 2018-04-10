import cv2
import numpy as np
	
def readAndShowRGBImage():
	#detection des contours
    imgRGB = cv2.imread("img/9.png",cv2.IMREAD_UNCHANGED)
    channels = cv2.split(imgRGB)
    imgray = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
    if imgRGB is None:
        print("erreur ouverture fichier")
        return 0
    ret, thresh = cv2.threshold(channels[3], 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgRGB, contours, 0, (0,255,0), 3)
    x,y,w,h=cv2.boundingRect(contours[0])
    cv2.rectangle(imgRGB,(x,y),(x+w,y+h),(0,0,255),3)

    cv2.imshow("Piece2", imgRGB)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    readAndShowRGBImage()


