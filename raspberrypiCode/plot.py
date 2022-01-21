import serial
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np
import threading as Threading
import time

class plot():
    kp = 100.0
    ki = 0.0
    kd = 0.0
    val = ""
    def plotStart(self):
        self.arduino = serial.Serial('/dev/ttyAMA2', 115200, timeout = 0.001)

        self.fig = plt.figure()
        ax = plt.axes(xlim=(0, 500), ylim=(-30, 30))
        self.line, = ax.plot([], [], lw=2)

        max_points = 130
        x1 = np.linspace(0,max_points,100)
        y1 = np.cos(4*np.pi*x1)
        #line, = ax.plot(np.arange(max_points), 
        #                np.ones(max_points, dtype=np.float)*np.nan, lw=2)
        self.line, = ax.plot(x1, y1,lw=2)

    def init(self):
        return self.line,
    
    def getValue(self):
        print(self.val)

    def animate(self,i):
        send = (str(self.kp)+","+str(self.ki)+","+str(self.kd)+'\0').encode()
        self.arduino.write(send)
        val = self.arduino.readline()
        if val :
            val = val.decode()
            val = val.split(",")
            self.val = val
        else:
            val = [0,0]
        y = float(val[0])

        y = 0.0
        old_y = self.line.get_ydata()
        new_y = np.r_[old_y[1:], y]
        self.line.set_ydata(new_y)
        
        target = float(val[0])
        return self.line,
    
    def start(self):
        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init, frames=200, interval=500, blit=False)
        plt.show()
        while True():
            pass

p = plot()
p.plotStart()
t = Threading.Thread(target = p.start, args=())
t.start()

time.sleep(5)
while True:
    print("[1]Kp     [2]Ki     [3]Kd   [4]getPrint")
    index = input()
    if (index == "1"):
        value = input("Kp: ")
        p.kp = float(value)
        
    elif (index == "2"):
        value = input("Ki: ")
        p.ki = float(value)
        
    elif (index == "3"):
        value = input("Kd: ")
        p.kd = float(value)
        
    elif (index == "4"):
        p.getValue()
        
