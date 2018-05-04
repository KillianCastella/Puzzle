import cv2
import numpy as np

img = cv2.imread("img/1.png")
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

angles = []
cornersint = np.int0(corners)
height, width = img.shape[:2]

def distpp(p1,p2):
    return (p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1])


def findangle(datas, w, h):
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


cotes = []


def calculfx(x, dia):
    print("  fx: ", dia[1][1]*(x-dia[0][0])/dia[1][0] + dia[0][1])
    return dia[1][1]*(x-dia[0][0])/dia[1][0] + dia[0][1]


def calculfy(y, dia):
    print("  fy: ", dia[1][0]*(y-dia[0][1])/dia[1][1] + dia[0][0])
    return dia[1][0]*(y-dia[0][1])/dia[1][1] + dia[0][0]


def defineside(listcorners):
    cote1 = []
    cote2 = []
    cote3 = []
    cote4 = []
    diago1 = [listcorners[0], [listcorners[2][0]-listcorners[0][0], listcorners[2][1]-listcorners[0][1]]]
    diago2 = [listcorners[3], [listcorners[1][0]-listcorners[3][0], listcorners[1][1]-listcorners[3][1]]]
    print(cornersint)
    for point in cornersint:
        print("  ", point)
        if listcorners[0][0] < point[0] < listcorners[1][0]:
            if point[1] < calculfx(point[0], diago1) and point[1] < calculfx(point[0], diago2):
                cote1.append(point)
        elif listcorners[1][1] < point[1] < listcorners[2][1]:
            if point[0] < calculfy(point[1], diago1) and point[0] < calculfy(point[1], diago2):
                cote2.append(point)
        elif listcorners[3][0] < point[0] < listcorners[2][0]:
            if point[1] > calculfx(point[0], diago1) and point[1] > calculfx(point[0], diago2):
                cote3.append(point)
        elif listcorners[0][1] < point[1] < listcorners[3][1]:
            if point[0] > calculfy(point[1], diago1) and point[0] > calculfy(point[1], diago2):
                cote4.append(point)
    cotes.append(cote1)
    cotes.append(cote2)
    cotes.append(cote3)
    cotes.append(cote4)


findangle(cornersint, width, height)

defineside(angles)
print(cotes)

posx, posy = zip(*angles)
print([posy[:], posx[:]])
img[posy[:], posx[:]] = [255,0,0]
cv2.imwrite('angles2.png',img)
print(angles)
