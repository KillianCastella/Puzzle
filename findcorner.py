import cv2
import numpy as np

img =  cv2.imread("img/1.png")
imgRGB = cv2.imread("img/1.png",cv2.IMREAD_UNCHANGED)
channels = cv2.split(imgRGB)
imgray = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
if imgRGB is None:
    print("erreur ouverture fichier")
ret, gray = cv2.threshold(channels[3], 127, 255, 0)

# find Harris corners
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)
dst = cv2.dilate(dst,None)
ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
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

cv2.imwrite('subpixel5.png',img)