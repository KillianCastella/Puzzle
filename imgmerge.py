import cv2
import numpy as np
	
def readAndShowRGBImage():
    #base image
    imgOne = cv2.imread("img/1.png",cv2.IMREAD_UNCHANGED)
    imgSix = cv2.imread("img/6.png",cv2.IMREAD_UNCHANGED)
    heightOne, widthOne, _ = imgOne.shape 
    heightTwo, widthTwo, _ = imgSix.shape 

    #create a white destination image
    result = np.zeros((heightOne, widthOne+widthTwo, 4), np.uint8)
    result[:] = (255,255,255,255)

    #copy base image into destination image
    result[0:heightOne,0:widthOne]=imgOne
    result[0:heightTwo,widthOne:]=imgSix
    print(imgOne.shape)
    print(imgSix.shape)
    print(result.shape)

    cv2.imwrite("oui.png",result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

if __name__ == '__main__':
    readAndShowRGBImage()


