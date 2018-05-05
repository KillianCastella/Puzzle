import cv2
import numpy as np
import os

def workimg(path):
    print(path)
    img =  cv2.imread("img/"+path)
    
    imgRGB = cv2.imread("img/"+path,cv2.IMREAD_UNCHANGED)
    channels = cv2.split(imgRGB)
    imgray = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
    if imgRGB is None:
        print("erreur ouverture fichier")
    ret, gray = cv2.threshold(channels[3], 127, 255, 0)

    # find Harris corners
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    factor=0.02
    while True : 
        try:
            ret, dst = cv2.threshold(dst,factor*dst.max(),255,0)
            dst = np.uint8(dst)

            # find centroids
            ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

            # define the criteria to stop and refine the corners
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
            corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

            # Now draw them
            res = np.hstack((centroids,corners))
            res = np.int0(res)
            img[res[:,1],res[:,0]]=[0,0,255]
            img[res[:,3],res[:,2]] = [0,255,0]
            break 
        except:   
            factor = factor + 0.02


    cv2.imwrite("im2/"+path,img)

listing = os.listdir("img")
for list in listing:
    workimg(list)