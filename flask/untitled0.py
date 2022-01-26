import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
import time,sys
sys.path.append('../')
import amg8833_i2c

t0 = time.time()
sensor = []
while (time.time()-t0)<1: # wait 1sec for sensor to start
    try:
        # AD0 = GND, addr = 0x68 | AD0 = 5V, addr = 0x69
        sensor = amg8833_i2c.AMG8833(addr=0x69) # start AMG8833
    except:
        sensor = amg8833_i2c.AMG8833(addr=0x68)
    finally:
        pass
time.sleep(0.1) # wait for sensor to settle

# If no device is found, exit the script
if sensor==[]:
    print("No AMG8833 Found - Check Your Wiring")
    sys.exit(); # exit the app if AMG88xx is not found 

pix_res = (8,8) # pixel resolution
xx,yy = (np.linspace(0,pix_res[0],pix_res[0]),
                    np.linspace(0,pix_res[1],pix_res[1]))
zz = np.zeros(pix_res) # set array with zeros first
# new resolution
pix_mult = 6 # multiplier for interpolation 
interp_res = (int(pix_mult*pix_res[0]),int(pix_mult*pix_res[1]))
grid_x,grid_y = (np.linspace(0,pix_res[0],interp_res[0]),
                            np.linspace(0,pix_res[1],interp_res[1]))


def interp(z_var):
    f = interpolate.interp2d(xx,yy,z_var,kind='cubic')
    return f(grid_x,grid_y)


 
pix_to_read = 64

while True:
    
    status,data = sensor.read_temp(pix_to_read) # read pixels with status
    if status:
        continue
    for index in range(len(data)):
        if int(data[index]) < 20:
            data[index] -= 5
    print(data)    
    data = interp(np.reshape(data,(8,8)))
    sns.heatmap(data)
    plt.draw()
    plt.pause(0.1)
    plt.clf()
