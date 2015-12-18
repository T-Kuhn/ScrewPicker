import RPi.GPIO as GPIO

# - - - - - - - - - - - - - - - - 
# - - - SWITCH OBJ CLASS  - - - -
# - - - - - - - - - - - - - - - -
class SwitchObj:
    def __init__(self):
        self.flag1 = False
        self.flag2 = False
        self.flag3 = False
        self.status = False
        GPIO.output(17, 0)

    def update(self):
        if(GPIO.input(4) is 1 and not self.flag1):
            self.flag1 = True
            GPIO.output(17, 1)
            self.status = True
            print "it`s on!"
        if(GPIO.input(4) is 1 and self.flag2 and not self.flag3):
            GPIO.output(17, 0)
            self.status = False
            self.flag3 = True
        if(GPIO.input(4) is 0 and self.flag3):
            self.flag1 = False
            self.flag2 = False
            self.flag3 = False
        if(GPIO.input(4) is 0 and self.flag1):
            self.flag2 = True
        
        if(GPIO.input(12) is 1):
            self.status = True
        if(GPIO.input(12) is 0):
            self.status = False
             
    def checkStatus(self):
        return self.status

    def setOutput(self, val):
        GPIO.output(17, val)
        




