"""
Template

This module contains a basic template for a class that extends the GLCanvas and includes the basic routines 
for setting up simple 2D drawing.

C. Andrews 2006

"""

import wx
import numpy
from texture import *

from wx.glcanvas import GLCanvas
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

from camera import *


class GLSphere(GLCanvas):
    """Basic template for a GLCanvas that can do simple 2D OpenGL drawing"""
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we can properly initialize the canvas"""
        GLCanvas.__init__(self, parent,-1)
        self.init = 0
        
        

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.HandleTime)
        
        self.camera = Camera([15, 0, 60], [0, 0, 0])
        
        self.angle = 0
        
        self.timer = wx.Timer(self)
        self.timer.Start(20)
        
        self.spherelist = None
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

        
    def SetupLights(self):
        """Sets up the Light in the world"""
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_AMBIENT, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_POSITION, (3,4,-3,1))

    def SetupMaterial(self):
        """Sets the material properties of the terrain"""
        glMaterialfv(GL_FRONT, GL_AMBIENT, (.19125, .0735, .0225, 1))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (.7038, .27048, .0828, 1))
        glMaterialfv(GL_FRONT, GL_SPECULAR,(.256777,.137622,.086014, 1))
        glMaterialfv(GL_FRONT, GL_SHININESS, 12.8)        
        glDisable(GL_COLOR_MATERIAL)


    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. 
        Again, we'll describe this in more detail later.
        """
        self.SetCurrent()
        glClearColor(0.0,0.0,0.0,0.0) # set clear color to black
        self.SetupView()
        self.SetupMaterial()
        glEnable(GL_DEPTH_TEST)
        self.texture = Checker()
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
        glRotatef(45, 0, 1, 0)
        self.SetupMaterial()
        
        if self.spherelist is None:
            self.spherelist = glGenLists(1)
            glNewList(self.spherelist, GL_COMPILE_AND_EXECUTE)
            
        
            self.SetupLights()
        
            glDisable(GL_COLOR_MATERIAL)
            
            self.DrawSphere(2, 10, 10)
            glPushMatrix()
            glTranslate(8, 0, 0)
            glEnable(GL_TEXTURE_2D)
            glEnable(GL_COLOR_MATERIAL)
            self.texture.set()
            self.DrawSphere(2, 10, 10)
            glDisable(GL_TEXTURE_2D)
            glDisable(GL_COLOR_MATERIAL)
            glPopMatrix()
            
            glEndList()
        else:
            glCallList(self.spherelist)

        
        self.SwapBuffers()

        return
    
    def HandleTime(self, event):
        self.angle = (self.angle + 1) % 360
        self.OnDraw()
        #self.DrawLine()
        
    def DrawSphere(self, radius, stacks, slices):
        stackoffset = float(2 * radius) / stacks
        sliceoffset = float(360) / slices
        
        print sliceoffset
        
        
        
        points = []
        y = float(0 - radius)
        while y < radius:
            x = float(0 - radius)
            while x < radius:
                z = float(0 - radius)
                while z < radius:
                    distance = math.floor(float(math.sqrt(x**2 + y**2 + z**2)))
                    #print distance + .0000000000000000000000000009
                    #if distance - .0000000000000000000000000009 <= radius + .009 or distance + .0000000000000000000000000009 >= radius - .009:
                    if distance == math.floor(radius):
                        points.append([x, y, z])
                    
                    #print "z: ", z
                    z = round(z + .05, 4)
                #print "x: ", x
                x = round(x + .05, 4)
            #print "y: ", y
            y = round(y + .05, 4)
        
        
        stack = []
        y = float(radius)
        j = 0
          
        
        
        #print stackoffset
        for j in range(stacks):
            stack.append([])
            
            for k in range(slices):
                stack[j].append([])
                                                    
            for i in points:
            
                if round(i[1], 1) == round(y, 1):
                    #print math.floor(math.degrees(math.acos(float(i[0]) / radius)))
                    #print "theta: ", theta
                    
                    #print math.floor(math.degrees(math.acos(float(i[0]) / radius))) % sliceoffset, int(math.floor(math.degrees(math.acos(float(i[0]) / radius))) / sliceoffset)
                    
                    if math.floor(math.degrees(math.acos(float(i[0]) / radius))) % sliceoffset <= 1:
                        #print math.floor(math.degrees(math.acos(float(i[0]) / radius))), " passed"
                        factor = math.floor(math.degrees(math.acos(float(i[0]) / radius))) 
                        if i[2] < 0:
                         #   print "We got here"
                            factor += 180
                        
                        #print "We got one for stack = ", j, " and slice = ", factor
                        #print math.acos(float(i[0]) / radius)
                        #print int(factor / sliceoffset)
                        stack[j][int(factor / sliceoffset) - 1].append(i)
                            
                    
                    
                
            y -= stackoffset
            
            
        
        
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        #print points
        
        
        #for i in points:
        
        #print stack
        
        for j in range(len(stack) - 1):
            
            for k in range(len(stack[j])):
                #print len(k)
                if len(stack[j][k]) > 0:
                    #if j == 0:
                    glTexCoord2f(0.,0.)
                    
                    glNormal3f(0, 0, 1)
                    glVertex3f(*stack[j][k][0])
                    #if j == 0:
                    glTexCoord2f(1.,0.)
                    
                    glNormal3f(0, 0, 1)
                    glVertex3f(*stack[j][(k + 1) % slices][0])
                    
                    #if j == len(stack) - 2:
                    glTexCoord2f(0., 1.)
                    glNormal3f(0, 0, 1)
                    glVertex3f(*stack[(j + 1)][(k + 1) % slices][0])
                    #if j == len(stack) - 2:
                    glNormal3f(0, 0, 1)
                    glTexCoord2f(1., 1.)
                    glVertex3f(*stack[(j + 1)][k][0])
                    
                #for m in k:
                #    glVertex3f(*m)
        
        glEnd()
            
                    
        