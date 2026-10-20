import numpy as np
from PIL import Image
import numba
from math import floor, ceil


img_mat = np.zeros((1000,1000, 3), dtype=np.uint8)

x1,x2,y1,y2 = 400, 500, 600, 900


def line(i_m, x0, y0, x1, y1):
    d_max = max(abs(floor(x1) - floor(x0)), abs(floor(y1) - floor(y0)))
    L = d_max + 1
    if L == 1:
        i_m[floor(y0)][floor(x0)] = [200,150,255]
    else:
        d_x = (x1 - x0)/(L-1)
        d_y = (y1 - y0)/(L-1)
        x = x0
        y = y0
        for _ in range(L):
            i_m[floor(y)][floor(x)] = [200,150,255]
            x += d_x
            y += d_y


def bar_coordinates(x, y, x0,y0,x1,y1,x2,y2):
    x = int(x)
    y = int(y)
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2))
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / ((x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2)) 
    lambda2 = 1.0 - lambda0 - lambda1

    return lambda0, lambda1, lambda2

def triangle(x0,y0,z0,x1,y1,z1,x2,y2,z2, color,z_buffer):
    x_min = int(max(min(x0,x1,x2), 0))
    x_max = ceil(min(max(x0,x1,x2), 1000))
    y_min = int(max(min(y0,y1,y2),0))
    y_max = ceil(min(max(y0,y1,y2), 1000))

    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            lambdas = np.array(bar_coordinates(x, y, x0,y0,x1,y1,x2,y2))
            if np.all(lambdas >= 0):
                z = lambdas[0]*z0 + lambdas[1]*z1 + lambdas[2]*z2
                
                if z < z_buffer[y][x]:
                    z_buffer[y][x] = z
                    img_mat[y][x] = color


def get_normal(x0,y0,z0,x1,y1,z1,x2,y2,z2):
    n = np.cross(np.array([x1 - x2, y1 - y2, z1 - z2]), np.array([x1 - x0, y1- y0, z1 - z0]))
    return n


with open(r"C:\Projects\Learning\Computer_Graphics\LR_2\model.obj", 'r') as file:
    v = []
    
    f = []
    for s in file:
        s1 = s.split()
        if s1[0] == 'v':
            v.append(s1[1::])
        if s1[0] == 'f':
            f0 = []
            for i in s1[1::]:
                f0.append(i.split('/')[0])
            f.append(f0)

    v = np.array(v).astype(float)
    f = np.array(f).astype(int)


    v = v*8000
    
    z_buffer = np.zeros((1000,1000)) + np.inf
    l = np.array([0, 0, 1]) 

    for i in range(len(f)):
        x0 = v[f[i][0]-1][0] + 500
        y0 = -v[f[i][0]-1][1] + 900
        z0 = v[f[i][0]-1][2]

        x1 = v[f[i][1]-1][0] + 500
        y1 = -v[f[i][1]-1][1] + 900
        z1 = v[f[i][1]-1][2]

        x2 = v[f[i][2]-1][0] + 500
        y2 = -v[f[i][2]-1][1] + 900
        z2 = v[f[i][2]-1][2]

        
        n = -get_normal(x0,y0,z0,x1,y1,z1,x2,y2,z2)
                    
        cos_a = (n@l)/(np.linalg.norm(n)*np.linalg.norm(l))

        color = np.array([-255*cos_a, 0, 0])


        if cos_a < 0:
            triangle(x0,y0,z0,x1,y1,z1,x2,y2,z2, color, z_buffer)





img = Image.fromarray(img_mat)
img.save(r'LR_2\img.png')