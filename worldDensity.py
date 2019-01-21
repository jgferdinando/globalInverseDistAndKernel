from math import *
from tkinter import *
import random 
root = Tk()
canwidth = 1028
canheight = canwidth / 2
can = Canvas(root, width = canwidth, height = canheight, background = 'white')
projection = 'sinusoidal' #'mercator', 'sinusoidal', or 'equirectangular'
densityType = 'inverse square' #'inverse square' or 'kernel'
colorScheme = 'blue green' #'black', 'gray', 'blue green' or 'purple' or 'red'
class pointDensity(list):
    def __init__(self):
        self
    def addData(self, data):
        self.append(data)
    def genRandPoints(self): #generate random datasets for testing purposes
        i = 500
        j = 0
        while j <= i:
            lat = asin(random.random())*180/3.1415926
            lon = (random.random())*180
            randomPoint = [lat, lon]  
            #print randomPoint
            self.append(randomPoint)  
            j += 1
        j = 0
        while j <= i:
            lat = asin(random.random())*-180/3.1415926
            lon = (random.random())*180
            randomPoint = [lat, lon]  
            self.append(randomPoint)  
            j += 1
        j = 0
        while j <= i:
            lat = asin(random.random())*180/3.1415926
            lon = (random.random())*-180
            randomPoint = [lat, lon]  
            self.append(randomPoint)  
            j += 1
        j = 0
        while j <= i:
            lat = asin(random.random())*-180/3.1415926
            lon = (random.random())*-180
            randomPoint = [lat, lon]  
            self.append(randomPoint)  
            j += 1
    def plotData(self):
        pointSize = 1
        for datum in self:
            if projection =='sinusoidal':
                projecty = ((datum[0]-90)**2)**0.5 
                projectx = ((datum[1])*cos(datum[0]*3.1415926/180))+180
            elif projection == 'equirectangular':
                projecty = ((datum[0]-90)**2)**0.5
                projectx = datum[1]+180 
            elif projection == 'mercator':
                projecty = (((25*(log((1+sin(datum[0]*3.1415926/180))/(1-sin(datum[0]*3.1415926/180)))))-90)**2)**0.5
                projectx = ((datum[1]+180)/1.4) + 60
            else:
                quit
            y = ((projecty)/170)*canheight - 10 #y1
            x = ((projectx)/340)*canwidth - 20 #x1
            #y = 100 + ( 0.8 * y1 ) - (0.02 * datum[3])                  #y = -100 + ( 0.500 * x1 ) + ( 0.500 * y1 ) - (0.02 * datum[3])
            #x = -400 + (canwidth/2 - y1) + ( (y1**0.33) * x1 * 0.15 )   #x = 400 + ( 0.866 * x1 ) - ( 0.866 * y1 )
            dataBox = [ x,y+pointSize, x,y ] 
            if datum[3] < 10:
                can.create_line(dataBox,fill='#bc2918') 
            elif datum[3] < (216/3.25):
                can.create_line(dataBox,fill='#e8a7a0') 
            else:
                can.create_line(dataBox,fill='gray70')
    def densityPlot(self): 
        widthgrid = 200 #define the grid resolution here
        heightgrid = widthgrid/2
        searchRadius = 1000
        latinterval = 180.00/heightgrid
        loninterval = 360.00/widthgrid
        gridlat = 60
        gridlon = -120
        gridPointsList = []
        distanceScoreList = []
        while gridlat > -60:
            gridlon = -179
            while gridlon < 175:
                gridpoint = []
                gridpoint.append(gridlat)
                gridpoint.append(gridlon)
                distancescore = 0.00
                score = 0.0
                numer = 0.0
                denom = 0.0
                elevation = 0.0
                pi = 3.1415926
                neighborhood = 1000
                for datum in self:
                    planetradius = 63710
                    lat1 = gridlat
                    lat2 = datum[0]
                    lon1 = gridlon
                    lon2 = datum[1]
                    arcdistance = planetradius * acos( (sin(lat1*3.1415926/180)*sin(lat2*3.1415926/180)) + (cos(lat1*3.1415926/180)*cos(lat2*3.1415926/180)*cos((((lon1-lon2)*3.1415926/180)**2)**0.5)) )
                    if arcdistance < searchRadius: #and datum[3] > 67:
                        if densityType == 'kernel':
                            kern = (1.0/(searchRadius*len(self)))*((arcdistance/(searchRadius)))
                            distancescore += kern
                        elif densityType == 'inverse square':
                            distancescore += (1/((arcdistance**2)+1))*datum[2]
                        else:
                            quit
                    else:
                        distancescore = distancescore
                    if arcdistance < neighborhood:
                        weight = ( 1 / ( arcdistance**2 ) )
                        numer += ( weight * datum[3] )
                        denom += weight
                    else:
                        continue 
                elevation = numer / (denom+1)
                distanceScoreList.append(distancescore)
                gridpoint.append(distancescore)
                gridpoint.append(elevation)
                gridPointsList.append(gridpoint)
                gridlon += loninterval
            gridlat -= latinterval
        maxDistanceScore = max(distanceScoreList)
        for gridpoint in gridPointsList:
            adjustedScore = int(round(8 - (8*(gridpoint[2]**0.1)) / (maxDistanceScore**0.1) )  )
            if colorScheme == 'blue green':
                colors = ['#016c59','#02818a','#3690c0','#67a9cf','#a6bddb','#d0d1e6','#ece2f0','#fff7fb','white']
            elif colorScheme == 'red':
                colors = ['#b30000','#d7301f','#ef6548','#fc8d59','#fdbb84','#fdd49e','#fee8c8','#fff7ec','white']
            elif colorScheme == 'purple':
                colors = ['#4d004b','#810f7c','#88419d','#8c6bb1','#8c96c6','#9ebcda','#bfd3e6','#e0ecf4','#f7fcfd']
            elif colorScheme =='black':
                colors = ['black','white']
            elif colorScheme == 'gray':
                colors = []
                n = 99
                while n >= 0:
                    gray = 'gray{}'.format(n)
                    colors.append(gray)
                    n -= 2
            else:
                quit
            color = colors[adjustedScore]
            gridpoint.append(color)        
        for gridpoint in gridPointsList:
            if projection =='sinusoidal':
                projecty = ((gridpoint[0]-90)**2)**0.5 
                projectx = ((gridpoint[1])*cos(gridpoint[0]*3.1415926/180))+180            
            elif projection == 'mercator':
                projecty = (((25*(log((1+sin(gridpoint[0]*3.1415926/180))/(1-sin(gridpoint[0]*3.1415926/180)))))-90)**2)**0.5
                projectx = ((gridpoint[1]+180)/1.4) + 60
            elif projection == 'equirectangular':
                projecty = ((gridpoint[0]-90)**2)**0.5
                projectx = gridpoint[1]+180     
            else:
                quit
            ploty = ((projecty)/170)*canheight #y1
            plotx = ((projectx)/340)*canwidth #x1
            #below: plot equations for isometric view, declare y1 and x1 as variables in above two equations
            #ploty = -200 + ( 0.500 * x1 ) + ( 0.500 * y1 ) - (100 * (gridpoint[3]**2)**0.25)
            #plotx = 200 + ( 0.866 * x1 ) - ( 0.866 * y1 )
            gridSize = 1
            gridBox = [ plotx-gridSize,ploty+gridSize, plotx+gridSize,ploty+gridSize, plotx+gridSize,ploty-gridSize, plotx-gridSize,ploty-gridSize, plotx-gridSize,ploty+gridSize ] 
            can.create_line(gridBox,fill=gridpoint[4])  
            #print(gridpoint[4])
cities = pointDensity()
#cities.genRandPoints()
citiesText = open('cities.txt', 'r')
lines = citiesText.read().split(';\n')
for line in lines:
    city = [ float(line.split(',')[0]) , float(line.split(',')[1]) , float(line.split(',')[2]) , float(line.split(',')[3].strip(';',)) ]
    cities.addData(city)
citiesText.close()
#cities.plotData()
cities.densityPlot()
can.pack()
root.mainloop()
