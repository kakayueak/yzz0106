from math import degrees

class Angle():
    def __init__(self):
        self.angle = 0 
        pass
    
    def setDegrees(self, degrees):
        self.degrees = degrees
        if (not(isinstance(degrees,int))):
            raise ValueError("Error in setDegrees")
        if (not(isinstance(degrees, float))):
            raise ValueError("Error in setDegrees")
        else:
            if 0 <= degrees <= 360:
                degrees = degrees
            else:
                if degrees >360 or degrees < -360:
                    degrees = degrees%360
                else: 
                    if 0 < degrees <= -360:
                        degrees = degrees + 360
                        return    
                pass
    
    def setDegreesAndMinutes(self, degrees, minutes):
        if(isinstance(degrees,basestring)):

            try:
                degreeslist = degrees.split('d')
            except:
                raise ValueError('Angle.setDegreesAndMinutes:')
            if (len(degreeslist)== 2):
                D = degreeslist[0]
                M = degreeslist[1]
                try:
                    D = int(D)
                except:
                    raise ValueError('Angle.setDegreesAndMinutes:')
                try:
                    M = float(M)
                except:
                    raise ValueError('Angle.setDegreesAndMinutes:')
                if (D is not None and D !=''):
                    if (M is not None and M !='' and M >=0):
                        M_list = str(M).split('.')
                        if len(M_list)==1:
                            pass
                        elif len(M_list)==2:
                            M_1 = int(M_list[1]) 
                        if 0<= M_1 <= 9: 
                            D_degrees= int(D)
                            D = int(D)
                            if D >= 0 and D < 360:
                                D = D 
                            elif D <0 and D>= -360:
                                D = abs(D) 
                            elif D >= 360:
                                D = D % 360
                            elif D< -360:
                                D =  D% 360    
                            M = float(M)
                            M = M/60
                            degrees = abs(int(D))+float(M)
                            degrees = float(degrees)
                            if D_degrees < 0 and D_degrees > -360:
                                degrees = 360 -degrees 
                            self.setDegrees(degrees)
                            return self.degrees
                        else:
                            raise ValueError('Angle.setDegreesAndMinutes:')
                    else:
                        raise ValueError('Angle.setDegreesAndMinutes:')
            else:
                raise ValueError('Angle.setDegreesAndMinutes:')
        else:
            raise ValueError('Angle.setDegreesAndMinutes:')       
            
            return
    
    def add(self, angle=0):
        if (not(isinstance(angle,Angle))):
            raise ValueError("Error in Angle.add")
        else:
            self.degrees = self.degrees + angle.degrees
            self.setdegrees(self.getdegrees)
            
        pass
    
    def subtract(self, angle):
        if (not(isinstance(angle,Angle))):
            raise ValueError("Error in Angle.subtract")
        else:
            self.degrees = self.degrees - angle.degrees
            self.setdgrees(self.getdegrees)
        pass
    
    def compare(self, angle):
        if (not(isinstance(angle,Angle))):
            raise ValueError("Error in Angle.compare")
        else:
            if self.degress > angle.degrees:
                print 1
            if self.degrees == angle.degrees:
                print 0 
            if self.degrees < angle.degrees:
                print -1        
        pass
    
    def getString(self):
        angleDegreeint = int(self.degrees)
        angleMinuteFloat = self.degrees - angleDegreeint
        angleMinute = round(angleMinuteFloat*60,1)
        angleString = str(angleDegreeint)+ "d" + str(angleMinute)
        
        pass
    
    def getDegrees(self):
        return self.degrees
        pass