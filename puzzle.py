import cv2
import numpy as np
	
def readAndShowRGBImage():
    imgRGB = cv2.imread("img/1.png",cv2.IMREAD_UNCHANGED)
    channels = cv2.split(imgRGB)
    # ADD COND TO CHECK IF IMG HAS 4 CHANNEL
    #imgray = cv2.cvtColor(channels[3], cv2.COLOR_BGR2GRAY)
    print(channels[3])
    if imgRGB is None:
        print("erreur ouverture fichier")
        return 0
    height, width, channels = imgRGB.shape
    print(height, width, channels)
    cv2.imshow("Piece", imgRGB)
    ret, thresh = cv2.threshold(channels[3], 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(imgRGB, contours, -1, (0,255,0), 3)
    cv2.imshow("Piece2", imgRGB)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    readAndShowRGBImage()


