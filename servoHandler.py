import sys
from time import sleep
import time
import math
sys.path.append("..")
from ax12 import ax12
from select import select

# - - - - - - - - - - - - - - - - 
# - - - ERROR HANDLING CLASS  - -
# - - - - - - - - - - - - - - - -
class errorHandler(Exception): pass

# - - - - - - - - - - - - - - - - 
# - - - SERVOHANDLER CLASS  - - -
# - - - - - - - - - - - - - - - -
class servoHandler:
    
    def __init__(self, servID, rampT, servoObj):
        self.rampTime_ms = rampT
        self.servoID = servID
        self.speed = 0
        self.currentPos = 0
        self.maxSpeed = 300
        self.currentSpeed = 0
        self.moveDemanded = False
        self.endRampFlag = False
        self.firstCycleFlag = False
        self.endStageFlag = False
        self.passedTimeSinceStart = 0
        self.passedTimeSinceEnd = 0
        self.endPosDif = 0
        self.startPos = 0
        self.goalPos = None
        self.startTimeStamp = None
        self.ledMem = 0

        self.servo = servoObj
        self.initParam()
        #self.initValuesToEeprom()
    
    def initValuesToEeprom(self):
        self.servo.setStatusReturnLevel(self.servoID, 1)
        self.servo.setReturnDelayTime(self.servoID, 100)
    
    def initParam(self):
        self.servo.setCompliance(self.servoID, 1, 1, 120, 120) #softMode: 1, 1, 200, 200
        self.servo.setPunchLimit(self.servoID, 60)

    # - - - - - - - - - - - - - - - - 
    # - - TRY TO DO A READ METHOD - -
    # - - - - - - - - - - - - - - - -
    def tryToRead(self, func):
        tryToSend = True
        reSendCounter  = 0
        value = 0;
        while(tryToSend):
            tryToSend = False
            try:
                value = func(self.servoID)
            except:
                tryToSend = True
                print "Retry"
                reSendCounter += 1
                if(reSendCounter > 30):
                    e = "Timeout on servo " + str(self.servoID) + ". After " + str(reSendCounter) + " retries."
                    raise errorHandler(e)
        return value

    # - - - - - - - - - - - - - - - - 
    # - - - MOVE SMOOTH METHOD  - - -
    # - - - - - - - - - - - - - - - -
    def moveSmooth(self, goalP, speed):
        self.goalPos = goalP
        self.startTimeStamp = self.getTimeStamp_ms()
        self.startPos = self.tryToRead(self.servo.readPosition)
        self.moveDemanded = True
        self.firstcycleFlag = False
        self.endRampFlag = False
        self.maxSpeed = speed
    
    # - - - - - - - - - - - - - - - - 
    # - - - - UPDATE METHOD - - - - -
    # - - - - - - - - - - - - - - - -
    def update(self):
        if(self.moveDemanded):
            self.updateTime()
            self.currentPos = self.tryToRead(self.servo.readPosition)
            self.endPosDif = abs(self.goalPos - self.currentPos)
            self.startPosDif = abs(self.startPos - self.currentPos)
            if(self.endPosDif < 100 + self.maxSpeed * 0.5  and not self.endRampFlag and self.startPosDif > 10):  #330 for speed = 300
                self.currentSpeed = int(round(self.maxSpeed * math.sin(self.passedTimeSinceStart/(self.rampTime_ms*2.0)*math.pi)))
                self.endRampFlag = True
            if(self.passedTimeSinceStart <= self.rampTime_ms and not self.endRampFlag):
                self.speed = int(round(self.maxSpeed * math.sin(self.passedTimeSinceStart/(self.rampTime_ms*2.0)*math.pi)))
            elif(self.endRampFlag and not self.endStageFlag):
                if(not self.firstCycleFlag):
                    print "start EndRamp!"
                    if(self.passedTimeSinceStart <= self.rampTime_ms):
                        self.currentSpeed = int(round(self.maxSpeed * math.sin(self.passedTimeSinceStart/(self.rampTime_ms*2.0)*math.pi)))
                    else:
                        self.currentSpeed = self.maxSpeed
                    print "set current speed to: ", self.currentSpeed
                    self.endTimeStamp = self.getTimeStamp_ms()
                    self.firstCycleFlag = True
                self.passedTimeSinceEnd = abs(self.getTimeStamp_ms() - self.endTimeStamp - self.rampTime_ms)
                self.speed = int(round(self.currentSpeed * math.sin(self.passedTimeSinceEnd/(self.rampTime_ms*2.0)*math.pi)))
                if(self.speed <= 40):
                    self.endStageFlag = True
            elif(self.endStageFlag):
                self.speed = 40
            else:
                self.speed = self.maxSpeed
            #print "speed: ", self.speed
            #sleep(0.001)
            self.servo.moveSpeed(self.servoID, self.goalPos, 1 + self.speed)
            #self.servo.action()
        if(self.currentPos < self.goalPos + 15 and self.currentPos > self.goalPos - 15 and self.passedTimeSinceStart > 80):
            self.moveDemanded = False
            self.endRampFlag = False
            self.firstCycleFlag = False
            self.endStageFlag = False
        return self.moveDemanded
        
    # - - - - - - - - - - - - - - - - 
    # - - -  GET MS TIME STAMP  - - -
    # - - - - - - - - - - - - - - - -
    def getTimeStamp_ms(self):
        return int(time.time()*1000)

    # - - - - - - - - - - - - - - - - 
    # - - - UPDATE PASSED TIME  - - -
    # - - - - - - - - - - - - - - - -
    def updateTime(self):
        self.passedTimeSinceStart = self.getTimeStamp_ms() - self.startTimeStamp
    
    # - - - - - - - - - - - - - - - - 
    # - - - - GET POSITION  - - - - -
    # - - - - - - - - - - - - - - - -
    def getPosition(self):
        return self.tryToRead(self.servo.readPosition)

    # - - - - - - - - - - - - - - - - 
    # - - - - - INVERT LED  - - - - -
    # - - - - - - - - - - - - - - - -
    def invertLed(self):
        if self.ledMem is 0:
            self.ledMem = 1
        else:
            self.ledMem = 0
        self.servo.setLedStatus(self.servoID, self.ledMem)

    # - - - - - - - - - - - - - - - - 
    # - - - - - - SET LED - - - - - -
    # - - - - - - - - - - - - - - - -
    def setLed(self, val):
        self.servo.setLedStatus(self.servoID, val)





