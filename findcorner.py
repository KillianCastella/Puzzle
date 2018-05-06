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
    #récupération des images
    img =  cv2.imread("img/"+path)
    imgRGB = cv2.imread("img/"+path,cv2.IMREAD_UNCHANGED)

    channels = cv2.split(imgRGB)
    if imgRGB is None:
        print("erreur ouverture fichier")
    ret, gray = cv2.threshold(channels[3], 127, 255, 0)
    #recherche des contours
    _, contours, _ = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0,0,0), 1)

    #recherche des coins par la méthode de harris 
    #https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray,2,3,0.04)
    dst = cv2.dilate(dst,None)
    factor=0.02
    #recherche du facteur le plus optimisé
    while True : 
        try:
            ret, dst = cv2.threshold(dst,factor*dst.max(),255,0)
            dst = np.uint8(dst)

            #Trouver les centroids
            ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

            #Definition des critères et recherche des coins
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
            corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

            break
        except:   
            factor = factor + 0.02
    #séléction des coins importants
    cornersint = np.int0(centroids)
    height, width = img.shape[:2]
    angles=findangle(cornersint, width, height)
    posx, posy = zip(*angles)
    
    #séparation des cotés
    sides=[]
    currentside=0
    sides.append([])
    #tableau -> liste
    for x in range(0,contours[0].size // 2):
        if(isAngle(contours[0][x][0][0],contours[0][x][0][1],angles)):
            sides[currentside].append([contours[0][x][0][0],contours[0][x][0][1]])
            currentside = currentside +1
            sides.append([])
        else:
            sides[currentside].append([contours[0][x][0][0],contours[0][x][0][1]])
    #on remet le premier et le dernier bout ensemble
    if len(sides)>1 :
        for i in sides[0]:
            sides[len(sides)-1].append(i)
        sides[0]=sides[len(sides)-1]
        sides.pop()

    #création d'une structure de données adapté à la méthode drawcontours
    for l in range(0,len(sides)):
        ctr1 = np.array(sides[l]).reshape((-1,1,2)).astype(np.int32)
        cv2.drawContours(img,[ctr1],0,sideColor[l],2)
    
    #définition du type de pièces
    numberofBorder=0
    if len(sides)>1 :
        for side in sides:
            if len(side)<10:
                numberofBorder = numberofBorder + 1
    else:
        numberofBorder=-1

    #écriture des images 
    if numberofBorder==1:
        cv2.imwrite("result/border/"+path,img)
    elif numberofBorder>1:
        cv2.imwrite("result/corner/"+path,img)
    elif numberofBorder == -1:
        cv2.imwrite("result/undefined/"+path,img)
    else:
        cv2.imwrite("result/inner/"+path,img)

def main():
    #création des dossiers si non existants
    if not os.path.exists("result/inner/"):
        os.makedirs("result/inner/")
    if not os.path.exists("result/border/"):
        os.makedirs("result/border/")
    if not os.path.exists("result/undefined/"):
        os.makedirs("result/undefined/")
    if not os.path.exists("result/corner/"):
        os.makedirs("result/corner/")
        
    #recuperation et traitement de chaque image du dossier img
    listing = os.listdir("img")
    for list in listing:
        workimg(list)

main()
