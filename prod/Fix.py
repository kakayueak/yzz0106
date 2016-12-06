from xml.dom.minidom import parse
import xml.dom.minidom
import Angle




class Fix():
    def __init__(self, logFile = "logFile.txt"):
        fuctionName = "Fix._init_"
        self.approximateLatitude = "0d0.0"
        self.approximateLongitude = "0d0.0"
        
        self.logFile = logFile
        self.Startoflog()
        self.
        self.date = None
        self.time = None
        self.observation = None
        self.height = None
        self.temperature = None
        self.horizon = None
        self.AriesFile = 0
        self.
        
        
        if (not(isinstance(logFile,basestring))):
            raise ValueError(fuctionName + "Error")
        if len(longfile) < 1:
            raise ValueError(functionName)
        try:
            self.logFile = open(logFile,'r')
        except:
            self.logFile = open(logFile, 'w')
    pass
    
    def setSightingFile(self, SightingFile = 0):
        self.SightingFile = SightingFile
        self.StartofSightingFile()
        
        if SightingFile is 0:
            raise ValueError('Fix.SightingFile')
        try:
            self.SightingFile = open(SightingFile,'r')
            return False
        except:
            self.SightingFile = open(SightingFile,'w')
            return True
    pass
    
    
    def getSightings(self, AssumedLatitude = "0d0.0", AssumedLongtitude = "0d0.0"):
        AssumedLatitudeDegree = self.AssumedLatitude
        
        HeadersOfSightings = "LOG"
        DateAndTime = ""
        EntryOfSightings = ""
        DomTree = xml.dom.minidom.parse(self.SightingFile)
        SightingsTree = DomTree.documentElement
        Sightings = SightingsTree.getElementsByTagName(self.SightingFile)
        
        for Sighting in Sightings:
            date = SightingsTree.getElementsByTagName('date')[0]
            print date.childNodes[0].data
            
            time = SightingsTree.getElementsByTagName('time')[0]
            print time.childNodes[0].data
            
            if(not(len(SightingsTree.getElementsByTagName('height')[0].childNodes))) == 0:
                height = SightingsTree.getElementsByTagName('height')[0]
                print height.childNodes[0].data 
            else: height = 0
            
            if(not(len(SightingsTree.getElementsByTagName('temperature')[0].childNodes))) == 0:
                temperature = SightingsTree.getElementsByTagName('temperature')[0]
                print temperature.childNodes[0].data 
            else: temperature = 72
            
            if(not(len(SightingsTree.getElementsByTagName('pressure')[0].childNodes))) == 0:
                pressure = SightingsTree.getElementsByTagName('pressure')[0]
                print pressure.childNodes[0].data 
            else: pressure = 1010
            
            if(not(len(SightingsTree.getElementsByTagName('horizon')[0].childNodes))) == 0:
                horizon = SightingsTree.getElementsByTagName('horizon')[0]
                print horizon.childNodes[0].data 
            else: horizon = "natural"
                
        approximateLatitude ="0d0.0"
        approximateLongtitude = "0d0.0"
        return (self.approximateLatitude,self.approximateLongtitude)
        
        pass
    
    def setAriesFile(self, AriesFile = "AriesFile"):
        self.AriesFilestring = AriesFile
        entrystring = ""
        
        if (not(isinstance(AriesFile,str))):
            raise ValueError("Input Error")
        
        try:
            self.AriesFile = open(AriesFile,'r')
        except:
            raise ValueError()
        pass
    
        
    
        
    def setStarFile(self, StarFile = "StarFile"): 
        self.StarFilestring = StarFile
        entrystring = ""  
        
        if (not(isinstance(StarFile,str))):
            raise ValueError("Input Error")
        
        try:
            self.StarFile = open(StarFile,'r')
        except:
             raise ValueError()
        pass
    
    
    def getGHA(self):
    
     
    
    
    
         
    
         
        

        
        
    