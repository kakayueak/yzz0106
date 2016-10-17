from math import degrees

class Angle():
    def __init__(self):
        self.angle = 0 
        pass
    print
    def setDegrees(self, degrees):
        if (not(isinstance(degrees,int))):
            raise ValueError("Input Error")
        else:
            if 0 <= degrees <= 360:
                degrees = degrees
            else:
                if degrees >360 and degrees <0:
                    degrees = degrees%360
                    pass
                print
            
    
    def setDegreesAndMinutes(self, degrees, minutes):
        if (not(isinstance(degrees,int))):
            raise ValueError("Input Error")
        else: 
            degrees.split("d")
            degrees = degrees[0]
            minutes = minutes[0]
            self.degrees =degrees%360 + minutes/60
            pass
        print
    
    def add(self, angle):
        if (not(isinstance(angle,int))):
            raise ValueError("Input Error")
        else:
            self.degrees = self.degrees + angle.degrees
            self.setdegrees(self.getdegrees)
            pass
        print
    
    def subtract(self, angle):
        if (not(isinstance(angle,int))):
            raise ValueError("Input Error")
        else:
            self.degrees = self.degrees - angle.degrees
            self.setdgrees(self.getdegrees)
        pass
    print
    
    def compare(self, angle):
        if (not(isinstance(angle,int))):
            raise ValueError("Input Error")
        else:
            if self.degress > angle.degrees:
                print -1
            if self.degrees == angle.degrees:
                print 0 
            if self.degrees < angle.degrees:
                print 1        
        pass
    print
    
    def getString(self):
        self.string = self.degrees + self.minutes * 60
        pass
    print
    
    def getDegrees(self):
        return self.degrees
        pass
    print