"""
Template

This module contains a basic template for a class that extends the GLCanvas and includes the basic routines for setting up simple 2D drawing.

C. Andrews 2006

"""

import wx
from wx.glcanvas import GLCanvas
#from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math




class GLPane(GLCanvas):
    """Basic template for a GLCanvas that can do simple 2D OpenGL drawing"""
    
    iterations = 0
    angle = 0
    seedstring = ""
    f = ""
    x = ""
    y = ""
    finalstring = ""
    currentheading = 0
    startingpoint = [100, 100]
    currentpoint = startingpoint
    length = 1
    
    maxleft = currentpoint[0]
    maxright = currentpoint[0] + 100
    maxtop = currentpoint[1] + 100
    maxbottom = currentpoint[1]
    
    stack = []
    
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we can properly initialize the canvas"""
        GLCanvas.__init__(self, parent,-1)
        self.init = 0


        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        return


    def SetupView(self):
        """This function does the actual work to setup the window so we can draw in it. We'll explain this in more detail later.
        """
        size = self.GetClientSizeTuple()
        height = self.maxtop - self.maxbottom
        width = self.maxright - self.maxleft
        screenratio = float(size[0]) / float(size[1])
        if height == 0 or width == 0:
            ratio = screenratio
        else:
            ratio = width / height
            print ratio, " ", float(size[0]) / float(size[1]), " ", size[0], " ", size[1]
        
        if ratio > screenratio:
            glViewport(0, (size[1] - (size[0] / ratio)) / 2, size[0], size[0] / ratio)
        if ratio < screenratio:
            glViewport((size[0] - size[1] * ratio) / 2, 0, size[1] * ratio, size[1])
        
        
        #glViewport(0,0,size[0], size[1])

        if width == 0 or height == 0:
            xborder = 1
            yborder = 1
        else:
            xscale = size[0] / width
            xborder = 10 / xscale
            yscale = size[1] / height
            yborder = 10 / yscale
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(self.maxleft - xborder, self.maxright + xborder, self.maxbottom - yborder, self.maxtop + yborder)



    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. Again, we'll describe this in more detail later.
        """
        glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
        glEnable(GL_TEXTURE_2D)
        self.SetupView()
        return



    def OnPaint(self,event):
        """This function is called when the canvas recieves notice that it needs to repaint its surface. This just makes sure that OpenGL is 
		inited and passes the work off to another function.
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
        
    def PrepareBoundaries(self):
        self.maxleft = self.currentpoint[0]
        self.maxright = self.currentpoint[0]
        self.maxtop = self.currentpoint[1]
        self.maxbottom = self.currentpoint[1]
        for element in self.finalstring:
            if element == '+':
                self.currentheading += self.angle
            elif element == '-':
                self.currentheading -= self.angle
            elif element == 'F':
                if self.maxleft > self.currentpoint[0]:
                    self.maxleft = self.currentpoint[0]
                if self.maxright < self.currentpoint[0]:
                    self.maxright = self.currentpoint[0]
                if self.maxbottom > self.currentpoint[1]:
                    self.maxbottom = self.currentpoint[1]
                if self.maxtop < self.currentpoint[1]:
                    self.maxtop = self.currentpoint[1]
                          
                
                self.currentpoint = self.NextPoint(self.currentpoint, self.length, self.currentheading)
                
                
                                
            elif element == '[':
                self.stack.append([self.currentpoint[0], self.currentpoint[1], self.currentheading])
            elif element == ']':
                popped = self.stack.pop()
                self.currentheading = popped.pop()
                self.currentpoint = popped
        
            if self.maxleft > self.currentpoint[0]:
                self.maxleft = self.currentpoint[0]
            if self.maxright < self.currentpoint[0]:
                self.maxright = self.currentpoint[0]
            if self.maxbottom > self.currentpoint[1]:
                self.maxbottom = self.currentpoint[1]
            if self.maxtop < self.currentpoint[1]:
                self.maxtop = self.currentpoint[1]        
                
                
        self.currentheading = 0
        self.currentpoint = self.startingpoint


    def OnDraw(self):
        """This is the main drawing function. We will put all of our OpenGL drawing calls in here. If we want to force a repaint, this is the 
		function that should be called. Note that this should always start by calling SetCurrent() and end by calling SwapBuffers().
		"""
        self.SetCurrent()

        glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_LINES)

        glColor3f(1.0, 1.0, 1.0)
        
        self.currentpoint = self.startingpoint
        self.currentheading = 0
        
        
             
        for element in self.finalstring:
            if element == '+':
                self.currentheading += self.angle
            elif element == '-':
                self.currentheading -= self.angle
            elif element == 'F':
                glVertex2i(self.currentpoint[0], self.currentpoint[1])
                self.currentpoint = self.NextPoint(self.currentpoint, self.length, self.currentheading)
                glVertex2i(self.currentpoint[0], self.currentpoint[1])
            elif element == '[':
                self.stack.append([self.currentpoint[0], self.currentpoint[1], self.currentheading])
            elif element == ']':
                popped = self.stack.pop()
                self.currentheading = popped.pop()
                self.currentpoint = popped
        
      
        
        
        glEnd()
        self.currentpoint = self.startingpoint
        self.currentheading = 0
        
        
        self.SwapBuffers()
        

        return	
    
    def DisplayTurtle(self, iterations, seedstring, angle, f, x, y):
        self.iterations = int(iterations)
        self.angle = int(angle)
        self.seedstring = seedstring.upper()
        self.f = f.upper()
        self.x = x.upper()
        self.y = y.upper()
        self.finalstring = self.GenerateString(self.iterations, self.seedstring)
        self.finalstring = self.finalstring.replace("X", "")
        self.finalstring = self.finalstring.replace("Y", "")
        self.PrepareBoundaries()
        self.SetupView()
        self.OnDraw()
		
	
    def GenerateString(self, i, string):
        if i <= 0:
            return string
		
        string = string.replace("F", (self.f).lower())        
        string = string.replace("X", (self.x).lower())
        string = string.replace("Y", (self.y).lower())
        
        
        string = string.upper()
        print string
        string = self.GenerateString(i - 1, string)

        return string
        
    def NextPoint(self, currentpoint, length, angle):
        x = length * math.degrees(math.cos(math.radians(angle)))
        y = length * math.degrees(math.sin(math.radians(angle)))
        return [currentpoint[0] + x, currentpoint[1] + y]