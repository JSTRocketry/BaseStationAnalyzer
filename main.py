from tkinter import filedialog
from tkinter import *
import serial
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

root = Tk()

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
            if i[0] < self.engineData[0][0]:
                burnTime = i[1] - self.engineData[0][1]
                return burnTime

    def convertToThrust(self):
        for i in range(1,len(self.engineData)):
            self.engineData[i][0] -= self.engineData[0][0]
        self.engineData[0][0] = 0
        for i in self.engineData:
            i[0] *= self.GRAVITY

    def getImpulse(self):
        area = 0
        #find burn time
        burnTime = self.getBurnTime()
        counter = 0
        while self.engineData[counter][1] < burnTime:
            midpoint = (self.engineData[counter + 1][0] - self.engineData[counter][0])/2.0 + self.engineData[counter][0]
            tempArea = midpoint * (self.engineData[counter+1][1] - self.engineData[counter][1])/1000.0
            counter += 1
            if(tempArea > 0):
                area += tempArea

        #for i in range(0,len(self.engineData)-1):
        #    midpoint = (self.engineData[i + 1][0] - self.engineData[i][0])/2.0 + self.engineData[i][0]
        #    tempArea = midpoint * (self.engineData[i+1][1] - self.engineData[i][1])/1000.0
        #    if(tempArea > 0):
        #        area += tempArea
        return area


class UserInterface():
    weightData = []
    def __init__(self, master):
        master.columnconfigure(0,weight=1)
        master.rowconfigure(1,weight=1)
        self.master = master
        self.master.title("Engine Test Analyzer")
        self.master.geometry('800x800')
        self.addModeButtons()
        self.master.attributes("-zoomed", False)
        self.addCalculationTextBoxes()
        self.createGraph()
        self.master.bind("<Escape>", self.end_fullscreen)

    def end_fullscreen(self, event=None):
        self.state = False
        sys.exit()

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
        self.ax0 = self.f.add_axes( (0.05, .05, .90, .90), axisbg=(.75,.75,.75), frameon=False)
        self.ax0.set_xlabel( 'Time (ms)' )
        self.ax0.set_ylabel( 'Thrust (N)' )
        self.ax0.grid(color='r',linestyle='-', linewidth=2)
        #self.ax0.plot(np.max(np.random.rand(100,10)*10,axis=1),"r-")
        self.frame = Frame(self.master)
        self.frame.grid(column=0,row=1,columnspan=4, rowspan=3, sticky=N+W+E+S)
        self.canvas = FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        self.canvas.show()
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame )
        #self.toolbar.grid(column = 0, row = 2, columnspan=2)
        self.toolbar.update()

    def addModeButtons(self):
        self.openButton = Button(self.master, text='Open', command=self.handleOpen)
        self.openButton.grid(column=2,row=0)

    def addCalculationTextBoxes(self):
        self.propellantWeight = Label(self.master, text="Propellant Weight: N/A",font=("Arial Bold", 20))
        self.burnTime = Label(self.master, text="Burn Time: N/A",font=("Arial Bold", 20))
        self.maxThrust = Label(self.master, text="Max Thrust: N/A",font=("Arial Bold", 20))
        self.totalImpulse = Label(self.master, text="Total Impulse: N/A",font=("Arial Bold", 20))
        self.propellantWeight.grid(column = 0, row = 4,sticky = W)
        self.burnTime.grid(column = 0, row = 4)
        self.maxThrust.grid(column = 1, row = 4, sticky = W)
        self.totalImpulse.grid(column = 3, row = 4)

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
            self.weightData.append(self.parseString(line))
        f.close()

    def handleOpen(self):
        file = filedialog.askopenfilename()
        self.openAndParseFile(file)
        self.thrustData = WeightToThrustAnalyzer(self.weightData)
        self.propellantWeight.configure(text="Propellant Weight: " + str(round(self.thrustData.getPropellantWeight(),3)) + " Kg")
        self.burnTime.configure(text="Burn Time: " + str(round(self.thrustData.getBurnTime(),3)) + " sec")
        self.totalImpulse.configure(text="Total Impulse: " + str(round(self.thrustData.getImpulse(),3)) + " N-S")
        self.maxThrust.configure(text="Max Thrust: " + str(round(self.thrustData.getMaxThrust()[0],3)) + " N")
        print("Propellant Weight: " + str(self.thrustData.getPropellantWeight()))
        print("Max Thrust: " + str(self.thrustData.getMaxThrust()[0]) + " Newtons At Time: " + str(self.thrustData.getMaxThrust()[1]))
        print("Burn time: " + str(self.thrustData.getBurnTime()))
        print("Total Impulse: " + str(self.thrustData.getImpulse()))
        self.plotGraph()
        print("Plotted")

def main():
    root.attributes("-zoomed", True)
    gui = UserInterface(root)
    root.mainloop()

main()
