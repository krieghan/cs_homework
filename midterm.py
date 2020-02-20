import sys
import math

class GeomCalc:
    """This class gives us the ability to do mathematical operations using two or more objects.  In all
       cases with the exception of DotProduct, the return value will be an object.  DotProduct returns
       a scalar value."""

    def AddVector(self, vector1, vector2):
        return Vector(vector1.GetX() + vector2.GetX(), vector1.GetY() + vector2.GetY())
    
    def SubVector(self, vector1, vector2):
        return Vector(vector1.GetX() - vector2.GetX(), vector1.GetY() - vector2.GetY())
    
    def DotProduct(self, vector1, vector2):
        
        
        return (vector1.GetX() * vector2.GetX() + vector1.GetY() * vector2.GetY())

    def MultScalar(self, scalar, vector):
        return Vector(scalar * vector.GetX(), scalar * vector.GetY())
    
    def AddPointAndVector(self, point, vector):
        x = point.GetPosition(0) + vector.GetX()
        y = point.GetPosition(1) + vector.GetY()
        return Point([x, y])
    
    def SubPoints(self, point1, point2):
        x = point1.GetPosition(0) - point2.GetPosition(0)
        y = point1.GetPosition(1) - point2.GetPosition(1)
        return Vector(x, y)


class Point:
    """Class definition for our points.  A point has is pure-position, and thus is not capable of very much.
       A point's main contribution is for making lines.  Points have the ability to set and report their
       position."""
    	
    def __init__(self, pointlist = [0, 0]):
        
        self.x = pointlist[0]
        self.y = pointlist[1]
        return
	
    def GetPosition(self, index = -1):
        if index == -1:
            return [self.x, self.y]
        if index == 0:
            return self.x
        if index == 1:
            return self.y
            #Error:
        print "Unrecognizable index given for Point.GetPosition()" 		
	
	
	
    def SetPosition(self, point, index = -1):
        if index == -1:
            self.x = point[0]
            self.y = point[1]
            return 1
		
        if index == 0:
            self.x = point
            return 1
		
        if index == 1:
            self.y = point
            return 1
		
        #Error:
        print "Unrecognizable index given for Point.SetPosition()"

        
class Line:
    """Since this project is based on shapes, lines are very important.  A line has the ability to return
       its true distance, or the distance in either the X or Y direction.  It can also give its angle in 
       relation to the X-Axis, and to return its Normal Perp Vector.  A line also has the ability to
       set its position"""
    
    geomcalc = GeomCalc()
    
    def __init__(self, point1 = [0, 0], point2 = [0, 0]):
        self.point = [None, None]
        self.point[0] = Point(point1)
        self.point[1] = Point(point2)
        
    def GetPoint(self, pointindex = -1):
        if pointindex == -1:
            return [self.point[0], self.point[1]]
        else:
            return self.point[pointindex]
        
        
    def SetPosition(self, point1, point2):
            self.point[0].SetPosition(point1)
            self.point[1].SetPosition(point2)
		
    def GetPosition(self, pointindex, coordinateindex = -1):
        if pointindex == -1:
            return [self.point[0].GetPosition(coordinateindex), self.point[1].GetPosition(coordinateindex)]
	
        if pointindex == 0 or pointindex == 1:
            return self.point[pointindex].GetPosition(coordinateindex)
		
        #Error:
        print "Error in given point index for Line.GetPosition()"
		
    def GetDeltaX(self):
        return point[1].GetPosition(0) - point[0].GetPosition(0)
	
    def GetDeltaY(self):
        return point[1].GetPosition(1) - point[0].GetPosition(1)
	
    def GetDistance(self):
        return math.sqrt(math.pow(self.GetDeltaX, 2) + math.pow(self.GetDeltaY, 2))
	
    def GetTheta(self):
        return math.degrees(math.arctan2(self.GetDeltaY(), self.GetDeltaX()))
    
    def FindNormalPerpVector(self):
        """Having a line return its normal perp vector is vital if we are to do the calculations 
        necessary for this project"""
        
        x = self.point[1].GetPosition(0) - self.point[0].GetPosition(0)
        y = self.point[1].GetPosition(1) - self.point[0].GetPosition(1)
        
        temp = x
        x = -y
        y = temp
        
        newvector = Vector(x, y)
        newvector.Normalize()
        return newvector
        

        
class Vector:
    """Vectors are vital for specifying rays.  A vector has the ability to set its X or Y value, or its direction
       or magnitude (updates must be made with these changes).  A vector also has the ability to return its 
       normalized counterpart."""
    	
    def __init__(self, vectorx, vectory):
        self.direction = 0
        self.magnitude = 0
        self.vectorx = vectorx
        self.vectory = vectory
        self.__AdjustDirectionAndMagnitude()
        
        
	
    def __AdjustDirectionAndMagnitude(self):
        self.magnitude = math.sqrt(math.pow(self.vectorx, 2) + math.pow(self.vectory, 2))
        self.direction = math.degrees(math.atan2(self.vectory, self.vectorx))
    
    def __AdjustXAndY(self):
        self.vectorx = self.magnitude * math.cos(math.radians(self.direction))
        self.vectory = self.magnitude * math.sin(math.radians(self.direction))
    
    def GetX(self):
        return self.vectorx
       
    def GetY(self):
        return self.vectory
    
    def GetDirection(self):
        return self.direction
	
    def GetMagnitude(self):
        return self.magnitude                

    def SetVector(self, x, y):
        self.vectorx = x
        self.vectory = y
        self.__AdjustDirectionAndMagnitude()
    
    def SetX(self, x):
        self.vectorx = x
        self.__AdjustDirectionAndMagnitude()
    
    def SetY(self, y):
        self.vectory = y
        self.__AdjustDirectionAndMagnitude()
        
        
    def SetDirection(self, direction):
        self.direction = direction
        self.__AdjustXAndY()
    
    def SetMagnitude(self, magnitude):
        self.magnitude = magnitude
        self.__AdjustXAndY()			
    
    def Normalize(self):
        self.SetMagnitude(1)
    
    def GetNormalized(self, vector):
        newvector = Vector(self.vectorx, self.vectory)
        newvector.SetMagnitude(1)
        return newvector

        
        
def PrintAnswer(dotproducts):        
    for i in dotproducts:
        if i > 0:
            print "Concave"
            return
    
    print "Convex"        
        
polygon = []
normals = []
dotproducts = []

geomcalc = GeomCalc()
        
f = open(sys.argv[1], 'r')

i = 0
k = 1
temp = []
lines = f.readlines()
numsides = int(lines[0])            
            
while i < numsides:
 
    temp.append(map(int, lines[k].split()))
 
                
    i += 1
    k += 1
            
for m in range(len(temp)):
    polygon.append(Line(temp[m], temp[(m + 1) % len(temp)]))

for i in polygon:
    normals.append(i.FindNormalPerpVector())

for i in range(len(normals)):
    j = i + 1
    while j < len(normals):
        dotproducts.append(round(geomcalc.DotProduct(normals[i], normals[j])))
        j += 1

PrintAnswer(dotproducts)        


        
        
        
    
    

    