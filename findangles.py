import cv2
import numpy as np

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
            print("up")

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
    #print("  fx: ", dia[1][1]*(x-dia[0][0])/dia[1][0] + dia[0][1])
    return dia[1][1]*(x-dia[0][0])/dia[1][0] + dia[0][1]


def calculfy(y, dia):
    #print("  fy: ", dia[1][0]*(y-dia[0][1])/dia[1][1] + dia[0][0])
    return dia[1][0]*(y-dia[0][1])/dia[1][1] + dia[0][0]


q1 = []
q2 = []
q3 = []
q4 = []


def density(data):
    q = [0, 0, 0, 0]
    q1.clear()
    q2.clear()
    q3.clear()
    q4.clear()
    for i in data:
        if 0 <= i[0] < int(width/2):
            if 0 <= i[1] < height/2:
                q[0] += 1
                q1.append(i)
            if height / 2 <= i[1] <= height:
                q[3] += 1
                q4.append(i)
        elif width/2 <= i[0] <= width:
            if 0 <= i[1] < height / 2:
                q[1] += 1
                q2.append(i)
            if height / 2 <= i[1] <= height:
                q[2] += 1
                q3.append(i)
    return q


def firstdist(data, used, p):
    #used ne doit pas être vide
    for i in data:
        if not any(t[0] == i[0] and t[1] == i[1] for t in used):
            return [i, distpp(p, i)]


def mindist(data, used, p, dist):
    ptemp = p
    for i in data:
        if not any(t[0] == i[0] and t[1] == i[1] for t in used):
            newdist = distpp(i, p)
            if newdist <= dist:
                ptemp = i
                dist = newdist
    return [ptemp, dist]


def sides(data, angle, nbpoints):
    d = angle
    used = []
    used.append(angle)
    #define destination
    f, distd = firstdist(data, used, angle)
    used.append(f)
    sf = [angle,f]
    sd = [angle]
    #find next dist
    tempd, x = firstdist(data, used, d)
    tempf, y = firstdist(data, used, f)
    while nbpoints >0:
        tempd, x = mindist(data, used, d, x)
        tempf, y = mindist(data, used, f, y)
        if x < y:
            sd.append(tempd)
            used.append(tempd)
            d = tempd
        elif y < x:
            sf.append(tempf)
            used.append(tempf)
            f = tempf
        print(sd)
        print(sf)
        nbpoints -= 1


findangle(cornersint, width, height)
qdens = density(cornersint)
sides(q2, angles[1], qdens[1])

#defineside(angles)
#print(cotes)

posx, posy = zip(*angles)
#print([posy[:], posx[:]])
img[posy[:], posx[:]] = [255,0,0]
cv2.imwrite('angles2.png',img)
#print(angles)
