"""
Template

This module contains a basic template for a class that extends the GLCanvas and includes the basic routines 
for setting up simple 2D drawing.

C. Andrews 2006

"""

import wx
import numpy
from wx.glcanvas import GLCanvas
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from camera import *


class GLCube(GLCanvas):
    """Basic template for a GLCanvas that can do simple 2D OpenGL drawing"""
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we can properly initialize the canvas"""
        GLCanvas.__init__(self, parent,-1)
        self.init = 0
        
        

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.HandleTime)
        
        self.camera = Camera([30, 30, 30], [0, 0, 0])
        
        self.angle = 0
        
        self.timer = wx.Timer(self)
        self.timer.Start(20)
        return


    def SetupView(self):
        """This function does the actual work to setup the window so we can draw in it. 
        We'll explain this in more detail later.
        """
        self.SetCurrent()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        size = self.GetSizeTuple()
        gluPerspective(20, size[0] / size[1], .1, 2000)
        
        ratio = 1
        
        viewport_left = 0
        viewport_bottom = (size[1] - (size[0] / ratio)) / 2
        viewport_width = size[0]
        viewport_height = size[0] / ratio
        
        glViewport(viewport_left,viewport_bottom,viewport_width, viewport_height)



    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. 
        Again, we'll describe this in more detail later.
        """
        self.SetCurrent()
        glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
        self.SetupView()
        glEnable(GL_DEPTH_TEST)
        return



    def OnPaint(self,event):
        """This function is called when the canvas recieves notice that it needs to repaint 
        its surface. This just makes sure that OpenGL is inited and passes the work off 
        to another function.
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

        
    def DrawDiagonal(self):
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        glVertex3f(-20, -20, -20)
        glVertex3f(20, 20, 20)
        
        glEnd()
        glColor3f(1, 1, 1)
        
    
        

    def OnDraw(self):
        """This is the main drawing function. We will put all of our OpenGL 
        drawing calls in here. If we want to force a repaint, this is the 
        function that should be called. Note that this should always start 
        by calling SetCurrent() and end by calling SwapBuffers().
        """
        self.SetCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        
        
        glMatrixMode(GL_MODELVIEW)
        
        glLoadIdentity()                
        
        glMultMatrixf(self.camera.matrix)
        
        rotationmatrix = numpy.identity(4, 'f')

        c = math.cos(math.radians(self.angle))
        s = math.sin(math.radians(self.angle))
        [ux, uy, uz] = [1, 1, 1]
        
        rotationmatrix[0][0] = c + (1 - c) * ux**2
        rotationmatrix[0][1] = ((1 - c) * ux * uy) + s * uz
        rotationmatrix[0][2] = ((1 - c) * ux * uz) - s * uy
        rotationmatrix[0][3] = 0
        
        rotationmatrix[1][0] = ((1 - c) * uy * ux) - (s * uz)
        rotationmatrix[1][1] = c + (1 - c) * uy**2
        rotationmatrix[1][2] = ((1 - c) * uy * uz) + s * ux
        rotationmatrix[1][3] = 0
        
        rotationmatrix[2][0] = ((1 - c) * uz * ux) + s * uy
        rotationmatrix[2][1] = ((1 - c) * uz * uy) - s * ux
        rotationmatrix[2][2] = c + (1 - c) * uz**2
        rotationmatrix[2][3] = 0
        
        rotationmatrix[3][0] = 0
        rotationmatrix[3][1] = 0
        rotationmatrix[3][2] = 0
        rotationmatrix[3][3] = 1
        
        #print rotationmatrix
        
        #glMultMatrixf(rotationmatrix)
        
        
        
        
        #glRotatef(self.angle, 0, 0, 1)
        #glRotatef(self.angle, 0, 1, 0)
        #glRotatef(self.angle, 1, 0, 0)        
        
        glBegin(GL_POLYGON)
        glColor3f(1, 0, 0)
        
        
        
        #glVertex3f(0, .33, -.33)
        
        #glVertex3f(-1.33, .33, -.33)        
        #glVertex3f(-2, 0, -2.5)
        #glVertex3f(-.2, .2, -2)                
        
        #glVertex3f(1 , 0, 0)
        #glVertex3f(0, 0, 0)        
        #glVertex3f(0, 0, 1)
        
        
        
        glVertex3f(0, 0, 0)   
        glVertex3f(0, 0, 1)              
        glVertex3f(-1.33, .33, -.33)                
        glVertex3f(-2, 0, -2.5)
        glVertex3f(-.2, .2, -2)                                        
        glVertex3f(1 , 0, 0)
             
        
        
        glColor3f(1, 1, 1)
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(0, 1, 0)
        glVertex3f(-1.33, .33, -.33)   
        glVertex3f(0, 0, 0)
        glColor3f(1, 1, 1)
        
        glEnd()
        
        glBegin(GL_POINTS)
        glColor3f(0, 0, 1)
        glVertex3f(4, 3, 5)
        glColor3f(1, 1, 1)
        glEnd()
        
        glBegin(GL_LINE_STRIP)

        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(1, 0, 1)
        glVertex3f(0, 0, 1)
        glEnd()
        
        glBegin(GL_LINE_STRIP)
        glVertex3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1, 0)
        glVertex3f(0, 1, 1)
        glEnd()
        
        glBegin(GL_LINE_STRIP)
        glVertex3f(0, 1, 1)
        glVertex3f(0, 0, 1)
        glVertex3f(1, 0, 1)        
        glVertex3f(1, 1, 1)
        glEnd()
        
        glBegin(GL_LINE_STRIP)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 0, 1)
        glVertex3f(1, 0, 0)             
        glVertex3f(1, 1, 0)
        glEnd()
        
        glBegin(GL_LINE_STRIP)
        glVertex3f(1, 1, 0)
        glVertex3f(1, 0, 0)
        glVertex3f(0, 0, 0)              
        glVertex3f(0, 1, 0)
        glEnd()
        
        glBegin(GL_LINE_STRIP)        
        glVertex3f(0, 1, 0)
        glVertex3f(1, 1, 0)
        glVertex3f(1, 1, 1)
        glVertex3f(0, 1, 1)
        
        glEnd()

        #self.DrawDiagonal()
        #self.DrawLine()
        
        self.SwapBuffers()

        return
    
    def HandleTime(self, event):
        self.angle = (self.angle + 1) % 360
        self.OnDraw()
        #self.DrawLine()