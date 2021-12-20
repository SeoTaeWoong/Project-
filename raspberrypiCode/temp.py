import serial
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np

arduino = serial.Serial('/dev/ttyAMA2', 115200, timeout = 0.001)

fig = plt.figure()
ax = plt.axes(xlim=(0, 500), ylim=(-30, 30))
line, = ax.plot([], [], lw=2)

max_points = 130
x1 = np.linspace(0,max_points,100)
y1 = np.cos(4*np.pi*x1)
#line, = ax.plot(np.arange(max_points), 
#                np.ones(max_points, dtype=np.float)*np.nan, lw=2)
line, = ax.plot(x1, y1,lw=2)

def init():
    return line,

def animate(i):
    val = arduino.readline()
    val = val.decode()
    val = val.split(",")
    y = float(val[0])

    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:], y]
    line.set_ydata(new_y)
    
    target = float(val[0])
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, interval=500, blit=False)

plt.show()
