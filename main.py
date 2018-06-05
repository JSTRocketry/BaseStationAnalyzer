import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()



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

weightData = []

def parseString(line):
    weightIndex = line.index("@{")
    timeIndex = line.index(";")
    endLine = line.index("}@")
    weight = line[(weightIndex + 2):timeIndex]
    time = line[(timeIndex + 1):endLine-1]
    return [float(weight), float(time)]

def main():
    file = open(filedialog.askopenfilename(), 'r')
    for line in file:
        weightData.append(parseString(line))
    thrustData = WeightToThrustAnalyzer(weightData)
    print("Propellant Weight: " + str(thrustData.getPropellantWeight()))
    print("Max Thrust: " + str(thrustData.getMaxThrust()[0]) + " Newtons At Time: " + str(thrustData.getMaxThrust()[1]))
    print("Burn time: " + str(thrustData.getBurnTime()))
    print("Total Impulse: " + str(thrustData.getImpulse()))

main()
