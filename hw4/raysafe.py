"""
C. Andrews 2006

"""

import wx
from wx.glcanvas import GLCanvas
#from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math


class GeomCalc:

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
        x = self.point[1].GetPosition(0) - self.point[0].GetPosition(0)
        y = self.point[1].GetPosition(1) - self.point[0].GetPosition(1)
        
        temp = x
        x = -y
        y = temp
        
        newvector = Vector(x, y)
        #newvector.Normalize()
        return newvector
        

        
class Vector:

    	
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
    
    

        
class Ray:
	
    def __init__(self, point1 = [0, 0], point2 = [0, 0]):
        self.point1 = Point([point1[0], point1[1]])
        self.point2 = Point([point2[0], point2[1]])
        
        vectorx = point2[0] - point1[0]
        vectory = point2[1] - point1[1]
        self.vector = Vector(vectorx, vectory)
        self.speed = self.vector.GetMagnitude()
    
    def GetPoint(self):
        return self.point1
    
    def GetVector(self):
        return self.vector
    
    def GetSpeed(self):
        return self.speed
    
    def SetPoint(self, x, y):
        self.point1.SetPosition([x, y])
    
    def SetVector(self, x, y):
        self.vector.SetVector(x, y)
    
    def SetSpeed(self, speed):
        self.speed = speed
        self.vector.SetMagnitude(speed)
		



class CollisionLine(Line):

    def __init__(self, point1 = [0, 0], point2 = [0, 0]):       
        self.bound = 0
        Line.__init__(self, point1, point2)
        
    def SetBound(self, bound = 0):
        self.bound = bound
    
    def GetBound(self):
        return self.bound
    
    def GetCollisionTime(self, ray):                
        #if self.geomcalc.DotProduct(self.FindNormalPerpVector(), ray.vector) == 0:
        #    print "parallel"
        #    return -1
            
        answer = self.geomcalc.DotProduct(self.FindNormalPerpVector(), self.geomcalc.SubPoints(self.point[0], ray.point1)) / self.geomcalc.DotProduct(self.FindNormalPerpVector(), ray.vector)
        return answer


class ColoredRay(Ray):
   
    def __init__(self, point1 = [0, 0], point2 = [0, 0], red = 0, green = 0, blue = 0):
        Ray.__init__(self, point1, point2)
        self.currentlength = 0
        self.red = red
        self.blue = blue
        self.green = green
        self.geomcalc = GeomCalc()
        self.finaltime = -1
        
    def GetColor(self):
        return [self.red, self.green, self.blue]
    
    def SetColor(self, red, green, blue):
        self.red = red
        self.blue = blue
        self.green = green
    
    def UpdateLength(self):
        self.currentlength += self.speed
	
    def GetEndPoint(self, time):            
        endpoint = self.geomcalc.AddPointAndVector(self.point1, self.geomcalc.MultScalar(time, self.geomcalc.SubPoints(self.point2, self.point1)))
        return [endpoint.GetPosition(0), endpoint.GetPosition(1)]

        
class Polygon:
	    
    def __init__(self, linelist = []):
        
        self.lines = []
        for i in linelist:
            self.lines.append(CollisionLine(i[0], i[1]))
        
        
    
    def GetLines(self):
        return self.lines

    def SetLines(self, linelist = []):
        self.lines = linelist
    
    def FindBoundaries(self):
        left = right = self.lines[0].GetPosition(0, 0)
        top = bottom = self.lines[0].GetPosition(0, 1)
        
                
        for i in self.lines:
            if i.GetPosition(0, 0) < left:
                left = i.GetPosition(0, 0)
            if i.GetPosition(0, 0) > right:
                right = i.GetPosition(0, 0)
            if i.GetPosition(0, 1) < bottom:
                bottom = i.GetPosition(0, 1)
            if i.GetPosition(0, 1) > top:
                top = i.GetPosition(0, 1)
        
        return [left, right, top, bottom]
        


class Arena(Polygon):
    def __init__(self, linelist = []):
        Polygon.__init__(self, linelist)
    
    
class Pillar(Polygon):
    def __init__(self, linelist = []):
        Polygon.__init__(self, linelist)

        
class GLArena(GLCanvas):
    

    
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we can properly initialize the canvas"""
	
        self.arena = None
        self.pillar = []
        self.temppoint = []
        self.ray = []
        self.currentray = None
        self.geomcalc = GeomCalc()
        self.nexttime = -1
        self.nextline = None
        self.t = 0
        GLCanvas.__init__(self, parent,-1)
        self.init = 0

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.HandleClick)
        self.Bind(wx.EVT_TIMER, self.HandleTime)
        self.timer = wx.Timer(self)
        self.timer.Start(100)
      	return

    
    
    
    def SetupView(self):	    
        """This function does the actual work to setup the window so we can draw in it. We'll explain this in more detail later.
        """
        self.clientsize = self.GetClientSizeTuple()
       
        if self.arena is None:
            self.worldleft = 5
            self.worldright = 10
            self.worldbottom = 5
            self.worldtop = 10
        else:            
            [self.worldleft, self.worldright, self.worldtop, self.worldbottom] = self.arena.FindBoundaries()
       
       
        self.worldheight = self.worldtop - self.worldbottom
        self.worldwidth = self.worldright - self.worldleft
                               
	
        
        
        #The ratio of the width to the height in the client-area
        screenratio = float(self.clientsize[0]) / float(self.clientsize[1])
        
        ratio = self.worldwidth / self.worldheight
        #Should seem familiar, since we did it in class...
        if ratio > screenratio:
        
            self.viewport_left = 0
            self.viewport_bottom = (self.clientsize[1] - (self.clientsize[0] / ratio)) / 2
            self.viewport_width = self.clientsize[0]
            self.viewport_height = self.clientsize[0] / ratio
            
            
        if ratio < screenratio:
        
            self.viewport_left = (self.clientsize[0] - self.clientsize[1] * ratio) / 2
            self.viewport_bottom = 0
            self.viewport_width = self.clientsize[1] * ratio
            self.viewport_height = self.clientsize[1]
        
        self.viewport_right = self.viewport_left + self.viewport_width
        self.viewport_top = self.viewport_bottom + self.viewport_height
        
        #glViewport(0, 0, self.clientsize[0], self.clientsize[1])
        
        glViewport(self.viewport_left, self.viewport_bottom, self.viewport_width, self.viewport_height)
         
        #I need to find an appropriate border value.  It's scaled by the client-area because the world-window zooms, thus skewing any normal border given.
        if self.worldwidth == 0 or self.worldheight == 0:
            self.xborder = 1
            self.yborder = 1
        else:
            self.xscale = self.clientsize[0] / self.worldwidth
            self.xborder = 10 / self.xscale
            self.yscale = self.clientsize[1] / self.worldheight
            self.yborder = 10 / self.yscale
            
            self.worldleft -= self.xborder
            self.worldright += self.xborder
            self.worldtop += self.yborder
            self.worldbottom -= self.yborder
            
            self.worldheight = self.worldtop - self.worldbottom
            self.worldwidth = self.worldright - self.worldleft
            
            
	
           
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(self.worldleft, self.worldright, self.worldbottom, self.worldtop)


	
    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. Again, we'll describe this in more detail later.
        """
        self.SetCurrent()
        glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
        
        glEnable(GL_TEXTURE_2D)
        self.SetupView()
        return



    def OnPaint(self,event):
        """This function is called when the canvas recieves notice that it needs to repaint its surface. This just makes sure that OpenGL is inited and passes the work off to another function.
        """
        dc = wx.PaintDC(self)
        if not self.init:
            self.InitGL()
            self.init = 1
        self.OnDraw()
	return

    def OnSize(self,event):
        """ This function is called when a resize event occurs. The primary
        purpose for this is to readjust the viewport appropriately.
        """
        self.SetupView()    
        if self.init:
            self.OnDraw()
        event.Skip()


    def OnDraw(self):
        """This is the main drawing function. We will put all of our OpenGL drawing calls in here. If we want to force a repaint, this is the function that should be called. Note that this should always start by calling SetCurrent() and end by calling SwapBuffers().
        """
        self.SetCurrent()
     
        glClear(GL_COLOR_BUFFER_BIT)
                                          
        if self.arena != None:
            glBegin(GL_LINE_LOOP)
            glColor3f(1.0, 1.0, 1.0)
            for lines in self.arena.GetLines():
                [point1x, point1y] = lines.GetPosition(0)
                [point2x, point2y] = lines.GetPosition(1)
                glVertex2f(point1x, point1y)
                glVertex2f(point2x, point2y)
        
        
            glEnd()
        
        
            for pillar in self.pillar:
                glBegin(GL_LINE_LOOP)
                for lines in pillar.GetLines():
                    [point1x, point1y] = lines.GetPosition(0)
                    [point2x, point2y] = lines.GetPosition(1)
                    glVertex2f(point1x, point1y)
                    glVertex2f(point2x, point2y)
                glEnd()


#	            if self.temppoint != []:
#	    	 glBegin(GL_POINTS)
#	    	 glVertex2f(self.temppoint[0][0], self.temppoint[0][1])
#                   glEnd()
	
        
        if self.currentray is not None:        
            glBegin(GL_LINES)
            [red, green, blue] = self.currentray.GetColor()
            glColor3f(red, green, blue)
	
            [x, y] = [self.currentray.GetPoint().GetPosition(0), self.currentray.GetPoint().GetPosition(1)]
            glVertex2f(x, y)
            
            
            [x, y] = self.currentray.GetEndPoint(self.t)
            
            glVertex2f(x, y)
	
            glEnd()
        
        for i in self.ray:
            glBegin(GL_LINES)
            [red, green, blue] = i.GetColor()
            glColor3f(red, green, blue)
            
            [x, y] = [i.GetPoint().GetPosition(0), i.GetPoint().GetPosition(1)]
            glVertex(x, y)
            [x, y] = i.GetEndPoint(i.finaltime)
            glVertex2f(x, y)
            glEnd()
			
 
        self.SwapBuffers()
 
        return
    
    def DoDisplay(self, filename, numreflections):
              
        f = open(filename, 'r')
        
        temp = []
        polylines = []
        j = 0
        k = 1
        lines = f.readlines()
        
        
        numsides = int(lines[0])
        
        while k < len(lines):
            
            i = 0
            
            while i < numsides:
 
                temp.append(map(int, lines[k].split()))
 
                
                i += 1
                k += 1
            
           
            
            for m in range(len(temp)):
                polylines.append([temp[m], temp[(m + 1) % len(temp)]])
            
            
            
            if j == 0:
                self.arena = Arena(polylines)
            else:
                self.pillar.append(Pillar(polylines))
            
            j += 1
            polylines = []
            temp = []
            if k < len(lines):
                numsides = int(lines[k])
                k += 1
        self.ray = []
            
        self.SetupView()
        self.OnDraw()
        
        

 


    def HandleClick(self, event):
        if len(self.ray) < 1 and self.arena is not None:
            
            #If the click isn't in the viewport, I can't do anything with it.  Without an arena, I am in much the same
            #situation
	    
            if event.GetX() >= self.viewport_left and event.GetX() <= self.viewport_right: 
                if self.clientsize[1] - event.GetY() <= self.viewport_top and self.clientsize[1] - event.GetY() >= self.viewport_bottom:                                
                    self.temppoint.append(self.GiveWorldXY(event.GetX(), event.GetY()))
                    
            if len(self.temppoint) >= 2:
                self.currentray = ColoredRay(self.temppoint[1], self.temppoint[0], 0, 0, 1)                                              
                [self.nexttime, self.nextline] = self.GenerateCollisionTimes()
                
                
                                
                
		self.temppoint = []
        self.t = 0
        self.OnDraw()
        event.Skip()
        return
            
    
    def GiveWorldXY(self, x, y):
        """Our conversion function.  Here, we must convert from canvas coordinates (which is how the
        click is expressed) to viewport coordinates and then to world coordinates."""

        self.clientsize = self.GetClientSizeTuple()

        yscale = float(self.worldheight) / float(self.viewport_height)

        xscale = float(self.worldwidth) / float(self.viewport_width)



        return [(x - self.viewport_left - self.xborder * 2) * xscale, (self.clientsize[1] - y - self.viewport_bottom - self.yborder * 4) * yscale]
    
    def HandleTime(self, event):
        if self.currentray is not None and self.nextline is not None:
            
            self.t += self.currentray.GetSpeed()
            
            if self.t >= self.nexttime:
                
                excess = self.nexttime - self.t
                self.t = self.nexttime
                self.OnDraw()
                normal = self.nextline.FindNormalPerpVector()
                newvector = self.geomcalc.SubVector(self.currentray.vector, self.geomcalc.MultScalar(2, self.geomcalc.MultScalar(self.geomcalc.DotProduct(self.currentray.vector, normal), normal))) 
                [x, y] = self.currentray.GetEndPoint(self.t)
                newx = x + newvector.GetX()
                newy = y + newvector.GetY()
                self.ray.append(self.currentray)
                self.currentray = ColoredRay([x, y], [newx, newy], 0, 0, 1)
                self.t += excess
                
                [self.nexttime, self.nextline] = self.GenerateCollisionTimes()
                
            self.OnDraw()
        event.Skip()
    
    def GenerateCollisionTimes(self):
        self.outlinetemp = None
        self.inlinetemp = None
        self.ClassifyLines()
        current_t_in =  500000000
        current_t_out = 500000000
        
        
        for i in self.arena.GetLines():
            
            if i.GetBound() != 0:
                temptime = i.GetCollisionTime(self.currentray)
                print "Arena: ", temptime
                         
            if i.GetBound() == -1:
                
                if temptime < current_t_in:
                    if temptime > 0:
                        current_t_in = temptime
                        print "Arena: Current In set to ", temptime
                        self.inlinetemp = i
            if i.GetBound() == 1:
                
                if temptime < current_t_out:
                    
                    if temptime > 0:
                        
                        current_t_out = temptime
                        print "Arena: Current Out set to ", temptime
                        self.outlinetemp = i

        for j in self.pillar:
            
            matchindex = 0
            for i in j.GetLines():
                matchindex += i.GetBound()
                
                if i.GetBound() != 0:
                    temptime = i.GetCollisionTime(self.currentray)
                    print "Pillar: ", temptime
                    
                if i.GetBound() == -1:
                    if temptime < current_t_in:
                        
                        
                        if matchindex <= 0:
                        
                            if temptime > 0:
                                current_t_in = temptime
                                print "Pillar: Current In set to ", temptime
                                self.inlinetemp = i
                if i.GetBound() == 1:
                    if temptime < current_t_out:
                        
                        if matchindex <= 0:
                        
                            if temptime > 0:
                                
                                current_t_out = temptime
                                print "Pillar: Current Out set to ", temptime
                                self.outlinetemp = i
        
        if current_t_out == 500000000:
            return [current_t_in, self.inlinetemp]
        
        if current_t_in == 500000000:
            return [current_t_out, self.outlinetemp]  
        
        
        if current_t_out < current_t_in:            
            print "Out: ", current_t_out
            return [current_t_out, self.outlinetemp]            
        if current_t_in <= current_t_out:
            print "In: ", current_t_in
            return [current_t_in, self.inlinetemp]
                      
    def ClassifyLines(self):                    
        for i in self.arena.GetLines():
            test = self.geomcalc.DotProduct(i.FindNormalPerpVector(), self.currentray.vector)
            
            if test < 0:
                i.SetBound(-1)
            if test == 0:
                i.SetBound(0)
            if test > 0:
                i.SetBound(1)
            
        for j in self.pillar:
            for i in j.GetLines():
                test = self.geomcalc.DotProduct(i.FindNormalPerpVector(), self.currentray.vector)
                if test < 0:
                    i.SetBound(-1)
                if test == 0:
                    i.SetBound(0)
                if test > 0:
                    i.SetBound(1)
                    
