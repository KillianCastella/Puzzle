import cv2
import numpy as np
import os
import math

sideColor=[(39,253,61),(39,54,253),(240,8,225),(240,155,8),(255,255,255)]

def distpp(p1,p2):
    return (p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])

def isAngle(x,y,angles):
    for index ,a in enumerate(angles):
        if(math.sqrt(pow(x-a[0],2)+pow(y-a[1],2)) <5):
            angles.pop(index)
            return True
    return False

def findangle(datas, w, h):
    angles = []
    c1 = (0, 0)
    c2 = (w, 0)
    c3 = (w, h)
    c4 = (0, h)
    #il est possible de rajouter facilement un point de contrôle supplémentaire.
    angle1 = [c1, [datas[0], distpp(c1, datas[0])], [datas[0], distpp(c1, datas[0])]]
    angle2 = [c2, [datas[0], distpp(c2, datas[0])], [datas[0], distpp(c2, datas[0])]]
    angle3 = [c3, [datas[0], distpp(c3, datas[0])], [datas[0], distpp(c3, datas[0])]]
    angle4 = [c4, [datas[0], distpp(c4, datas[0])], [datas[0], distpp(c4, datas[0])]]
    angletest = [angle1, angle2, angle3, angle4]
    '''test laissé si besoin
    itercorners = iter(datas)
    next(itercorners)
    #for point in itercorners:'''
    for point in datas[1:]:
        for i in angletest:
            temp = distpp(point, i[0])
            if i[1][1] > temp:
                i[2][1] = i[1][1]
                i[2][0] = i[1][0]
                i[1][1] = temp
                i[1][0] = point
            elif i[2][1] > temp:
                i[2][1] = temp
                i[2][0] = point

    for i in angletest:
        angles.append(i[1][0])
    return angles


def workimg(path):
    print(path)
    img =  cv2.imread("img/"+path)
    imgRGB = cv2.imread("img/"+path,cv2.IMREAD_UNCHANGED)

    channels = cv2.split(imgRGB)
    imgray = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
    if imgRGB is None:
        print("erreur ouverture fichier")
    ret, gray = cv2.threshold(channels[3], 127, 255, 0)

    _, contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0,0,0), 1)

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
    cornersint = np.int0(centroids)
    height, width = img.shape[:2]
    angles=findangle(cornersint, width, height)
    posx, posy = zip(*angles)
    
    #side separation
    sides=[]
    currentside=0
    sides.append([])
    #make a list with angles
    for x in range(0,contours[0].size // 2):
        if(isAngle(contours[0][x][0][0],contours[0][x][0][1],angles)):
            sides[currentside].append(contours[0][x][0])
            currentside = currentside +1
            sides.append([])
        else:
            sides[currentside].append(contours[0][x][0])

    for l in range(0,len(sides)):
        for s in sides[l]:
            img[s[1],s[0]]=sideColor[l]
    cv2.imwrite("im2/"+path,img)

def main():
    listing = os.listdir("img")
    for list in listing:
        workimg(list)

main()
