import numpy as np
from PIL import Image
import numba
from math import floor


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


with open('model.obj', 'r') as file:
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
    
    # for i in v:
    #     img_mat[-i[0]+500][-i[1]+500]= 255

    for i in range(len(f)):
        x0 = v[f[i][0]-1][0] + 500
        y0 = -v[f[i][0]-1][1] + 900

        x1 = v[f[i][1]-1][0] + 500
        y1 = -v[f[i][1]-1][1] + 900

        x2 = v[f[i][2]-1][0] + 500
        y2 = -v[f[i][2]-1][1] + 900

        line(img_mat,x0,y0,x1,y1)
        line(img_mat,x0,y0,x2,y2)
        line(img_mat,x2,y2,x1,y1)


img = Image.fromarray(img_mat)
img.save('img.png')