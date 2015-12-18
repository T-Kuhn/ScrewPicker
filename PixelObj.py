from FCab import JsonDump
import math
import string

# - - - - - - - - - - - - - - - - 
# - - - - PIXELOBJ CLASS  - - - -
# - - - - - - - - - - - - - - - -
class PixelObj:
    def __init__(self, id_):
       self.XYset = set()
       self.id_ = id_
       self.numberOfPixels = 0
       self.coord_x = 0
       self.coord_y = 0
       self.coord_real_y = 0
       print "new object made with id: ", self.id_

    def checkXYset(self, nList):
        flag = False
        for entry in nList:
            if len(self.XYset) is 0:
                print "append"
                self.XYset.add(entry)
            if entry in self.XYset:
                flag = True
        if flag is True:
            for entry in nList:
                self.XYset.add(entry)
        return flag

    def countPixel(self):
        self.numberOfPixels = len(self.XYset)
        print "Object ID: ", self.id_
        print "Number of Pixels: ", self.numberOfPixels
    
    def computeMeanCoord(self):
        if len(self.XYset) is 0:
            return
        tmpX = 0
        tmpY = 0
        for ent in self.XYset:
            x, y = ent
            tmpX += x
            tmpY += y
        self.coord_x = int(tmpX / len(self.XYset))
        tmp = int(tmpY / len(self.XYset))
        self.coord_real_y = tmp
        self.coord_y = 96 - tmp
        
        print "X coord: ", self.coord_x
        print "Y coord: ", self.coord_y
