'''
Based on Jesse Merritt's script:
https://github.com/jes1510/python_dynamixels

and Josue Alejandro Savage's Arduino library:
http://savageelectronics.blogspot.it/2011/01/arduino-y-dynamixel-ax-12.html
'''

from time import sleep
from serial import Serial
import RPi.GPIO as GPIO

class Ax12:
    # important AX-12 constants
    # /////////////////////////////////////////////////////////// EEPROM AREA
    AX_MODEL_NUMBER_L = 0
    AX_MODEL_NUMBER_H = 1
    AX_VERSION = 2
    AX_ID = 3
    AX_BAUD_RATE = 4
    AX_RETURN_DELAY_TIME = 5
    AX_CW_ANGLE_LIMIT_L = 6
    AX_CW_ANGLE_LIMIT_H = 7
    AX_CCW_ANGLE_LIMIT_L = 8
    AX_CCW_ANGLE_LIMIT_H = 9
    AX_SYSTEM_DATA2 = 10
    AX_LIMIT_TEMPERATURE = 11
    AX_DOWN_LIMIT_VOLTAGE = 12
    AX_UP_LIMIT_VOLTAGE = 13
    AX_MAX_TORQUE_L = 14
    AX_MAX_TORQUE_H = 15
    AX_RETURN_LEVEL = 16
    AX_ALARM_LED = 17
    AX_ALARM_SHUTDOWN = 18
    AX_OPERATING_MODE = 19
    AX_DOWN_CALIBRATION_L = 20
    AX_DOWN_CALIBRATION_H = 21
    AX_UP_CALIBRATION_L = 22
    AX_UP_CALIBRATION_H = 23

    # ////////////////////////////////////////////////////////////// RAM AREA
    AX_TORQUE_STATUS = 24
    AX_LED_STATUS = 25
    AX_CW_COMPLIANCE_MARGIN = 26
    AX_CCW_COMPLIANCE_MARGIN = 27
    AX_CW_COMPLIANCE_SLOPE = 28
    AX_CCW_COMPLIANCE_SLOPE = 29
    AX_GOAL_POSITION_L = 30
    AX_GOAL_POSITION_H = 31
    AX_GOAL_SPEED_L = 32
    AX_GOAL_SPEED_H = 33
    AX_TORQUE_LIMIT_L = 34
    AX_TORQUE_LIMIT_H = 35
    AX_PRESENT_POSITION_L = 36
    AX_PRESENT_POSITION_H = 37
    AX_PRESENT_SPEED_L = 38
    AX_PRESENT_SPEED_H = 39
    AX_PRESENT_LOAD_L = 40
    AX_PRESENT_LOAD_H = 41
    AX_PRESENT_VOLTAGE = 42
    AX_PRESENT_TEMPERATURE = 43
    AX_REGISTERED_INSTRUCTION = 44
    AX_PAUSE_TIME = 45
    AX_MOVING = 46
    AX_LOCK = 47
    AX_PUNCH_L = 48
    AX_PUNCH_H = 49

    # /////////////////////////////////////////////////////////////// Status Return Levels
    AX_RETURN_NONE = 0
    AX_RETURN_READ = 1
    AX_RETURN_ALL = 2

    # /////////////////////////////////////////////////////////////// Instruction Set
    AX_PING = 1
    AX_READ_DATA = 2
    AX_WRITE_DATA = 3
    AX_REG_WRITE = 4
    AX_ACTION = 5
    AX_RESET = 6
    AX_SYNC_WRITE = 131

    # /////////////////////////////////////////////////////////////// Lengths
    AX_RESET_LENGTH = 2
    AX_ACTION_LENGTH = 2
    AX_ID_LENGTH = 4
    AX_LR_LENGTH = 4
    AX_SRL_LENGTH = 4
    AX_RDT_LENGTH = 4
    AX_LEDALARM_LENGTH = 4
    AX_SHUTDOWNALARM_LENGTH = 4
    AX_TL_LENGTH = 4
    AX_VL_LENGTH = 6
    AX_AL_LENGTH = 7
    AX_CM_LENGTH = 6
    AX_CS_LENGTH = 5
    AX_COMPLIANCE_LENGTH = 7
    AX_CCW_CW_LENGTH = 8
    AX_BD_LENGTH = 4
    AX_TEM_LENGTH = 4
    AX_MOVING_LENGTH = 4
    AX_RWS_LENGTH = 4
    AX_VOLT_LENGTH = 4
    AX_LOAD_LENGTH = 4
    AX_LED_LENGTH = 4
    AX_TORQUE_LENGTH = 4
    AX_POS_LENGTH = 4
    AX_GOAL_LENGTH = 5
    AX_MT_LENGTH = 5
    AX_PUNCH_LENGTH = 5
    AX_SPEED_LENGTH = 5
    AX_GOAL_SP_LENGTH = 7

    # /////////////////////////////////////////////////////////////// Specials
    AX_BYTE_READ = 1
    AX_INT_READ = 2
    AX_ACTION_CHECKSUM = 250
    AX_BROADCAST_ID = 254
    AX_START = 255
    AX_CCW_AL_L = 255
    AX_CCW_AL_H = 3
    AX_LOCK_VALUE = 1
    LEFT = 0
    RIGTH = 1
    RX_TIME_OUT = 10
    TX_DELAY_TIME = 0.00002    #0.00002

    # RPi constants
    RPI_DIRECTION_PIN = 18
    RPI_DIRECTION_TX = GPIO.HIGH
    RPI_DIRECTION_RX = GPIO.LOW
    RPI_DIRECTION_SWITCH_DELAY = 0.000001   #0.000001

    # static variables
    port = None
    gpioSet = False

    def __init__(self):
        if(Ax12.port == None):
            Ax12.port = Serial("/dev/ttyAMA0", baudrate=1000000, timeout=0.001)
        if(not Ax12.gpioSet):
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(Ax12.RPI_DIRECTION_PIN, GPIO.OUT)
            Ax12.gpioSet = True
        self.direction(Ax12.RPI_DIRECTION_RX)

    connectedServos = []

    # Error lookup dictionary for bit masking
    dictErrors = {  1 : "Input Voltage",
            2 : "Angle Limit",
            4 : "Overheating",
            8 : "Range",
            16 : "Checksum",
            32 : "Overload",
            64 : "Instruction"
            }

    # Custom error class to report AX servo errors
    class axError(Exception) : pass

    # Servo timeout
    class timeoutError(Exception) : pass

    def direction(self,d):
        GPIO.output(Ax12.RPI_DIRECTION_PIN, d)
        sleep(Ax12.RPI_DIRECTION_SWITCH_DELAY)


    def readDataSimple(self):
        self.direction(Ax12.RPI_DIRECTION_RX)
        print Ax12.port.read()

    def readData(self,id):
        self.direction(Ax12.RPI_DIRECTION_RX)
        sleep(0.00001)   #0.0006
        reply = Ax12.port.read(5) # [0xff, 0xff, origin, length, error]
        try:
            assert ord(reply[0]) == 0xFF
        except:
            e = "Timeout on servo " + str(id)
            raise Ax12.timeoutError(e)

        try :
            length = ord(reply[3]) - 2
            error = ord(reply[4])

            if(error != 0):
                print "Error from servo: " + Ax12.dictErrors[error] + ' (code  ' + hex(error) + ')'
                return -error
            # just reading error bit
            elif(length == 0):
                return error
            else:
                if(length > 1):
                    reply = Ax12.port.read(2)
                    returnValue = (ord(reply[1])<<8) + (ord(reply[0])<<0)
                else:
                    reply = Ax12.port.read(1)
                    returnValue = ord(reply[0])
                return returnValue
        except Exception, detail:
            raise Ax12.axError(detail)

    def ping(self,id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_READ_DATA + Ax12.AX_PING))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_READ_DATA)
        outData += chr(Ax12.AX_PING)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def factoryReset(self,id, confirm = False):
        if(confirm):
            self.direction(Ax12.RPI_DIRECTION_TX)
            Ax12.port.flushInput()
            checksum = (~(id + Ax12.AX_RESET_LENGTH + Ax12.AX_RESET))&0xff
            outData = chr(Ax12.AX_START)
            outData += chr(Ax12.AX_START)
            outData += chr(id)
            outData += chr(Ax12.AX_RESET_LENGTH)
            outData += chr(Ax12.AX_RESET)
            outData += chr(checksum)
            Ax12.port.write(outData)
            sleep(Ax12.TX_DELAY_TIME)
            return self.readData(id)
        else:
            print "nothing done, please send confirm = True as this fuction reset to the factory default value, i.e reset the motor ID"
            return

    def setID(self, id, newId):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_ID_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_ID + newId))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_ID_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_ID)
        outData += chr(newId)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def setBaudRate(self, id, baudRate):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        br = ((2000000/long(baudRate))-1)
        checksum = (~(id + Ax12.AX_BD_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_BAUD_RATE + br))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_BD_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_BAUD_RATE)
        outData += chr(br)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def setStatusReturnLevel(self, id, level):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_SRL_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_RETURN_LEVEL + level))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_SRL_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_RETURN_LEVEL)
        outData += chr(level)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        #return self.readData(id)

    def setReturnDelayTime(self, id, delay):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_RDT_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_RETURN_DELAY_TIME + (int(delay)/2)&0xff))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_RDT_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_RETURN_DELAY_TIME)
        outData += chr((int(delay)/2)&0xff)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        #return self.readData(id)

    def lockRegister(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_LR_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_LOCK + Ax12.AX_LOCK_VALUE))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_LR_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_LOCK)
        outData += chr(Ax12.AX_LOCK_VALUE)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        #return self.readData(id)

    def move(self, id, position):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        p = [position&0xff, position>>8]
        checksum = (~(id + Ax12.AX_GOAL_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_GOAL_POSITION_L + p[0] + p[1]))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_GOAL_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_GOAL_POSITION_L)
        outData += chr(p[0])
        outData += chr(p[1])
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        #return self.readData(id)

    def moveSpeed(self, id, position, speed):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        p = [position&0xff, position>>8]
        s = [speed&0xff, speed>>8]
        checksum = (~(id + Ax12.AX_GOAL_SP_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_GOAL_POSITION_L + p[0] + p[1] + s[0] + s[1]))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_GOAL_SP_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_GOAL_POSITION_L)
        outData += chr(p[0])
        outData += chr(p[1])
        outData += chr(s[0])
        outData += chr(s[1])
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        #return self.readData(id)

    def moveRW(self, id, position):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        p = [position&0xff, position>>8]
        checksum = (~(id + Ax12.AX_GOAL_LENGTH + Ax12.AX_REG_WRITE + Ax12.AX_GOAL_POSITION_L + p[0] + p[1]))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_GOAL_LENGTH)
        outData += chr(Ax12.AX_REG_WRITE)
        outData += chr(Ax12.AX_GOAL_POSITION_L)
        outData += chr(p[0])
        outData += chr(p[1])
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        #return self.readData(id)

    def moveSpeedRW(self, id, position, speed):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        p = [position&0xff, position>>8]
        s = [speed&0xff, speed>>8]
        checksum = (~(id + Ax12.AX_GOAL_SP_LENGTH + Ax12.AX_REG_WRITE + Ax12.AX_GOAL_POSITION_L + p[0] + p[1] + s[0] + s[1]))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_GOAL_SP_LENGTH)
        outData += chr(Ax12.AX_REG_WRITE)
        outData += chr(Ax12.AX_GOAL_POSITION_L)
        outData += chr(p[0])
        outData += chr(p[1])
        outData += chr(s[0])
        outData += chr(s[1])
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        #return self.readData(id)

    def action(self):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(Ax12.AX_BROADCAST_ID)
        outData += chr(Ax12.AX_ACTION_LENGTH)
        outData += chr(Ax12.AX_ACTION)
        outData += chr(Ax12.AX_ACTION_CHECKSUM)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        self.direction(Ax12.RPI_DIRECTION_RX)
        sleep(Ax12.TX_DELAY_TIME)

    def setTorqueStatus(self, id, status):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        ts = 1 if ((status == True) or (status == 1)) else 0
        checksum = (~(id + Ax12.AX_TORQUE_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_TORQUE_STATUS + ts))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_TORQUE_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_TORQUE_STATUS)
        outData += chr(ts)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        #return self.readData(id)

    def setLedStatus(self, id, status):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        ls = 1 if ((status == True) or (status == 1)) else 0
        checksum = (~(id + Ax12.AX_LED_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_LED_STATUS + ls))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_LED_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_LED_STATUS)
        outData += chr(ls)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        #return self.readData(id)

    def setTemperatureLimit(self, id, temp):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_TL_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_LIMIT_TEMPERATURE + temp))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_TL_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_LIMIT_TEMPERATURE)
        outData += chr(temp)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def setVoltageLimit(self, id, lowVolt, highVolt):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_VL_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_DOWN_LIMIT_VOLTAGE + lowVolt + highVolt))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_VL_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_DOWN_LIMIT_VOLTAGE)
        outData += chr(lowVolt)
        outData += chr(highVolt)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def setAngleLimit(self, id, cwLimit, ccwLimit):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        cw = [cwLimit&0xff, cwLimit>>8]
        ccw = [ccwLimit&0xff, ccwLimit>>8]
        checksum = (~(id + Ax12.AX_AL_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_CW_ANGLE_LIMIT_L + cw[0] + cw[1] + ccw[0] + ccw[1]))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_AL_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_CW_ANGLE_LIMIT_L)
        outData += chr(cw[0])
        outData += chr(cw[1])
        outData += chr(ccw[0])
        outData += chr(ccw[1])
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def setTorqueLimit(self, id, torque):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        mt = [torque&0xff, torque>>8]
        checksum = (~(id + Ax12.AX_MT_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_MAX_TORQUE_L + mt[0] + mt[1]))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_MT_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_MAX_TORQUE_L)
        outData += chr(mt[0])
        outData += chr(mt[1])
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def setPunchLimit(self, id, punch):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        p = [punch&0xff, punch>>8]
        checksum = (~(id + Ax12.AX_PUNCH_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_PUNCH_L + p[0] + p[1]))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_PUNCH_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_PUNCH_L)
        outData += chr(p[0])
        outData += chr(p[1])
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        #return self.readData(id)

    def setCompliance(self, id, cwMargin, ccwMargin, cwSlope, ccwSlope):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_COMPLIANCE_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_CW_COMPLIANCE_MARGIN + cwMargin + ccwMargin + cwSlope + ccwSlope))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_COMPLIANCE_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_CW_COMPLIANCE_MARGIN)
        outData += chr(cwMargin)
        outData += chr(ccwMargin)
        outData += chr(cwSlope)
        outData += chr(ccwSlope)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        #return self.readData(id)

    def setLedAlarm(self, id, alarm):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_LEDALARM_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_ALARM_LED + alarm))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_LEDALARM_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_ALARM_LED)
        outData += chr(alarm)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def setShutdownAlarm(self, id, alarm):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_SHUTDOWNALARM_LENGTH + Ax12.AX_WRITE_DATA + Ax12.AX_ALARM_SHUTDOWN + alarm))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_SHUTDOWNALARM_LENGTH)
        outData += chr(Ax12.AX_WRITE_DATA)
        outData += chr(Ax12.AX_ALARM_SHUTDOWN)
        outData += chr(alarm)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def readTemperature(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_TEM_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_PRESENT_TEMPERATURE + Ax12.AX_BYTE_READ))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_TEM_LENGTH)
        outData += chr(Ax12.AX_READ_DATA)
        outData += chr(Ax12.AX_PRESENT_TEMPERATURE)
        outData += chr(Ax12.AX_BYTE_READ)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def readPosition(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_POS_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_PRESENT_POSITION_L + Ax12.AX_INT_READ))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_POS_LENGTH)
        outData += chr(Ax12.AX_READ_DATA)
        outData += chr(Ax12.AX_PRESENT_POSITION_L)
        outData += chr(Ax12.AX_INT_READ)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def readVoltage(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_VOLT_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_PRESENT_VOLTAGE + Ax12.AX_BYTE_READ))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_VOLT_LENGTH)
        outData += chr(Ax12.AX_READ_DATA)
        outData += chr(Ax12.AX_PRESENT_VOLTAGE)
        outData += chr(Ax12.AX_BYTE_READ)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def readSpeed(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_SPEED_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_PRESENT_SPEED_L + Ax12.AX_INT_READ))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_SPEED_LENGTH)
        outData += chr(Ax12.AX_READ_DATA)
        outData += chr(Ax12.AX_PRESENT_SPEED_L)
        outData += chr(Ax12.AX_INT_READ)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def readLoad(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_LOAD_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_PRESENT_LOAD_L + Ax12.AX_INT_READ))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_LOAD_LENGTH)
        outData += chr(Ax12.AX_READ_DATA)
        outData += chr(Ax12.AX_PRESENT_LOAD_L)
        outData += chr(Ax12.AX_INT_READ)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def readMovingStatus(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_MOVING_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_MOVING + Ax12.AX_BYTE_READ))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_MOVING_LENGTH)
        outData += chr(Ax12.AX_READ_DATA)
        outData += chr(Ax12.AX_MOVING)
        outData += chr(Ax12.AX_BYTE_READ)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)

    def readRWStatus(self, id):
        self.direction(Ax12.RPI_DIRECTION_TX)
        Ax12.port.flushInput()
        checksum = (~(id + Ax12.AX_RWS_LENGTH + Ax12.AX_READ_DATA + Ax12.AX_REGISTERED_INSTRUCTION + Ax12.AX_BYTE_READ))&0xff
        outData = chr(Ax12.AX_START)
        outData += chr(Ax12.AX_START)
        outData += chr(id)
        outData += chr(Ax12.AX_RWS_LENGTH)
        outData += chr(Ax12.AX_READ_DATA)
        outData += chr(Ax12.AX_REGISTERED_INSTRUCTION)
        outData += chr(Ax12.AX_BYTE_READ)
        outData += chr(checksum)
        Ax12.port.write(outData)
        sleep(Ax12.TX_DELAY_TIME)
        return self.readData(id)


    def learnServos(self,minValue=1, maxValue=6, verbose=False) :
        servoList = []
        for i in range(minValue, maxValue + 1):
            try :
                temp = self.ping(i)
                servoList.append(i)
                if verbose: print "Found servo #" + str(i)
                time.sleep(0.1)

            except Exception, detail:
                if verbose : print "Error pinging servo #" + str(i) + ': ' + str(detail)
                pass
        return servoList


#
#def playPose() :
#    '''
#    Open a file and move the servos to specified positions in a group move
#    '''
#    infile=open(Arguments.playpose, 'r')    # Open the file
#    poseDict = {}                           # Dictionary to hold poses and positions
#    if Arguments.verbose : print "Reading pose from", Arguments.playpose
#    for line in infile.readlines() :        # Read the file and step through it
#        servo = int(line.split(':')[0])     # Servo is first
#        position = int(line.split(':')[1])  # Position is second
#        poseDict[servo]=position            # add the servo to the Dictionary
#
#    groupMove2(poseDict)
#
#
#
#def writePose() :
#    '''
#    Read the servos and save the positions to a file
#    '''
#    of = open(Arguments.savepose, 'w')      # open the output file
#    pose = getPose2(connectedServos)        # get the positions
#    if Arguments.verbose :
#        print "Servo Positions"
#        print "---------------"
#
#    for key in  pose.keys():                # step through the keys, writing to the file
#        if Arguments.verbose : print "Servo " + str(key), pose[key]
#        of.write(str(key) + ':' + str(pose[key]) + '\n')    # Write to the file
#
#    if Arguments.verbose :
#        print "Wrote pose to " + Arguments.savepose
#        print
#
#    of.close()      # close the file
#
