import tkinter as tk
from tkinter import filedialog
BURN_TIME_TOLLERENCE = .03

root = tk.Tk()
root.withdraw()


engineData = []
propellantWeight = 0
burnTime = 0
totalThrust = 0
maxThrust = []
impulse = 0

def getMaxThrust():
    global maxThrust
    maxThrust = engineData[0]
    #print(maxThrust)
    for i in engineData:
        if i[0] > maxThrust[0]:
            maxThrust = i
            print("new max")

def getPropellantWeight():
    global propellantWeight
    propellantWeight = float(engineData[0][0]) - float(engineData[-1][0])

def getBurnTime():
    global burnTime
    for i in engineData:
        if abs(1 - (i[0]/engineData[-1][0])) <= BURN_TIME_TOLLERENCE:
            burnTime = i[1] - engineData[0][1]
            return


def parseString(line):
    weightIndex = line.index("@{")
    timeIndex = line.index(";")
    endLine = line.index("}@")
    weight = line[(weightIndex + 2):timeIndex]
    time = line[(timeIndex + 1):endLine-1]
    engineData.append([float(weight), float(time)])

def getRocketThrust():
    thrust = []
    for i in engineData:
        thrust.append([i[0]*9.81, i[1]])
    return thrust

def getArea():
    #NOTE: time is x-axis, thrust/weight is y-axis
    graphArea = []
    midpoint = []
    width = 0.0
    height = 0.0
    for i in range(0, len(engineData)-1):
        midpoint.append([(engineData[i][0] + engineData[i+1][0])/2.0, (engineData[i][1] + engineData[i+1][1])/2.0])
        height = midpoint[i][0] - engineData[i][0]
        width = engineData[i+1][1] - engineData[i][1]
        graphArea.append(height*width)
    return graphArea

def main():
    #open the file
    #read each line
    #parse
    #calculate
    file = open(filedialog.askopenfilename(), 'r')
    for line in file:
        parseString(line)
    print(engineData)
    getMaxThrust()
    print(maxThrust)
    getPropellantWeight();
    print(propellantWeight)
    getBurnTime();
    print(burnTime)
    #print(engineData)

main()
