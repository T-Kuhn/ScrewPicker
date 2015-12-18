import sys
from time import sleep
from random import random
import time
import math
sys.path.append("..")
from ax12 import ax12
from select import select
import RPi.GPIO as GPIO
import spidev
import os
from servoHandler import servoHandler
from switchObj import SwitchObj
import json
from ImPro import ImPro
from FCab import JsonDump
import numpy as np

# - - - - - - - - - - - - - - - - 
# - - - - - GPIO SETUP  - - - - -
# - - - - - - - - - - - - - - - -
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(6,GPIO.IN)
GPIO.setup(13,GPIO.IN)
GPIO.setup(19,GPIO.IN)
GPIO.setup(26,GPIO.IN)
GPIO.setup(12,GPIO.IN)
GPIO.setup(16,GPIO.IN)
GPIO.setup(20,GPIO.IN)

# - - - - - - - - - - - - - - - - 
# - - - GLOBAL OBJECTS  - - - - -
# - - - - - - - - - - - - - - - -

jD = JsonDump()

imageProObj = ImPro()

spi = spidev.SpiDev()
spi.open(0,0)
servos = ax12.Ax12()
switchObj = SwitchObj()

servoHandlerObj = [0]
servoHandlerObj.append(servoHandler(1, 500, servos))
servoHandlerObj.append(servoHandler(2, 500, servos))
servoHandlerObj.append(servoHandler(3, 500, servos))
servoHandlerObj.append(servoHandler(4, 500, servos))


# - - - - - - - - - - - - - - - - 
# - CHECK MOVE DEMANDED FLAGS - -
# - - - - - - - - - - - - - - - -
def checkMoveDemandedFlags(servoID):
    controlBit = False
    for i in range(len(servoID)):
        if(servoHandlerObj[servoID[i]].moveDemanded):
            return True
    return False

# - - - - - - - - - - - - - - - - 
# - - -  MOVE THEM SERVOS   - - -
# - - - - - - - - - - - - - - - -
def moveThemServos(servoID, pos, speed):
    if isinstance(servoID, list): 
        for index, servo_id in enumerate(servoID):
            servoHandlerObj[servo_id].moveSmooth(pos[index], speed[index])
        while checkMoveDemandedFlags(servoID):
            for i in servoID:
                servoHandlerObj[i].update()
            servos.action()
        sleep(0.1)
    else:
        servoHandlerObj[servoID].moveSmooth(pos, speed)
        while checkMoveDemandedFlags([servoID]):
            servoHandlerObj[servoID].update()
        servos.action()
        sleep(0.1)

# - - - - - - - - - - - - - - - - 
# - - -  SET TORQUE TO VAL  - - -
# - - - - - - - - - - - - - - - -
def setTorqueServos(servoID, val):
    for i in servoID:
        servos.setTorqueStatus(i, val)
    print "Torque set to ", val

# - - - - - - - - - - - - - - - - 
# - - - WAIT FOR USER RESP  - - -
# - - - - - - - - - - - - - - - -
def waitForUserResponce(string):
    tmp = raw_input(string)
    if(tmp is ""):
        return True
    else:
        return False

# - - - - - - - - - - - - - - - - 
# - - - - - - LEDS OFF  - - - - -
# - - - - - - - - - - - - - - - -
def LedsOff(servoID):
    for i in servoID:
        servoHandlerObj[i].setLed(0)


# - - - - - - - - - - - - - - - - 
# - - - - - INVERT LEDS - - - - -
# - - - - - - - - - - - - - - - -
def invertLeds(servoID):
    for i in servoID:
        servoHandlerObj[i].invertLed()

# - - - - - - - - - - - - - - - - 
# - - - - - INPUT CHECK - - - - -
# - - - - - - - - - - - - - - - -
def checkForInput():
    rlist, _, _, = select([sys.stdin], [], [], 0.1)
    if rlist:
        s = sys.stdin.readline()
        print s
        return s
    else:
        return "None"


# - - - - - - - - - - - - - - - - 
# - - - CAUTION LED BLINK - - - -
# - - - - - - - - - - - - - - - -
def cautionLedBlink():
    for i in [1,2,3,4]:
        servoHandlerObj[i].setLed(0)
    sleep(0.1)
    for _ in range(24):
        invertLeds([1,2,3,4])
        sleep(0.1)
    for i in [1,2,3,4]:
        servoHandlerObj[i].setLed(1)

# - - - - - - - - - - - - - - - - 
# - - UPDATE SERVO POS POTS - - -
# - - - - - - - - - - - - - - - -
def updateServoPosPots():
    if GPIO.input(13) is 1:
        moveThemServos([2], [readChannel(2)], [readChannel(0) + 1])
    if GPIO.input(19) is 1:
        moveThemServos([3], [readChannel(3)], [readChannel(0) + 1])
    if GPIO.input(26) is 1:
        moveThemServos([4], [readChannel(4)], [readChannel(0) + 1])
    if GPIO.input(6) is 1:
        moveThemServos([1], [readChannel(1)], [readChannel(0) + 1])

# - - - - - - - - - - - - - - - - 
# - - - - SAVE SERVO POS  - - - -
# - - - - - - - - - - - - - - - -
def saveServoPos(servoID):
    posList = []
    speedList = []
    idList = []
    switchObj.update()
    status_ = switchObj.checkStatus()

    while True:
        switchObj.update()
        updateServoPosPots()
        for id_ in servoID:
            if(id_ is 1 and GPIO.input(6) is 1):
                if id_ not in idList: 
                    idList.append(id_)
                    print "idList: ", idList

            if(id_ is 2 and GPIO.input(13) is 1):
                if id_ not in idList: 
                    idList.append(id_)
                    print "idList: ", idList

            if(id_ is 3 and GPIO.input(19) is 1):
                if id_ not in idList: 
                    idList.append(id_)
                    print "idList: ", idList

            if(id_ is 4 and GPIO.input(26) is 1 and not id_ in idList):
                if id_ not in idList: 
                    idList.append(id_)
                    print "idList: ", idList

            if(id_ is 55 and status_ is not switchObj.checkStatus() and not id_ in idList):
                sleep(0.1)
                GPIO.output(17, GPIO.input(12))
                idList.append(id_)
                print "idList: ", idList


        if(GPIO.input(20) is 1 and GPIO.input(6) is 0 and GPIO.input(13) is 0 and GPIO.input(19) is 0
                and GPIO.input(26) is 0):
            for _ in range(8):
                GPIO.output(21, 1)            
                sleep(0.1)
                GPIO.output(21, 0)
                sleep(0.1)

            for id_ in idList:
                if(id_ is not 55):
                    if id_ is 2:
                        speedList.append(readChannel(0))
                        posList.append(servoHandlerObj[id_].getPosition() + 4)
                    else:
                        speedList.append(readChannel(0))
                        posList.append(servoHandlerObj[id_].getPosition())
                else:
                    posList.append(GPIO.input(12))
            #imageProObj.blink()
            #imageProObj.captureFrame()
            return idList, posList, speedList    

# - - - - - - - - - - - - - - - - 
# - - - -  READ CHANNEL - - - - -
# - - - - - - - - - - - - - - - -
def readChannel(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

# - - - - - - - - - - - - - - - - 
# - SHUT DOWN AND WAIT FOR POKE -
# - - - - - - - - - - - - - - - -
def shutDown():
    positionList = [0, 1, 2, 3, 4]
    moveList = []
    moveList.append([[3, 2, 1, 4], [862, 100, 100, 512], [400, 200, 200, 200]])

    #get in pre shut down position
    for ent in moveList:
        tmp = False
        print "ent: ", ent
        servoID = ent[0]
        pos = ent[1]
        speed = ent[2]
        for index, id_ in enumerate(servoID):
            if id_ is 55:
                GPIO.output(17, pos[index])
                tmp = True
                sleep(0.2)
        if tmp is False:
            moveThemServos(servoID, pos, speed)

    setTorqueServos([1, 2, 3, 4], 0)
    LedsOff([1, 2, 3, 4])
    imageProObj.camera._set_led(False)
    sleep(1.0)
    for index, ent in enumerate(servoHandlerObj):
        if ent is not 0:
            positionList[index] = ent.getPosition()

    while True:
        sleep(0.5)
        for index, ent in enumerate(servoHandlerObj):
            if ent is not 0:
                tmp = ent.getPosition()
                if positionList[index] + 10 < tmp or positionList[index] - 10 > tmp:
                    print "movement!"
                    imageProObj.camera._set_led(True)
                    return True



# - - - - - - - - - - - - - - - - 
# - - - PICK UP ALGORITHM - - - -
# - - - - - - - - - - - - - - - -
def pickUpAlgorithm(number):
    '''Algorithm which contains all the things needed for
    looking up the screws, picking them up and putting them somewhere
    return True if there were objects
    return False if there was no object'''
    flag = False
    x_offset = [204, 358, 512, 666, 820]
    moveList = []
    newList = []

    #load some position arrays
    startposY = jD.load('startposY.txt')
    Ypos = jD.load('Ypos.txt')
    endpos = jD.load('endpos.txt')

    if number is 0:
        #This is the standard position
        moveList.append([[3, 2, 1], [0, 36, 203], [300, 300, 300]])
        
    #Here we got the robot on the right startposition on the X axis
    moveList.append([[4], [x_offset[number]], [300]])

    #Here we write the posture for frame taking (startpos Y axis)
    for ent in startposY:
        moveList.append(ent)

    #get in image taking position
    for ent in moveList:
        tmp = False
        print "ent: ", ent
        servoID = ent[0]
        pos = ent[1]
        speed = ent[2]
        for index, id_ in enumerate(servoID):
            if id_ is 55:
                GPIO.output(17, pos[index])
                tmp = True
                sleep(0.2)
        if tmp is False:
            moveThemServos(servoID, pos, speed)

    #reset moveList
    moveList = []
    y_vals = []
    x_vals = []

    #CAPTURE FRAME and GET PIXEL OBJECTS
    imageProObj.blink()
    imageProObj.captureFrame()

    print "nr. of obj in pixel obj list: ", len(imageProObj.pixelObjList)
    for ent in imageProObj.pixelObjList:
        if ent.numberOfPixels > 50:
            rounded_val = int(round((1.2*ent.coord_y)/10.0 - 0.5))
            if rounded_val > 11:
                rounded_val = 11
            if (number <= 1 and rounded_val <= 2) :
                print "skip"
            else:
                flag = True
                print "rounded thing: ", rounded_val
                y_vals.append(rounded_val)
                tmp = np.arctan(1.0*(ent.coord_x - 24)/ent.coord_y)
                print "tmp: ", tmp
                x_vals.append(-int(195*tmp))
        print "numberOfPixels: ", ent.numberOfPixels
        print "coord_x: ", ent.coord_x
        print "coord_y: ", ent.coord_y

    if flag is False:
        return False

    #get the robot to GOALPOS on X axis!
    for index, ent in enumerate(x_vals):
        moveList.append([[4], [x_offset[number] + ent], [200]])
        #this is to get to the GOALPOS on the Y axis!
        for entry in Ypos[y_vals[index]]:
            moveList.append(entry)

        moveList.append([[3, 2, 1], [612, 36, 203], [300, 300, 300]])

        #ENDPOS
        for e in endpos:
            moveList.append(e)

        #standard position
        moveList.append([[3, 2, 1, 4], [0, 36, 203, x_offset[number]], [300, 300, 300, 300]])



    #write positiondata in list
    #while GPIO.input(20) is 0:
    #    sleep(0.1)
    #    result = saveServoPos([1, 2, 3, 4, 55])
    #    moveList.append(result)
    #    newList.append(result)
    #    print moveList

    #jD.dump(newList, 'newList.txt')


    #playback
    for ent in moveList:
        tmp = False
        print "ent: ", ent
        servoID = ent[0]
        pos = ent[1]
        speed = ent[2]
        for index, id_ in enumerate(servoID):
            if id_ is 55:
                GPIO.output(17, pos[index])
                tmp = True
                sleep(0.4)
        if tmp is False:
            moveThemServos(servoID, pos, speed)
    return True

# - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - 
# - - - MAIN PROG START - - - - -
# - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - 

while shutDown():
    cautionLedBlink()
    for i in range(5):
        while pickUpAlgorithm(i):
            print "doing the thing"    







