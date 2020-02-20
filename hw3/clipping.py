"""
Title:      Clipping Polygons
Author:     Krieghan J. Riley
Date:       April 11, 2006
Purpose:    This program starts with a clipping rectangle.  The user draws a polygon using click events,
            and we clip the polygon based on where it lies in relation to the rectangle.
            
Problems:   There is a minor problem with a special case that I haven't been able to figure out.
            If a polygon leaves the rectangle at a side and re-enters on another side, the line-loop
            cuts across the rectangle instead of appropriately drawing along the sides.  I have not yet developed a 
	    solution for this issue.
	    
Based on template.py from C. Andrews 2006	    
"""


import wx
from wx.glcanvas import GLCanvas
#from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math

class GLPane(GLCanvas):
    """Our Canvas Class - everything drawn will be drawn on this canvas"""
    
    #We want to start with some dimensions and locations
    
    worldmaxleft = 0
    worldmaxright = 250
    worldmaxtop = 200
    worldmaxbottom = 0
    
    rectmaxleft = 50
    rectmaxright = 200
    rectmaxtop = 150
    rectmaxbottom = 50
    
    viewport_left = 0
    viewport_bottom = 0
    viewport_height = 0
    viewport_width = 0
    
    #These lists hold the points in their appropriate category.
    points = []
    acceptpoints = []
    rejectpoints = []
    
    #If 0, the user may draw. If 1, the polygon has been clipped and further clicks are discarded.  Clearing the screen resets this variable to 0.
    clipmode = 0
    
    #The codeword values of our half-plane sectors
    sector = [[1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0], [1, 0, 0, 1], [0, 0, 0, 1], [0, 0, 1, 1]]
    
    drawlist = None
    
  
    
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we
        can properly initialize the canvas"""
        GLCanvas.__init__(self, parent,-1)
        self.init = 0        
        
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_LEFT_UP, self.HandleClick)
        return


    def SetupView(self):
        """This function does the actual work to setup the window so we can 
        draw in it.  Most of its task is going to be sizing the Viewport to
        maintain aspect ratio and sizing the World Window to achieve the 
        maximum possible zoom.
        
        """
        
        self.clientsize = self.GetClientSizeTuple()
       
        height = 200 
        width = 250                
        
        #The ratio of the width to the height in the client-area
        screenratio = float(self.clientsize[0]) / float(self.clientsize[1])
        
        ratio = width / height
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
         
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(self.worldmaxleft, self.worldmaxright, self.worldmaxbottom, self.worldmaxtop)
        


    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. 
        """
        glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
        glEnable(GL_TEXTURE_2D)
        self.SetupView()
        return



    def OnPaint(self,event):
        """This function is called when the canvas recieves notice that it needs to repaint its surface. 
        This just makes sure that OpenGL is inited and passes the work off to another function.
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
        event.Skip()

        
    def OnDraw(self):
        """This is the main drawing function. It does the work of plotting the in-progress polygon or 
        the accepted and rejected line segments.
        """
        
        self.SetCurrent()
        glClear(GL_COLOR_BUFFER_BIT)
               
        glBegin(GL_LINE_LOOP)
        glColor3f(1.0, 1.0, 1.0)                
        
        
        glVertex2f(self.rectmaxleft, self.rectmaxbottom)
        glVertex2f(self.rectmaxleft, self.rectmaxtop)
        glVertex2f(self.rectmaxright, self.rectmaxtop)
        glVertex2f(self.rectmaxright, self.rectmaxbottom)
              
        
        glEnd()                     
        
        
        glBegin(GL_LINE_STRIP)
        glColor3f(1.0, 1.0, 1.0)
        
        for currentpoint in self.points:
            glVertex2f(currentpoint[0], currentpoint[1])
        
        glEnd()
        
        
           
        if len(self.acceptpoints) > 0:
               
            glBegin(GL_LINE_LOOP)
            glColor3f(0, 1.0, 0)
        
            
            
            for currentpoint in self.acceptpoints:
                glVertex2f(currentpoint[0], currentpoint[1])                          
            glEnd()
        
        if len(self.rejectpoints) > 0:
               
            
            glBegin(GL_LINES)
            glColor3f(1.0, 0, 0)
        
            
            for currentpoint in self.rejectpoints:
                glVertex2f(currentpoint[0], currentpoint[1])
                
          
            glEnd()
        
        
        self.SwapBuffers()

        return	
    
    def HandleClick(self, event):
        """Called when the user clicks in the canvas.  The main idea of this
        function is to record the points in points[].  A conversion must take
        place in GiveWorldXY for the points to be expressed in terms of the world.
        """
    
        if self.clipmode == 1:
            return
            
        self.clientsize = self.GetClientSizeTuple()
        
        #If the click isn't in the viewport, I can't do anything with it
        if event.GetX() >= self.viewport_left and event.GetX() <= self.viewport_right: 
            if self.clientsize[1] - event.GetY() <= self.viewport_top and self.clientsize[1] - event.GetY() >= self.viewport_bottom:
                
                
                self.points.append(self.GiveWorldXY(event.GetX(), event.GetY()))                     

                numpoints = len(self.points)
                
                #These ifs handle the last line in the polygon.  I don't want to use Line_Loop because the last line would be lost when I do the clipping.
                if numpoints > 2:
                    if numpoints > 3:
                        self.points.pop(numpoints - 2)
                    self.points.append([self.points[0][0], self.points[0][1]])
                
                
                
        self.OnDraw()
        event.Skip()
        return
        
    
    def DoDisplay(self):
        """Called when the user clicks the display button on the GUI.  Clips the image, empties out 
        points[] and draws."""
        
        self.clipmode = 1
        self.ClipImage()
        self.points = []
        self.OnDraw()        
        return
        
    def DoClear(self):
        """Called when the user clicks the clear button on the GUI.  Resets clipmode, empties out
        the point lists and draws the image"""
        self.clipmode = 0
        self.points = []
        self.acceptpoints = []
        self.rejectpoints = []
        self.OnDraw()
        return
    
    def GiveWorldXY(self, x, y):
        """Our conversion function.  Here, we must convert from canvas coordinates (which is how the
        click is expressed) to viewport coordinates and then to world coordinates."""

        self.clientsize = self.GetClientSizeTuple()
        
        yscale = float(self.worldmaxtop - self.worldmaxbottom) / float(self.viewport_height)
        
        xscale = float(self.worldmaxright - self.worldmaxleft) / float(self.viewport_width)

        
        
        return [(x - self.viewport_left) * xscale, (self.clientsize[1] - y - self.viewport_bottom) * yscale]

    def ClipImage(self):
        """This function is the master clip function (responsible for clipping the entire image).  
        Not much here, since clipping an image is really just clipping a series of lines.
        """
        
        i = 0
        
        while i + 1 < len(self.points):
            self.ClipLine(self.points[i][0], self.points[i][1], self.points[i + 1][0], self.points[i + 1][1])
            i += 1
            

    def ClipLine(self, x1, y1, x2, y2):
        """Responsible for clipping individual lines.  The master loop here shouldn't be executed
        more then 4 times.  The majority of the function is as described in the book.  However,
        since I want to save the rejected lines in rejectedpoints[], I have to do some extra
        appending"""
    
        while 1:
    
            
            #Gets the sector id for each point
            sector1 = self.SegmentPoint(x1, y1)
            sector2 = self.SegmentPoint(x2, y2)
            
            
            #Decides whether or not this line is trivial accept, trivial reject or whether it demands further processing
            result = self.JudgeLine(sector1, sector2)
            
            
        
            if result == 0:
                self.rejectpoints.append([x1, y1])
                self.rejectpoints.append([x2, y2])
                return 0
                
            if result == 1:
                self.acceptpoints.append([x1, y1])
                self.acceptpoints.append([x2, y2])
                return 1
                
            #Here we do the clipping
            if result == 2:
                
                if sector1 != 4:
                    if sector1 == 0 or sector1 == 3 or sector1 == 6:
                        
                    
                        self.rejectpoints.append([x1, y1])
                        
                        y1 += (self.rectmaxleft - x1) * (y2 - y1) / (x2 - x1)
                        x1 = self.rectmaxleft + .001
                    
                        self.rejectpoints.append([x1, y1])
                        
                        
                    
                    elif sector1 == 2 or sector1 == 5 or sector1 == 8:
                        self.rejectpoints.append([x1, y1])
                        y1 += (self.rectmaxright - x1) * (y2 - y1) / (x2 - x1)
                        x1 = self.rectmaxright - .001
                        self.rejectpoints.append([x1, y1])
                                        
                    elif sector1 == 6 or sector1 == 7 or sector1 == 8:
                        self.rejectpoints.append([x1, y1])
                        x1 += (self.rectmaxbottom - y1) * (x2 - x1) / (y2 - y1) 
                        y1 = self.rectmaxbottom + .001
                        self.rejectpoints.append([x1, y1])
                
                    elif sector1 == 0 or sector1 == 1 or sector1 == 2:
                        self.rejectpoints.append([x1, y1])
                        x1 += (self.rectmaxtop - y1) * (x2 - x1) / (y2 - y1)
                        y1 = self.rectmaxtop - .001
                        self.rejectpoints.append([x1, y1])
                        
                    
                        
                else:
            
                    if sector2 == 0 or sector2 == 3 or sector2 == 6:
                        
                        self.rejectpoints.append([x2, y2])
                        y2 += ((self.rectmaxleft - x2) * (y1 - y2)) / (x1 - x2)
                        x2 = self.rectmaxleft + .001
                        self.rejectpoints.append([x2, y2])
                        
                        
                    
                    elif sector2 == 2 or sector2 == 5 or sector2 == 8:
                        self.rejectpoints.append([x2, y2])
                        y2 += (self.rectmaxright - x2) * (y1 - y2) / (x1 - x2)
                        x2 = self.rectmaxright - .001
                        self.rejectpoints.append([x2, y2])
                                        
                    elif sector2 == 6 or sector2 == 7 or sector2 == 8:
                        self.rejectpoints.append([x2, y2])
                        x2 += (self.rectmaxbottom - y2) * (x1 - x2) / (y1 - y2) 
                        y2 = self.rectmaxbottom + .001
                        self.rejectpoints.append([x2, y2])
                
                    elif sector2 == 0 or sector2 == 1 or sector2 == 2:
                        self.rejectpoints.append([x2, y2])
                        x2 += (self.rectmaxtop - y2) * (x1 - x2) / (y1 - y2)
                        y2 = self.rectmaxtop - .001
                        self.rejectpoints.append([x2, y2])
                    
                    
            
        
        
    def JudgeLine(self, sector1, sector2):
        """Tells us if a line is trivial accept, trivial reject or whether it requires
        further processing based on the sector ids of the two points"""
        i = 0
        
        if self.sector[sector1] == [0, 0, 0, 0] and self.sector[sector2] == [0, 0, 0, 0]:
            return 1
        
        while i < 4:
            if self.sector[sector1][i] == self.sector[sector2][i] and self.sector[sector1][i] == 1:                            
            
                return 0
            i += 1
        
        return 2
    
    def SegmentPoint(self, x, y):
        """Gives us the sectorid of a point"""
    
        if y >= self.rectmaxtop:
            if x <= self.rectmaxleft:
                return 0
            if x < self.rectmaxright and x > self.rectmaxleft:
                return 1
            if x >= self.rectmaxright:
                return 2
                
        if y < self.rectmaxtop and y > self.rectmaxbottom:
            if x <= self.rectmaxleft:
                return 3
            if x < self.rectmaxright and x > self.rectmaxleft:
                return 4
            if x >= self.rectmaxright:
                return 5
        
        if y <= self.rectmaxbottom:
            if x <= self.rectmaxleft:
                return 6
            if x < self.rectmaxright and x > self.rectmaxleft:
                return 7
            if x >= self.rectmaxright:
                return 8
        
                
    
    
    