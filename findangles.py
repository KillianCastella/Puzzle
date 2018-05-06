import numpy as np
import cv2
from scipy.spatial import distance
import math
import os


def distpp(p1, p2):
    '''Méthode rendant la distance entre les deux points entrés en paramètres'''
    #return (p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def findangle(datas, w, h, qdens):
    '''Méthode grossière pour trouver les angles'''
    angles = []
    c1 = (0, 0)
    c2 = (w, 0)
    c3 = (w, h)
    c4 = (0, h)
    #Variables du second test
    atangle = 0
    # il est possible de rajouter facilement un point de contrôle supplémentaire.
    angle1 = [c1, [datas[0], distpp(c1, datas[0])], [datas[0], distpp(c1, datas[0])]]
    angle2 = [c2, [datas[0], distpp(c2, datas[0])], [datas[0], distpp(c2, datas[0])]]
    angle3 = [c3, [datas[0], distpp(c3, datas[0])], [datas[0], distpp(c3, datas[0])]]
    angle4 = [c4, [datas[0], distpp(c4, datas[0])], [datas[0], distpp(c4, datas[0])]]
    angletest = [angle1, angle2, angle3, angle4]
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
    for d in qdens:
        if d < 1:
            if atangle == 0:
                angles[atangle] = [0, 0]
            elif atangle == 1:
                angles[atangle] = [w - 1, 0]
            elif atangle == 2:
                angles[atangle] = [w - 1, h - 1]
            elif atangle == 3:
                angles[atangle] = [0, h - 1]
        atangle += 1
    return angles


''' Tentative d'amélioration de la recherche d'angle
def checkangles(angles, ):
    for d in qdens:
        if d < 1:
            if i == 0:
                angles[i] = [0, 0]
            elif i == 1:
                angles[i] = [width - 1, 0]
            elif i == 2:
                angles[i] = [width - 1, height - 1]
            elif i == 3:
                angles[i] = [0, height - 1]
        i += 1


#def anglefinder(quart, w, h):
'''


def density(data, w, h):
    '''Méthode séparant les points par quadrans et comptant le nombre dans chacun'''
    q = [0, 0, 0, 0]
    q1 = []
    q2 = []
    q3 = []
    q4 = []
    for i in data:
        if 0 <= i[0] < w/2:
            if 0 <= i[1] < h/2:
                q[0] += 1
                q1.append(i)
            if h / 2 <= i[1] <= h:
                q[3] += 1
                q4.append(i)
        elif w/2 <= i[0] <= w:
            if 0 <= i[1] < h / 2:
                q[1] += 1
                q2.append(i)
            if h / 2 <= i[1] <= h:
                q[2] += 1
                q3.append(i)
    return q, q1, q2, q3, q4


def closest_node(node, nodes):
    '''Méthode permettant de trouver le point d'une liste étant le plus proche du point passé en paramètre.'''
    closest_index = distance.cdist([node], nodes).argmin()
    return nodes[closest_index]


def side_test(datas, angle, nbpoints):
    '''Méthode qui va initier la conception des 4 côtés d'une pièce.'''
    d = angle
    cd = [angle]
    cf = [angle]
    if nbpoints<2:
        f = angle
    else:
        datas.remove(d)
        f = closest_node(d, datas)
        datas.remove(f)
        cf.append(f)
        if nbpoints > 2:
            nbpoints -= 2
            while nbpoints >0:
                '''Pour plus de sureté, on essaie de parcourir les deux côtés d'un angle en même temps.
                   Cela permet de supprimer un nombre certains d'erreur.'''
                wayd = distpp(angle, d)
                wayf = distpp(angle, f)
                if wayd > wayf:
                    newpoint = closest_node(f, datas)
                else:
                    newpoint = closest_node(d, datas)
                testd = distpp(newpoint, d)
                testf = distpp(newpoint, f)
                if testd < testf:
                    cd.append(newpoint)
                    d = newpoint
                else:
                    cf.append(newpoint)
                    f = newpoint
                nbpoints -= 1
                datas.remove(newpoint)
    return d, f, cd, cf


def fullside(c1, c2, x, y):
    '''Méthode pour relier les coins entre eux afin de former les côtés.'''
    c1a = distpp(c1[0], [x, y])
    c1b = distpp(c1[1], [x, y])
    c2b = distpp(c2[1], [x, y])
    c2a = distpp(c2[0], [x, y])
    c2p1 = c2[2]
    c2p1.reverse()
    c2p2 = c2[3]
    c2p2.reverse()
    if c1a < c1b:
        if c2a <= c2b:
            return c1[2] + c2p1
        else:
            return c1[2] + c2p2
    else:
        if c2a <= c2b:
            return c1[3] + c2p1
        else:
            return c1[3] + c2p2


def working(path):
    '''Méthode gérant la classification des pièces ainsi que les modifications de leur image.'''
    img = cv2.imread("img/"+path)
    imgRGB = cv2.imread("img/"+path,cv2.IMREAD_UNCHANGED)
    channels = cv2.split(imgRGB)
    imgray = cv2.cvtColor(imgRGB, cv2.COLOR_BGR2GRAY)
    if imgRGB is None:
        print("erreur ouverture fichier")
    #obtention des contours en passant par l'image du canal alpha
    ret, gray = cv2.threshold(channels[3], 127, 255, 0)
    ret,thresh = cv2.threshold(channels[3],127,255,0)
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #dessin des contours de la pièce
    cv2.drawContours(img, contours, -1, (0,255,0), 1)
    #obtention des coins de la pièce avec la méthode des bon traits à relever
    corners = cv2.goodFeaturesToTrack(gray, 300, 0.01, 5)
    corners = np.int0(corners)
    data = []
    for corner in corners:
        x, y = corner.ravel()
        data.append([x,y])
        cv2.circle(img, (x, y), 1, 1, -1)
    #acquisition des valeurs nécessaires à l'étude des pièces
    height, width = img.shape[:2]
    qdens, q1, q2, q3, q4 = density(data, width, height)
    angles = findangle(data, width, height, qdens)
    #mise en place des coins
    corner1 = side_test(q1, angles[0], qdens[0])
    corner2 = side_test(q2, angles[1], qdens[1])
    corner3 = side_test(q3, angles[2], qdens[2])
    corner4 = side_test(q4, angles[3], qdens[3])
    side1 = fullside(corner1, corner2, width/2, 0)
    side2 = fullside(corner2, corner3, width, height/2)
    side3 = fullside(corner3, corner4, width/2, height)
    side4 = fullside(corner4, corner1, 0, height/2)

    #dessin corner1
    posx, posy = zip(*side1)
    img[posy[:], posx[:]] = [0,0,255]
    '''posx, posy = zip(*corner1[3])
    img[posy[:], posx[:]] = [255,0,0]
    #dessin corner2
    posx, posy = zip(*corner2[2])
    img[posy[:], posx[:]] = [0,255,0]
    posx, posy = zip(*corner2[3])
    img[posy[:], posx[:]] = [255,0,0]
    #dessin corner3
    posx, posy = zip(*corner3[2])
    img[posy[:], posx[:]] = [0,255,0]
    posx, posy = zip(*corner3[3])
    img[posy[:], posx[:]] = [255,0,0]
    #dessin corner4
    posx, posy = zip(*corner4[2])
    img[posy[:], posx[:]] = [0,255,0]
    posx, posy = zip(*corner4[3])
    img[posy[:], posx[:]] = [255,0,0]'''
    #dessin angles
    posx, posy = zip(*angles)
    img[posy[:], posx[:]] = [255,255,255]
    #enregistrement de l'image dans un fichier
    cv2.imwrite("imtest/" + path, img)


if __name__ == "__main__":
    listing = os.listdir("img")
    for list in listing:
        working(list)
