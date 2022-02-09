import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import cv2
import os


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

def createDirectory(directoryNameList, filePath):
    
    for index in range(len(directoryNameList)):
        directoryNameList[index] = directoryNameList[index].replace(":","-");    
        filePath += directoryNameList[index]+"/"
        try:
            if not os.path.exists(filePath):
                os.makedirs(filePath)
        except OSError:
            print ('Error: Creating directory. ' +  filePath)


def amg8833_IMG_Save(data, filePath, rectFilePath, x1,y1,x2,y2):
    data = [21.75, 21.75, 21.5, 21.25, 21.75, 41.5, 21.75, 22.25, 23.0, 22.25, 21.75, 22.0, 22.25, 22.0, 22.25, 22.5, 23.25, 23.25, 21.75, 22.25, 22.25, 22.25, 22.0, 21.75, 22.25, 23.0, 26.0, 27.75, 24.5, 22.25, 22.0, 22.75, 23.5, 23.25, 25.5, 27.0, 26.5, 23.0, 22.75, 23.0, 23.5, 23.75, 25.25, 28.75, 27.0, 25.0, 25.0, 24.75, 25.25, 26.0, 26.5, 27.75, 27.25, 27.75, 27.75, 27.25, 27.25, 27.5, 27.75, 28.0, 27.5, 28.0, 28.75, 28.75];
    for index in range(len(data)):
        if int(data[index]) < 23:
            data[index] = 0.
        
    data = interp(np.reshape(data,pix_res))
    
    sns.heatmap(data)
    plt.xticks(color='w')
    plt.yticks(color='w')
    plt.savefig(filePath, bbox_inches='tight', pad_inches=0)
    
    rect = patches.Rectangle((y1,x1), x2-x1, y2-y1, linewidth=2, edgecolor='cyan', fill = False)
    ax = plt.gca()
    ax.add_patch(rect)
    plt.savefig(rectFilePath, bbox_inches='tight', pad_inches=0)
    plt.clf()
    
    

    
#amg8833_JPG_Save([21.75, 21.75, 21.5, 21.25, 21.75, 41.5, 21.75, 22.25, 23.0, 22.25, 21.75, 22.0, 22.25, 22.0, 22.25, 22.5, 23.25, 23.25, 21.75, 22.25, 22.25, 22.25, 22.0, 21.75, 22.25, 23.0, 26.0, 27.75, 24.5, 22.25, 22.0, 22.75, 23.5, 23.25, 25.5, 27.0, 26.5, 23.0, 22.75, 23.0, 23.5, 23.75, 25.25, 28.75, 27.0, 25.0, 25.0, 24.75, 25.25, 26.0, 26.5, 27.75, 27.25, 27.75, 27.75, 27.25, 27.25, 27.5, 27.75, 28.0, 27.5, 28.0, 28.75, 28.75])