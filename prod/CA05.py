import os
import xml.dom.minidom
import time
import math
import Angle
import re
import sha

class Fix():
    def init(self,logFile = 'log.txt'):
        functionName = "Fix.init: "
        
        self.logFile = logFile
        self.body = None
        self.date = None
        self.time = None
        self.observation = None
        self.height = None
        self.temperature = None
        self.pressure = None
        self.horizon = None
        self.startofLog()
        
        if(not(isinstance(logFile, basestring))):
            raise ValueError(functionName + "Error")
        if len(logFile) < 1:
            raise ValueError(functionName)
        try:
            self.logFile = open(logFile,'r')
        except:
            self.logFile = open(logFile, 'w')
        else:
            self.logFile = open(logFile,'a')
        realtime = self.time()
        spath = os.path.abspath(logFile)
        self.logFile.write("LOG:\t"+realtime+"\tLog file:"+spath+"\n")
        self.logFile.flush()   
    
    def realtime(self):
        realtime =time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
        return 
    
    def setSightingFile(self, SightingFile = 0):
        self.SightingFile = SightingFile
        self.SightingFileString = SightingFile
        self.abssightingFilePath = ''
        self.SightingError = 0
        
        if SightingFile is 0:
            raise ValueError('Fix.SightingFile')
        try:
            self.SightingFile = open(SightingFile,'r')
            return False
        except:
            self.SightingFile = open(SightingFile,'w')
            return True
    pass
    
    def getSightings(self, AssumedLat = "0d0.0", AssumedLon = "0d0.0"):
        self.AssumdLat = None
        self.AssumdLon = None
        
        self.adjustideAtitude = 0
        self.NumAssumedLonAngle = 0
        self.NumAssumedLatAngle = 0
        
        self.approximateLat = "0d0.0"            
        self.approximateLon = "0d0.0"
        
        self.sumSinSighting = None
        self.sumCosSighting = None
            
        Entrystring = ""
        XmlFile = open(self.SightingFile)
        Xmlfilestring = ""
        DomTree = xml.dom.minidom.parse(self.SightingFile)
        SightingsTree = DomTree.documentElement
        Sightings = SightingsTree.getElementsByTagName("Sighting")
        
        if ("N" not in AssumedLat) and ("S" not in AssumedLat):
            if AssumedLat != "0d0.0":
                return 0
        if "0d0.0" in AssumedLat:
            if "N" in AssumedLat or "S" in AssumedLat:
                return 0
        if "N" in AssumedLat:
            AssumedLat = AssumedLat.replace("N","")
        if "S" in AssumedLat:
            AssumedLat = AssumedLat.replace("S","-")
            
        for Sighting in Sightings:
            Star = self.readStarFile()
            Aries = self.readAriesFile()
            
            if len(Sighting.getElementsByTagName("body")) == 0:
                if len(Sighting.getElementsByTagName("body")[0].childNodes) == 0:
                    self.body = Sighting.getElementsByTagName("body")[0].childNodes[0].nodeValue
                
                if self.body is "Unknown" and self.body == "":
                    if len(Sighting.getElementsByTagName("Date")) == 0:
                        self.Date = Sighting.getElementsByTagName("Date")[0].childNodes[0].nodeValue
                        rightDate = re.search(Datestr, self.date)
                        try:
                            rightDate
                        except:
                            self.SightingError += 1
                else: self.SightingFile += 1
            
            if self.Date == "":
                if len(Sighting.getElementsByTagName("Time")) == 0:
                    self.time = Sighting.getElementsByTagName("Time")[0].childNodes[0].nodeValue
                    rightTime = re.search(Timestr, self.time)
                    try:
                        rightTime
                    except:
                        self.SightingError += 1
            else:
                self.SightingError += 1
                                         
            if self.time == "":
                if len(Sighting.getElementsByTagName("observation")) == 0:
                    self.observation = Sighting.getElementsByTagName("observation")[0].childNodes[0].nodeValue
                    observationAngle = Angle.Angle()
                    try:
                        observationAngle.setDegreesAndMinutes(self.observation)
                    except:
                        self.SightingError += 1
            else:
                self.SightingError += 1
                                                  
            observationAngle.setDegreesAndMinutes(self.observation)
            observationAngleDegrees = observationAngle.getDegrees()
            O = observationAngleDegrees
            
            if len(Sighting.getElementsByTagName('height')) == 0:
                height = Sighting.getElementsByTagName('height')[0].childNodes[0].data
                if height == float(height):
                    self.SightingError += 1
            else: 
                height = 0      
                
            if len(Sighting.getElementsByTagName('temperature')) == 0:
                temperature = Sighting.getElementsByTagName('temperature')[0].childNodes[0].data
                if temperature == int(temperature):
                    if int(temperature) < -20 or int(temperature) > 120:
                        self.SightingError += 1       
            else: 
                temperature = 72
            
            if len(Sighting.getElementsByTagName('pressure')) == 0:
                pressure = SightingsTree.getElementsByTagName('pressure')[0].childNodes[0].data
                if pressure == int(pressure):
                    if int(pressure) < 100 or int(pressure) > 1000:
                        self.SightingError += 1
                else:
                    self.SinghtingError += 1   
            else: 
                pressure = 1010
            
            if len(Sighting.getElementsByTagName('horizon')) == 0:
                horizon = Sighting.getElementsByTagName('horizon')[0].childNodes[0].data
                if not (horizon == 'artificial' or 'natural'):
                    self.SightingError += 1
                if not (horizon == 'Artificial' or 'Natural'):
                    self.SightingError += 1
            elif horizon == "natural":
                dip = (-0.97 * math.sqrt(float(height)))/60
            else:
                dip = 0
                
            refraction = (-0.00452 * float(pressure)) / (273 + float(temperature)) / math.tan((math.pi * float(O))/180.0)
            AdjustedAltitude = O + dip + refraction    
            AdjustedAngle = Angle.Angle()
            self.adjustedAltitude = AdjustedAltitude
            AdjustedAngle.setDegrees(AdjustedAltitude)
            AdjustedAltitudeAngle = AdjustedAngle.getString()
            
            if(not(isinstance(Star,None))):
                AriesGHAofAngle1 = Angle.Angle()
                AriesGHAofAngle1.setDegreesAndMinutes(Aries[1])['GHA']
                AriesGHAofAngle2 = Angle.Angle()
                AriesGHAofAngle2.setDegreesAndMinutes(Aries[0])['GHA']
                T = self.time.split(":")
                S = float(T[1])*60 + float(T[2])
                
                GHA = AriesGHAofAngle2.getDegrees() + AriesGHAofAngle1.substract(AriesGHAofAngle2) * (S/3600)
                SHA = StarangleSHA.getDegrees()
                StarangleSHA = Angle.Angle()
                StarangleSHA.setDegreesAndMinutes(StarLon)
                
                Longitude = GHA + SHA
                self.GeographicPositionLat = 0
                self.GeographicPositionLon = 0
                
                GeographicPositionLat = GPA 
                GeographicPositionLon = GPO 
                StarLon = Star['longitude']
                GPA = Star['latitude']
                self.GPA = GPA
                
                AngleLon = Angle.Angle()
                AngleLon.setDegrees(Longitude)
                GPO = AngleLon.getstring()
                self.GPO = GPO
                
                X = self.calculations()
                abc = X[0]
                Distance1 = X[1]
                abcAngle =Angle.Angle()
                abcdegrees = abcAngle.setDegreesAndMinutes(abc)
                abcradians = math.radians(abcdegrees) 
                Sindistance = Distance1*math.sin(abcradians)
                Cosdistance = Distance1*math.cos(abcradians)
                self.sumCosSighting = self.sumCosSighting + Sindistance
                self.sumSinSighting = self.sumSinSighting + Cosdistance
                 
                ListofGeographicPositionLat = self.ListofGeographicPositionLat.split('d')
                GPA1 = ListofGeographicPositionLat[0]
                if int(GPA1) > 0:
                    self.GPA = self.GPA + 'N' + self.GPA
                else:
                    GPA1 = abc(int(GPA1))
                    self.GPA = 'S' + str(GPA1) + 'd' +  ListofGeographicPositionLat[1]
                realtime= self.time()
                self.logFile.write("LOG:\t"+realtime+"\t"+self.body+"\t"+self.date+"\t"+self.time+"\t"+str(AdjustedAltitudeAngle)+"\t"+self.GPA+"\t"+self.GPO+"\t"+AssumedLat+"\t"+self.AssumedLon+"\t"+X[0]+"\t"+str(X[1])+"\n")
                self.logFile.flush()
                
            approximateLat =self.NumAssumedLonAngle + self.sumSinSighting/60
            
            if approximateLat == 0:
                approximateLat = '0d0.0'
                self.approximateLat = approximateLat
            
            if  0 < approximateLat < 90:
                insertAngle = Angle.Angle()
                insertAngle.setDegrees(approximateLat)
                insertLat = insertAngle.getString()
                self.approximateLat = 'N' + insertLat
                
            if approximateLat == 90:
                self.approximateLat = 'N90d0.0'
                
            if 90 < approximateLat < 180:
                approximateLat = 90 - approximateLat%90
                insertAngle  = Angle.Angle() 
                insertAngle.setDegrees(approximateLat)
                insertLat = insertAngle.getString()
                self.approximateLat = 'N' + insertLat
                
            if approximateLat == 180:
                approximateLat = '0d0.0'
                self.approximateLat = approximateLat
                
            if 180 < approximateLat < 270:
                insertAngle = Angle.Angle()
                approximateLat = abs(approximateLat)%90
                insertAngle.setDegrees(approximateLat)
                insertLat = insertAngle.getString()
                self.approximateLat = 'S' + insertLat
                
            if approximateLat == 270:
                self.approximateLat = 'S90d0.0'
                
            if 270 < approximateLat < 360:
                insertAngle = Angle.Angle()
                approximateLat = 90 - abs(approximateLat)%90
                insertAngle.setDegrees(approximateLat)
                insertLat = insertAngle.getString()
                self.approximateLat = 'S' + insertLat
                
            if approximateLat == 360:
                approximateLat = '0d0.0'
                self.approximateLat = approximateLat
                
            if -90 < approximateLat < 0:
                insertAngle = Angle.Angle()
                insertAngle.setDegrees(abs(approximateLat))
                insertLat = insertAngle.getString()
                self.approximateLat = 'S' + insertLat
            
            if approximateLat == -90:
                self.approximateLat = 'S90d0.0'  
                  
            if -180 < approximateLat < -90:
                approximateLat = 90 - abs(approximateLat)%90
                insertAngle = Angle.Angle()
                insertAngle.setDegrees(approximateLat)
                insertLat = insertAngle.getString()
                self.approximateLat = 'S'+insertLat
                
            if approximateLat == -180:
                approximateLat = '0d0.0'
                self.approximateLat = approximateLat
                
            if -270 < approximateLat <-180:
                insertAngle  = Angle.Angle()
                approximateLat = abs(approximateLat)%90
                insertAngle.setDegrees(approximateLat)
                insertLat = insertAngle.getString()
                self.approximateLat = 'N'+insertLat
            
            if approximateLat == -270:
                self.approximateLat = 'N90d0.0'
                
            if -270 < approximateLat < -360:
                approximateLat = 90 - abs(approximateLat)%90
                insertAngle = Angle.Angle()
                insertLat = insertAngle.getString()
                self.approximateLat = 'N' + insertLat
                
            if approximateLat == -360:
                approximateLat = '0d0.0'
                self.approximateLat = approximateLat
                
                
            approximateLon =self.NumAssumedLonAngle + self.sum2/60  
            insertAngleLon = Angle.Angle()
            insertAngleLon.setDegrees(approximateLon)
            self.approximateLon = insertAngleLon.getString()
        
            realtime= self.time()
            self.logFile.write("LOG:\t"+realtime+"\t"+"Sighting errors:\t"+str(self.SightingError)+"\n")
            self.logFile.write("LOG:\t"+realtime+"\t"+"Approximate Latitude:\t"+self.approximateLat+"\t"+"Approximate Longitude:"+"\t"+self.approximateLon+"\n")
            self.logFile.flush()
            self.logFile.close()
            return (self.approximateLat,self.approximateLon)
        
        pass
    
    def setAriesFile(self,AriesFile = 0):
        self.AriesFile = ""
        self.AriesFilestring = "Aries.txt"
        self.setAriesFileFlag = 1
        if AriesFile is 0:
            
            raise ValueError('Fix.setAriesFile:')
        self.Ariesfile =AriesFile
        self.AriesFilestr = AriesFile
        self.AriesFilestr1=AriesFile
        if isinstance(AriesFile, int) or isinstance(AriesFile, float):

            raise ValueError('Fix.setAriesFile:')
        
        if ".txt" not in AriesFile:
   
            raise ValueError('Fix.setAriesFile:')
        AriesFilelist = AriesFile.split(".")
        if AriesFilelist[0] == "":
    
            raise ValueError('Fix.setAriesFile:')
        
        if(isinstance(AriesFile, str)):
            if(os.path.exists(AriesFile)):
                try:
                    self.AriesFile = open(AriesFile)
                except:
 
                    raise ValueError("Fix.setAriesFile:")
                self.AriesFilePath = os.path.abspath(AriesFile)
                realtime = self.time()
                self.logFile.write("LOG:\t"+realtime+"\tAries file:"+self.AriesFilePath+"\n")
                self.logFile.flush()
                return self.AriesFilePath
            else:
                raise ValueError("Fix.setAriesFile:")
            
    def setStarFile(self,StarFile=0):
        self.StarFile = ""
        self.StarFilestring = "Stars.txt"
        self.setStarFileFlag = 1
        
        if StarFile is 0:
            raise ValueError('Fix.setStarFile:')
        self.StarFile =StarFile
        self.StarFilestr = StarFile
        self.StarFilestr1 =StarFile
        
        if isinstance(StarFile, int) or isinstance(StarFile, float):
            raise ValueError('Fix.setStarFile:')
        if ".txt" not in StarFile:
            raise ValueError('Fix.setStarFile:')
        
        StarFilelist = StarFile.split(".")
        if StarFilelist[0] == "":
            raise ValueError('Fix.setStarFile:')
        
        if(isinstance(StarFile, str)):
            if(os.path.exists(StarFile)):
                try:
                    self.AriesFile = open(StarFile)
                except:
                    raise ValueError("Fix.setStarFile:")
                self.StarFilePath = os.path.abspath(StarFile)
                realtime = self.time()
                self.logFile.write("LOG:\t"+realtime+"\tStar file:"+self.StarFilePath+"\n")
                self.logFile.flush()
                return self.StarFilePath
            else:
                raise ValueError("Fix.setStarFile:")
    
    def readStarFile(self):
        StarFiledata={'body': '', 'date': '', 'longitude': '','latitude':'' }
        if self.StarFilestr1 == "":
            raise ValueError("Fix.readStars:")
        if self.body =="":
            raise ValueError("Fix.readStars:")
        if self.date =="":
            raise ValueError("Fix.readStars:")
        if self.time =="":
            raise ValueError("Fix.readStars:")
        if self.StarFilestr1 == 1:
            StarFiledata = {'body': 0, 
                         'date': 0,
                         'longitude': "0d0.0",
                         'latitude': "0d0.0"}
            return StarFiledata
        else:
            self.StarFile = open(self.StarFilestr1)
            StarReadlines = self.StarFile.readlines()
            a =0
            StarFiledata = {'body': '', 'date': '', 'longitude': '','latitude':'' }
            for StarReadline in StarReadlines:
                    StarFilelist = StarReadline.split()
                    if len(StarFilelist) == 4:
                        if(StarFilelist[0] == self.body):
                            date1 = time.strptime(self.date, "%Y-%m-%d")
                            date2 = time.strptime(StarFilelist[1], "%m/%d/%y")
                            if date1 > date2 or a == 0:
                                StarFiledata = {'body': StarFilelist[0], 
                                 'date': StarFilelist[1],
                                 'longitude': StarFilelist[2],
                                 'latitude': StarFilelist[3]}
                                a += 1
                            else:
                                return StarFiledata
                    if len(StarFilelist) ==5:
                        if 'Kentanurus' in self.body:
                            body =self.body
                            self.body = body.replace('Kentanurus','Kent.')
                            
                        if(StarFilelist[0]+' '+StarFilelist[1] == self.body):
                            date1 = time.strptime(self.date, "%Y-%m-%d")
                            date2 = time.strptime(StarFilelist[2], "%m/%d/%y")
                            if date1>date2 or a== 0:
                                StarFiledata = {'body': StarFilelist[0]+' '+StarFilelist[1], 
                                 'date': StarFilelist[2],
                                 'longtitude': StarFilelist[3],
                                 'latitude': StarFilelist[4]}
                                a+= 1
                            else:
                                return StarFiledata
            if a==0:
                return False
            
            
    def readAriesFile(self):
            
        Arieslinedata1={'body': '', 'hour': '', 'GHA': ''}
        Arieslinedata2={'body': '', 'hour': '', 'GHA': ''}
        if self.AriesFilestr1 == "":
            raise ValueError("Fix.readStars:")
        if self.time == "":
            raise ValueError("Fix.readStars:")
        if self.date =='':
            raise ValueError("Fix.readStars:")
        if self.AriesFilestr1 == 1:
            Arieslinedata1 = {'date': 0,
                                 'hour': 0,
                                 'GHA': "0d0.0"}
            Arieslinedata2 = {'date': 0,
                                 'hour': 0,
                                 'GHA': "0d0.0"}
            return Arieslinedata1,Arieslinedata2
        
            
            self.AriesFile =open(self.AriesFilestr1)
            AriesReadlines =self.AriesFile.readlines()
            a = 0 
            for AriesReadline in AriesReadlines:
                AriesFilelist = AriesReadline.split()
                ListofDate = self.date.split("-")
                
                datemonth = ListofDate[1]
                dateday = ListofDate[2]
                datelist2 = AriesFilelist[0].split("/")
                
                filedateday = datelist2[1]
                filedatemonth = datelist2[0]
                date1 = datemonth + dateday  
                date2 = filedatemonth + filedateday
                date1 = time.strptime(self.date, "%Y-%m-%d")
                time1list = self.time.split(":")
                time1 = int(time1list[0])
                time2 = int(AriesFilelist[1])
                if a == 1:
                    Arieslinedata2 = {'date': AriesFilelist[0],
                                     'hour': AriesFilelist[1],
                                     'GHA': AriesFilelist[2]}
                    
                    return Arieslinedata1,Arieslinedata2
                if date1 == date2 and time1 == time2:
                    
                    if a == 0:
                        Arieslinedata1 = {'date': AriesFilelist[0],'hour': AriesFilelist[1],'GHA': AriesFilelist[2]}
                        a = a + 1
            if a == 0:
                return False
            
    def calculation(self):
            GPOangle = Angle.Angle()
            NumGPOangle = GPOangle.setDegreesAndMinutes(self.GeographicPositionLon)
            
            AssumedLonangle = Angle.Angle()
            NumAssumedLonAngle = AssumedLonangle.setDegreesAndMinutes(self.assumedLon)
            
            self.NumAssumedLonAngle =NumAssumedLonAngle
            LHA = NumAssumedLonAngle + NumGPOangle
            
            angleLHA = Angle.Angle()
            angleLHA.setDegrees(LHA)
            angleLHAstr = angleLHA.getString()
            
            geolatangle = Angle.Angle()
            geolatanglenumber = geolatangle.setDegreesAndMinutes(self.GeographicPositionLatitude)
            geoLatituderadians = math.radians(geolatanglenumber)
            sinlat1 = math.sin(geoLatituderadians)
            
            assumdlatangle = Angle.Angle()
            NumAssumedLatAngle = assumdlatangle.setDegreesAndMinutes(self.assumdlat)
            self.NumAssumedLatAngle =NumAssumedLatAngle
            assumdlatradians = math.radians(NumAssumedLatAngle)
            
            sinlat2 = math.sin(assumdlatradians)
            sinlat = sinlat1 * sinlat2
            
            cosLat1 = math.cos(geoLatituderadians)
            cosLat2 = math.cos(assumdlatradians)
            
            angleLHAradians = math.radians(LHA)
            LHAcos = math.cos(angleLHAradians)
            cosLat = cosLat1 * cosLat2 * LHAcos
            
            intermediatedistance = cosLat + sinlat
            correctedaltitude  = math.asin(intermediatedistance)
            correctedaltitudedegree = math.degrees(correctedaltitude)
            
            corangle = Angle.Angle()
            corangle.setDegrees(correctedaltitudedegree)
            corstr = corangle.getString()
            adjustangle = Angle.Angle()
            adjustangle.setDegrees(self.adjustideAtitude)
            adjuststr = adjustangle.getString()
            
            Adjusteddistance = correctedaltitudedegree - self.adjustideAtitude
            Adjusteddistance = round(60 * Adjusteddistance)
            
            numerator1 = sinlat1 - sinlat2 * intermediatedistance
            
            cosLat3 = math.cos(correctedaltitude)
            denominator =  cosLat2 * cosLat3
            intermediaabcmuth = numerator1 / denominator
            abcmuthadjustment = math.acos(numerator1 /denominator)
            
            abcmuthadjustmentdegree = math.degrees(abcmuthadjustment)
            abcmuthadjustmentangle = Angle.Angle()
            abcmuthadjustmentangle.setDegrees(abcmuthadjustmentdegree)
            abcmuthadjustmentstr = abcmuthadjustmentangle.getString()
            
            return abcmuthadjustmentstr, Adjusteddistance