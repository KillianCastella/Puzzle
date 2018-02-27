import cv2
import numpy as np
	
def readAndShowRGBImage():
    imgRGB = cv2.imread("img/1.png")
    if imgRGB is None:
        print("erreur ouverture fichier")
        return 0
    cv2.imshow("Pièce", imgRGB)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    readAndShowRGBImage()


