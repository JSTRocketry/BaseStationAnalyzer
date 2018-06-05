import tkinter as tk
from tkinter import filedialog
BURN_TIME_TOLLERENCE = .03
GRAVITY = 9.81
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
    for i in engineData:
        if i[0] > maxThrust[0]:
            maxThrust = i

def getPropellantWeight():
    global propellantWeight
    propellantWeight = abs(engineData[0][0] - engineData[-1][0])

def getBurnTime():
    global burnTime
    for i in engineData:
        if abs(1 - (i[0]/engineData[-1][0])) <= BURN_TIME_TOLLERENCE:
            burnTime = i[1] - engineData[0][1]
            return

def convertToThrust():
    for i in engineData:
        i[0] *= GRAVITY

def getImpulse():
    area = 0
    for i in range(0,len(engineData)-1):
        midpoint = (engineData[i + 1][0] - engineData[i][0])/2.0 + engineData[i][0]
        tempArea = midpoint * (engineData[i+1][1] - engineData[i][1])/1000.0
        if(tempArea > 0):
            area += tempArea
    return area

def parseString(line):
    weightIndex = line.index("@{")
    timeIndex = line.index(";")
    endLine = line.index("}@")
    weight = line[(weightIndex + 2):timeIndex]
    time = line[(timeIndex + 1):endLine-1]
    engineData.append([float(weight), float(time)])

def main():
    file = open(filedialog.askopenfilename(), 'r')
    for line in file:
        parseString(line)
    getPropellantWeight();
    print("Propellant Weight: " + str(propellantWeight))
    convertToThrust()
    getMaxThrust()
    print("Max Thrust: " + str(maxThrust[0]) + " Newtons At Time: " + str(maxThrust[1]))
    getBurnTime();
    print("Burn time: " + str(burnTime))
    print("Total Impulse: " + str(getImpulse()))

main()
