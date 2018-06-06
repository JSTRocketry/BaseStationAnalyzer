from tkinter import filedialog
from tkinter import *
import serial
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

root = Tk()
#root.withdraw()



class WeightToThrustAnalyzer():
    BURN_TIME_TOLLERENCE = .03
    GRAVITY = 9.81
    engineData = []

    def __init__(self, weightData):
        self.engineData = weightData
        self.convertToThrust()

    def getMaxThrust(self):
        maxThrust = self.engineData[0]
        for i in self.engineData:
            if i[0] > maxThrust[0]:
                maxThrust = i
        return maxThrust

    def getPropellantWeight(self):
        return abs(self.engineData[0][0] - self.engineData[-1][0])/self.GRAVITY

    def getBurnTime(self):
        for i in self.engineData:
            if abs(1 - (i[0]/self.engineData[-1][0])) <= self.BURN_TIME_TOLLERENCE:
                burnTime = i[1] - self.engineData[0][1]
                return burnTime

    def convertToThrust(self):
        for i in self.engineData:
            i[0] *= self.GRAVITY

    def getImpulse(self):
        area = 0
        for i in range(0,len(self.engineData)-1):
            midpoint = (self.engineData[i + 1][0] - self.engineData[i][0])/2.0 + self.engineData[i][0]
            tempArea = midpoint * (self.engineData[i+1][1] - self.engineData[i][1])/1000.0
            if(tempArea > 0):
                area += tempArea
        return area


class UserInterface():
    weightData = []
    def __init__(self, master):
        master.columnconfigure(0,weight=1)
        master.rowconfigure(1,weight=1)
        self.master = master
        self.master.title("BaseStation")
        self.master.geometry('800x600')
        self.addModeButtons()
        self.createGraph()

    def plotGraph(self):
        xData = []
        yData = []
        for i in self.thrustData.engineData:
            xData.append(i[1])
            yData.append(i[0])
        self.ax0.plot(xData,yData)
        self.canvas.show()

    def createGraph(self):
        self.frame = Frame(self.master)
        self.f = Figure( figsize=(10, 9), dpi=80 )
        self.ax0 = self.f.add_axes( (0.05, .05, .90, .90), frameon=False)
        self.ax0.set_xlabel( 'Time (ms)' )
        self.ax0.set_ylabel( 'Thrust (N)' )
        self.ax0.grid(color='r',linestyle='-', linewidth=2)
        #self.ax0.plot(np.max(np.random.rand(100,10)*10,axis=1),"r-")
        self.frame = Frame( self.master )
        self.frame.grid(column=0,row=1,columnspan=3,sticky=N+S+E+W)
        self.canvas = FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.show()
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame )
        #self.toolbar.grid(column = 0, row = 2, columnspan=2)
        self.toolbar.update()

    def addModeButtons(self):
        self.openButton = Button(self.master, text='Open', command=self.handleOpen)
        self.openButton.grid(column=2,row=0)


    def parseString(self,line):
        weightIndex = line.index("@{")
        timeIndex = line.index(";")
        endLine = line.index("}@")
        weight = line[(weightIndex + 2):timeIndex]
        time = line[(timeIndex + 1):endLine-1]
        return [float(weight), float(time)]


    def openAndParseFile(self,fileName):
        f = open(fileName,'r')
        for line in f:
            #parse the line
            #add to the block
            self.weightData.append(self.parseString(line))
        f.close()

    def handleOpen(self):
        file = filedialog.askopenfilename()
        self.openAndParseFile(file)
        self.thrustData = WeightToThrustAnalyzer(self.weightData)
        print("Propellant Weight: " + str(self.thrustData.getPropellantWeight()))
        print("Max Thrust: " + str(self.thrustData.getMaxThrust()[0]) + " Newtons At Time: " + str(self.thrustData.getMaxThrust()[1]))
        print("Burn time: " + str(self.thrustData.getBurnTime()))
        print("Total Impulse: " + str(self.thrustData.getImpulse()))
        self.plotGraph()
        print("Plotted")





def main():
    gui = UserInterface(root)
    root.mainloop()


main()
