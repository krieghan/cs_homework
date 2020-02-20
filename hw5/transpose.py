"""

C. Andrews 2006

"""

import wx
from wx.glcanvas import GLCanvas
#from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy




class GLTranspose(GLCanvas):
    """Basic template for a GLCanvas that can do simple 2D OpenGL drawing"""
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we can properly initialize the canvas"""
        GLCanvas.__init__(self, parent, -1)
        self.init = 0
        self.SetCurrent()

        self.startingpoints = [[0, 0, 0, 1], [0, 10, 0, 1], [10, 10, 0, 1], [10, 0, 0, 1]]
        self.points = []
        self.currentpoints = self.startingpoints
        
        self.AppendCurrentPoints()
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.command = []
        self.macro = {}
        self.macrostate = 0
        self.displaylist = None
        return


    def SetupView(self):
        """This function does the actual work to setup the window so we can draw in it. We'll
        explain this in more detail later.
        """
        
        self.SetCurrent()
        self.FindBoundaries()
        
        
        
        
        self.clientsize = self.GetClientSizeTuple()
        glViewport(0,0, self.clientsize[0], self.clientsize[1])
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        
        #I need to find an appropriate border value.  It's scaled by the client-area because the world-window zooms, thus skewing any normal border given.
        if self.worldwidth == 0 or self.worldheight == 0:
            self.xborder = 1
            self.yborder = 1
        else:
            self.xscale = self.clientsize[0] / self.worldwidth
            self.xborder = 10 / self.xscale
            self.yscale = self.clientsize[1] / self.worldheight
            self.yborder = 10 / self.yscale
            
            self.maxleft -= self.xborder
            self.maxright += self.xborder
            self.maxtop += self.yborder
            self.maxbottom -= self.yborder
            
            self.worldheight = self.maxtop - self.maxbottom
            self.worldwidth = self.maxright - self.maxleft

        
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
        
        
        gluOrtho2D(self.maxleft, self.maxright, self.maxbottom, self.maxtop)



    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. Again,
        we'll describe this in more detail later.
        """
        self.SetCurrent()
        glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
        self.SetupView()
        return



    def OnPaint(self,event):
        """This function is called when the canvas recieves notice that it needs to repaint its
        surface. This just makes sure that OpenGL is inited and passes the work off to another
        function.
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
        """This is the main drawing function. We will put all of our OpenGL drawing calls in here.
        If we want to force a repaint, this is the function that should be called. Note that this
        should always start by calling SetCurrent() and end by calling SwapBuffers().
        """

        self.SetCurrent()

        glClear(GL_COLOR_BUFFER_BIT)


        
        if self.displaylist is None:
            self.displaylist = glGenLists(1)
            glNewList(self.displaylist, GL_COMPILE_AND_EXECUTE)
            self.DrawList(self.command)
            glEndList()
            
        else:
            glCallList(self.displaylist)
        
        
        self.SetupView()
        
        glMatrixMode(GL_MODELVIEW)
        
        glLoadIdentity()         

        
        
        
        self.SwapBuffers()

        return


    def DoDisplay(self, filename):
        
    
        f = open(filename, 'r')
        self.command = f.read()
        self.command = self.command.split('\n')
        for i in range(len(self.command)):
            self.command[i] = self.command[i].split()

        self.displaylist = None
        self.points = []
        self.currentpoints = [[5, 5, 0, 1], [5, -5, 0, 1], [-5, 5, 0, 1], [-5, -5, 0, 1]]
        self.OnDraw()
        self.OnDraw()

    def DrawAxis(self):
        glBegin(GL_LINES)
        glColor3f(0, 0, 1)
        glVertex2i(0, 0)
        glVertex2i(0, 10)
        glColor3f(0, 1, 0)
        glVertex2i(0, 0)
        glVertex2i(10, 0)
        glEnd()

    def DrawSquare(self):
        glColor3f(1, 1, 1)
        glBegin(GL_LINE_LOOP)
        glVertex2i(0,0)
        glVertex2i(0,10)
        glVertex2i(10,10)
        glVertex2i(10,0)
        glEnd()

    def AppendCurrentPoints(self):
        for i in self.currentpoints:
            self.points.append(i)


    def FindBoundaries(self):
        self.maxleft = 0
        self.maxright = 10
        self.maxbottom = 0
        self.maxtop = 10
        
        
        
        for i in self.points:
            if i[0] < self.maxleft:
                self.maxleft = i[0]
            if i[0] > self.maxright:
                self.maxright = i[0]
            if i[1] < self.maxbottom:
                self.maxbottom = i[1]
            if i[1] > self.maxtop:
                self.maxtop = i[1]
        
        self.worldheight = self.maxtop - self.maxbottom
        self.worldwidth = self.maxright - self.maxleft
            
            
    def FindNewPoints(self):
        for i in range(len(self.currentpoints)):
            self.currentpoints[i] = numpy.matrixmultiply(self.startingpoints[i], glGetFloatv(GL_MODELVIEW_MATRIX))
            
        self.AppendCurrentPoints()
        
   
    def DrawList(self, commandlist):

        for command in commandlist:
            if self.macrostate == 1:
                if command[0] == "end":
                    self.macrostate = 0
                    self.macroname = ''
                else:
                    self.macro[self.macroname].append(command)
            else:

                if command[0] == "draw":
                    self.DrawSquare()
                    self.FindNewPoints()
                    print "DrawCube()"
                    
                elif command[0] == "translate":
                    glTranslatef(float(command[1]), float(command[2]), 0)
                    print "glTranslatef(", float(command[1]), float(command[2]), 0, ")"
                                        
                elif command[0] == "scale":
                    glScalef(float(command[1]), float(command[2]), 1)
                    print "glScalef(", float(command[1]), float(command[2]), 1, ")"
                elif command[0] == "rotate":
                    glRotatef(float(command[1]), 0, 0, 1)
                    print "glRotatef(", float(command[1]), 0, 0, 1, ")"
                elif command[0] == "shear":
                    sheer = numpy.identity(4, 'f')
                    sheer[0][1] = float(command[1])
                    sheer[1][0] = float(command[2])
                    glMultMatrixf(sheer)
                    
                elif command[0] == "push":
                    glPushMatrix()
                    print "glPushMatrix()"
                elif command[0] == "pop":
                    glPopMatrix()
                    print "glPopMatrix()"
                elif command[0] == "start":
                    self.macrostate = 1
                    self.macroname = command[1]
                    self.macro[self.macroname] = []
                else:
                    if self.macro.has_key(command[0]):
                        self.DrawList(self.macro[command[0]])
                    else:
                        print "Invalid command: ", command[0]