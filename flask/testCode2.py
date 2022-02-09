import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import seaborn as sns
import numpy as np
from scipy import interpolate

pix_res = (8,8) # pixel resolution
xx,yy = (np.linspace(0,pix_res[0],pix_res[0]),
                    np.linspace(0,pix_res[1],pix_res[1]))
# new resolution
pix_mult = 6 # multiplier for interpolation 
interp_res = (int(pix_mult*pix_res[0]),int(pix_mult*pix_res[1]))
grid_x,grid_y = (np.linspace(0,pix_res[0],interp_res[0]),
                            np.linspace(0,pix_res[1],interp_res[1]))

def interp(z_var):
    
    f = interpolate.interp2d(xx,yy,z_var,kind='cubic')
    return f(grid_x,grid_y)

data = [21.75, 21.75, 21.5, 21.25, 21.75, 41.5, 21.75, 22.25, 23.0, 22.25, 21.75, 22.0, 22.25, 22.0, 22.25, 22.5, 23.25, 23.25, 21.75, 22.25, 22.25, 22.25, 22.0, 21.75, 22.25, 23.0, 26.0, 27.75, 24.5, 22.25, 22.0, 22.75, 23.5, 23.25, 25.5, 27.0, 26.5, 23.0, 22.75, 23.0, 23.5, 23.75, 25.25, 28.75, 27.0, 25.0, 25.0, 24.75, 25.25, 26.0, 26.5, 27.75, 27.25, 27.75, 27.75, 27.25, 27.25, 27.5, 27.75, 28.0, 27.5, 28.0, 28.75, 28.75];
for index in range(len(data)):
    if int(data[index]) < 23:
        data[index] = 0.
 
    
data = interp(np.reshape(data,pix_res))

maxX = 16;
minX = 10;
maxY = 15;
minY = 10;       
# for x in range(minX, maxX):
#     for y in range(minY, maxY):
#         if(x == minX or x == maxX-1 or y == minY or y == maxY-1):
#             data[x][y] = 0.42


sns.heatmap(data)
plt.xticks(color='w')   
plt.yticks(color='w')
plt.savefig("d:/aa1.jpg", bbox_inches='tight', pad_inches=0)
rect = patches.Rectangle((minY,minX),
     maxY-minY,
     maxX-minX,
     linewidth=1,
     edgecolor='cyan',
     fill = False)

ax = plt.gca()
ax.add_patch(rect)
plt.savefig("d:/aa2.jpg", bbox_inches='tight', pad_inches=0)
print("complate")

plt.clf()
