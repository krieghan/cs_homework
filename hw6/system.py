"""

Title: Solar System
Author: Krieghan J. Riley
Date: May 8, 2006
Purpose: This program simulates a solar system.  The user has the ability to explore the system using
         slide, pitch and yaw.

Cool Thing: I thought that having everything rotate on different axes was pretty cool.  However, given your
            opinion, I scrambled to find something to add.  I implemented my own DrawRing() function
            and created an object with several rings that rotated around different axes about the same
            point.  Just to see if I could, I used the DrawRing() function as part of the basis for a
            DrawRingedWorld() function.  This ringed planet is nothing special (no special rotation tricks
            with the rings), but it does demonstrate what DrawRing() can be used for.
            
            Another note, DrawRing() basically works by drawing a point and doing a rotation, another point,
            another rotation, etc.  It can be very costly if the granularity is low enough, and can 
            really cut down on performance.  I tried displaylists briefly, but had limited success inserting
            them into either the drawing function or the DrawRing() function.
            
Changes:    I chose to make the forward, pitch and yaw buttons change the velocity of the camera, and not
            just the position.  This makes for less busy work with the button clicks.

            Based on template.py from C. Andrews 2006

"""

import wx
from wx.glcanvas import GLCanvas
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
import numpy

class AstralBody:
    """This class exists for the purpose of handling a sun, a planet, a moon, an asteroid, etc."""
    
    def __init__(self, distance, revspeed, rotspeed, revangle = 0, drawfunction = None, arglist = [], parentbody = None, revvector = [0, 1, 0], rotvector = [0, 1, 0], color = [1, 1, 1]):
        self.parentbody = parentbody
        self.distance = distance
        self.revangle = revangle
        self.rotangle = 0
        self.revvector = revvector
        self.rotvector = rotvector
        self.revspeed = revspeed
        self.rotspeed = rotspeed
        self.childbody = []
        self.drawfunction = drawfunction
        self.arglist = arglist
        self.color = color
    
    #Accessors:
    
    def GetChild(self, index = -1):
        if index == -1:
            return self.childbody
        
        return self.childbody[index]
    
    def GetParent(self):
        return self.parentbody
    
    def GetDistance(self):
        return self.distance

    def GetDrawfunction(self):    
        return self.drawfunction
        
    def GetArgList(self):
        return self.arglist
    
    def GetRevVector(self):
        return self.revvector
    
    def GetRotVector(self):
        return self.rotvector
    
    def GetColor(self):
        return self.color

    #Mutators:
        
    def SetParent(self, parentbody = None):
        self.parentbody = parentbody
    
    def SetDistance(self, distance = 0):
        self.distance = distance
    
    def SetDrawfunction(self, drawfunction = None):
        self.drawfunction = drawfunction
    
    def SetArglist(self, arglist):
        self.arglist = arglist
    
    def SetRevVector(self, revvector):
        self.revvector = revvector
    
    def SetRotVector(self, rotvector):
        self.rotvector = rotvector

    def SetColor(self, color):
        self.color = color
    
    def Draw(self):
        """Takes advantage of first class functions in python.  AstralBody
        keeps track of its drawing function and arguments.  When Draw() is 
        called, we just call that function."""
        
        glColor3f(*self.color)
        self.drawfunction(*self.arglist)
    
    def DrawBody(self):
        """A recursive function.  Basically, handle rotation and revolution, draw the body, 
        then call DrawBody() on all this AstralBody's children"""
        
    
        self.rotangle += math.radians(self.rotspeed)
        self.revangle += math.radians(self.revspeed)
        glPushMatrix()
        
        if self.parentbody != None:
            glRotatef(self.revangle, *self.revvector)
            glTranslatef(self.distance * self.revvector[1], self.distance * self.revvector[2], self.distance * self.revvector[0])
            glRotatef(-self.revangle, *self.revvector)
            
        glRotatef(self.rotangle, *self.rotvector)
        self.Draw()
        glRotatef(-self.rotangle, *self.rotvector)
        
        
        for i in self.childbody:
            glPushMatrix()
            i.DrawBody()
            glPopMatrix()
            
        glPopMatrix()
            
    def AddChild(self, child):
        self.childbody.append(child)
        
class Camera:                        
    """This class handles the camera, which allows us to change our
    point of view in the world"""
    
    def __init__(self, eyelist, looklist, uplist = [0, 1, 0]):
        self.forward = 0
        self.pitch = 0
        self.yaw = 0
        self.roll = 0
        
        self.eyelist = eyelist
        self.looklist = looklist
        self.uplist = uplist
                
        self.matrix = numpy.identity(4, 'f')        
        self.n = []
        self.u = []
        self.v = []
        self.d = []
        
        self.SetVectors()
        self.SetD()
        self.SetMatrix()
        
        
    def DotProduct(self, a, b):
        sum = 0
        for i in range(len(a)):
            sum += a[i] * b[i]
        return sum
    
    def CrossProduct(self, a, b):
        i = 1
        j = 1
        k = 1
        
        return [i * (a[1] * b[2] - a[2] * b[1]), j * (a[2] * b[0] - a[0] * b[2]), k * (a[0] * b[1] - a[1] * b[0])]
    
    def Normalize(self, vector, magnitude):
        
    
        for i in range(len(vector)):
            vector[i] /= magnitude
        
        return vector
    
    def GetForward(self):
        return self.forward
    
    def GetPitch(self):
        return self.pitch
    
    def GetYaw(self):
        return self.yaw
    
    def SetVectors(self):
        
        self.n = []
        for i in range(3):
            self.n.append(self.eyelist[i] - self.looklist[i])
        
        magnitude = math.sqrt(math.pow(self.n[0], 2) + math.pow(self.n[1], 2) + math.pow(self.n[2], 2))
        
        self.n = self.Normalize(self.n, magnitude)
        
        self.u = self.CrossProduct(self.uplist, self.n)
        
        magnitude = math.sqrt(math.pow(self.u[0], 2) + math.pow(self.u[1], 2) + math.pow(self.u[2], 2))
        
        self.u = self.Normalize(self.u, magnitude)
                
        self.v = self.CrossProduct(self.n, self.u)
        
        magnitude = math.sqrt(math.pow(self.v[0], 2) + math.pow(self.v[1], 2) + math.pow(self.v[2], 2))
        
        self.v = self.Normalize(self.v, magnitude)
        
        
        
    def SetD(self):
        #print "Setting D"
        negeye = [-self.eyelist[0], -self.eyelist[1], -self.eyelist[2]]
    
        self.d = []
        self.d.append(self.DotProduct(negeye, self.u))
        self.d.append(self.DotProduct(negeye, self.v))
        self.d.append(self.DotProduct(negeye, self.n))
        
        
    def SetMatrix(self):
        print self.d
        
        self.matrix[0] = [self.u[0], self.v[0], self.n[0], 0]
        self.matrix[1] = [self.u[1], self.v[1], self.n[1], 0]
        self.matrix[2] = [self.u[2], self.v[2], self.n[2], 0]
        self.matrix[3] = [self.d[0], self.d[1], self.d[2], 1]
        
        
        
    def Slide(self, delU, delV, delN):
        """Given the vectors, this function slides us along an axis"""
        
        self.eyelist[0] += delU * self.u[0] + delV * self.v[0] + delN * self.n[0]
        self.eyelist[1] += delU * self.u[1] + delV * self.v[1] + delN * self.n[1]
        self.eyelist[2] += delU * self.u[2] + delV * self.v[2] + delN * self.n[2]
        
        self.SetD()
        self.SetMatrix()


    def Roll(self, angle):
        """Given an angle, this function rolls the camera (that is, rotation about the z axis"""
        cs = math.cos(math.pi/180 * angle)
        sn = math.sin(math.pi/180 * angle)
        
        temp = self.u
        self.u = [cs * temp[0] - sn * self.v[0], cs * temp[1] - sn * self.v[1], cs * temp[2] - sn * self.v[2]]
        self.v = [sn * temp[0] + cs * self.v[0], sn * temp[1] + cs * self.v[1], sn * temp[2] + cs * self.v[2]]
        
        self.SetD()
        self.SetMatrix()
    
    def Pitch(self, angle):
        """Given an angle, this function pitches the camera (that is, rotation about the x axis"""
        cs = math.cos(math.pi/180 * angle)
        sn = math.sin(math.pi/180 * angle)
        
        
        temp = self.v
        self.v = [sn * self.n[0] + cs * temp[0], sn * self.n[1] + cs * temp[1], sn * self.n[2] + cs * temp[2]]
        self.n = [cs * self.n[0] - sn * temp[0], cs * self.n[1] - sn * temp[1], cs * self.n[2] - sn * temp[2]]
        
        self.SetD()
        self.SetMatrix()
    
    def Yaw(self, angle):
        """Given an angle, this function yaws the camera (that is, rotation about the y axis"""
        
        cs = math.cos(math.pi/180 * angle)
        sn = math.sin(math.pi/180 * angle)
    
    
        temp = self.u
        self.u = [cs * temp[0] - sn * self.n[0], cs * temp[1] - sn * self.n[1], cs * temp[2] - sn * self.n[2]]
        self.n = [sn * temp[0] + cs * self.n[0], sn * temp[1] + cs * self.n[1], sn * temp[2] + cs * self.n[2]]
        self.SetD()
        self.SetMatrix()


    def ChangeForward(self, value):
        """Basically, a function for changing where we are on the z axis"""
        self.forward += value
    
    def ChangePitch(self, value):
        """A function for changing the pitch by some amount"""
        self.pitch += value
    
    def ChangeYaw(self, value):
        """A function for changing the yaw by some amount"""
        self.yaw += value
        
        



        
class GLSystem(GLCanvas):
    """This class handles the Solar System and all the Canvas elements"""
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we can properly initialize the canvas"""
        GLCanvas.__init__(self, parent,-1)
        self.init = 0
        self.displaylist = None
        self.camera = Camera([25, 55, 25], [1, 1, 1])

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        
        self.Bind(wx.EVT_TIMER, self.HandleTime)
        glEnable(GL_DEPTH_TEST)
        
        #The following calls create a tree with root sun
        
        
        #The center of the system
        self.sun = AstralBody(0, 30, 30, 0, glutWireSphere, [10, 6, 3], None, [1, 0, 0], [1, 0, 0], [.2, .4, .6])
        
        #Planets
        
        self.sun.AddChild(AstralBody(40, 180, 20, 0, glutWireSphere, [10, 60, 60], self.sun, [0, 0, 1], [1, 0, 1], [.8, .2, .3]))
        self.sun.AddChild(AstralBody(80, 40, 40, 90, glutWireSphere, [10, 60, 60], self.sun, [0, 1, 0], [1, 1, 0], [.8, .2, .3]))
        self.sun.AddChild(AstralBody(120, 30, 80, 180, glutWireSphere, [10, 60, 60], self.sun, [0, 0, 1], [1, 1, 1], [.8, .2, .3]))
        self.sun.AddChild(AstralBody(160, 50, 90, 270, glutWireSphere, [10, 60, 60], self.sun, [1, 0, 0], [0, 0, 1], [.8, .2, .3]))
        self.sun.AddChild(AstralBody(200, 25, 60, 90, glutWireSphere, [10, 60, 60], self.sun, [0, 0, 1], [0, 1, 0], [.8, .2, .3]))
        self.sun.AddChild(AstralBody(240, 80, 35, 180, glutWireSphere, [10, 60, 60], self.sun, [1, 0, 1], [0, 1, 1], [.8, .2, .3]))
        self.sun.AddChild(AstralBody(280, 120, 45, 270, glutWireSphere, [10, 60, 60], self.sun, [0, 0, 1], [1, 0, 0], [.8, .2, .3]))
        self.sun.AddChild(AstralBody(320, 140, 25, 95, glutWireSphere, [10, 60, 60], self.sun, [0, 0, 1], [1, 0, 1], [.8, .2, .3]))
        self.sun.AddChild(AstralBody(360, 10, 95, 110, glutWireSphere, [10, 60, 60], self.sun, [1, 0, 1], [1, 1, 0], [.8, .2, .3]))
        self.sun.AddChild(AstralBody(400, 35, 105, 135, glutWireSphere, [10, 60, 60], self.sun, [0, 0, 1], [1, 1, 1], [.8, .2, .3]))
        self.sun.AddChild(AstralBody(440, 45, 165, 97, glutWireSphere, [10, 60, 60], self.sun, [0, 1, 0], [0, 0, 1], [.8, .2, .3]))
        self.sun.AddChild(AstralBody(480, 90, 180, 157, glutWireSphere, [10, 60, 60], self.sun, [1, 0, 0], [0, 1, 0], [.8, .2, .3]))
        
        #My rotating rings
        
        self.sun.AddChild(AstralBody(60, 130, 130, 45, self.DrawRing, [10, .1], self.sun, [1, 0, 0], [0, 0, 1], [.4, .8, .1]))
        self.sun.AddChild(AstralBody(60, 130, 130, 45, self.DrawRing, [10, .1], self.sun, [1, 0, 0], [1, 0, 0], [.4, .8, .1]))
        self.sun.AddChild(AstralBody(60, 130, 130, 45, self.DrawRing, [10, .1], self.sun, [1, 0, 0], [1, 0, 1], [.4, .8, .1]))
        self.sun.AddChild(AstralBody(60, 130, 130, 45, self.DrawRing, [10, .1], self.sun, [1, 0, 0], [1, 1, 1], [.4, .8, .1]))

        
        #My ringed world
        #DrawRingedWorld(self, distance, startrev, radius, numrings, ringraddist, ringdistance, granularity, parent, revvector, rotvector, revspeed, rotspeed, planetcolor, ringcolor, ringrotvector)

        self.DrawRingedWorld(180, 0, 30, 5, 4, 3, .5, self.sun, [1, 1, 0], [0, 1, 1], 100, 70, [.6, 0, .8], [.3, .7, .9], [0, 0, 1])
        
        #My moons
        self.sun.GetChild(1).AddChild(AstralBody(20, 130, 180, 0, glutWireSphere, [5, 30, 30], self.sun.GetChild(1), [0, 0, 1], [1, 1, 0], [.8, .7, .3]))
        self.sun.GetChild(2).AddChild(AstralBody(20, 90, 70, 0, glutWireSphere, [5, 30, 30], self.sun.GetChild(2), [1, 0, 0], [0, 1, 0], [.8, .7, .3]))

        
        #My satellite (just for kicks)
        self.sun.GetChild(2).GetChild(0).AddChild(AstralBody(6, 140, 180, 0, glutWireSphere, [2, 15, 15], self.sun.GetChild(2).GetChild(0), [0, 1, 0], [1, 1, 0], [.7, 1, 0]))
        
        
        self.timer = wx.Timer(self)
        self.timer.Start(20)

        return


    def SetupView(self):
        """This function does the actual work to setup the window so we can draw in it. 
        Maintaing aspect ratio is easy for this project, since the controlling factor 
        is the size of the client window.  
        """
        
        
        self.SetCurrent()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        size = self.GetSizeTuple()
        gluPerspective(35, size[0] / size[1], 2, 2000)
        
        ratio = 1
        
        viewport_left = 0
        viewport_bottom = (size[1] - (size[0] / ratio)) / 2
        viewport_width = size[0]
        viewport_height = size[0] / ratio
        
        glViewport(viewport_left,viewport_bottom,viewport_width, viewport_height)

            
    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. 
        
        """
        self.SetCurrent()
        glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
        self.SetupView()
        self.OnDraw()
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


    def OnDraw(self):
        """This is the main drawing function. Basically, this is where we need to
        call the recursive DrawBody() function on the root of the system.  Because
        it's recursive, the subsequent in-function calls handle the rest of the system.
        """
        self.SetCurrent()
        
        

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glMatrixMode(GL_MODELVIEW)
        
        glLoadIdentity()                
        
        glMultMatrixf(self.camera.matrix) 
               
        glColor3f(1, 1, 1)
  
        self.sun.DrawBody()
   
        self.SwapBuffers()

        return
    
    def DoCameraChange(self, id, value):
        """This function is called by the button click handler in hw6.py."""
        if id == 0:
            self.camera.ChangeForward(value)
        if id == 1:
            self.camera.ChangePitch(value)
        if id == 2:
            self.camera.ChangeYaw(value)
        self.OnDraw()
    

    def DrawRing(self, radius, granularity):       
            """This function is called when we want to draw a ring.  Granularity basically
               indicates how much we rotate each time (that is, how close the points of the ring
               are to each other"""
               
            i = 0
            while i < 360:
                glBegin(GL_POINTS)
                glVertex3f(radius, 0, 0)
                glEnd()
                i += granularity
                glRotatef(granularity, 0, 1, 0)
  
    
    def DrawRingedWorld(self, distance, startrev, radius, numrings, ringraddist, ringdistance, granularity, parent, revvector, rotvector, revspeed, rotspeed, planetcolor, ringcolor, ringrotvector):
        """Uses DrawRing() to display a planet with a set of rings around it"""
        
        parent.AddChild(AstralBody(distance, revspeed, rotspeed, startrev, glutWireSphere, [radius, 60, 60], parent, revvector, rotvector, planetcolor))
                
        i = 0
        while i < numrings:
            parent.AddChild(AstralBody(distance, revspeed, rotspeed, startrev, self.DrawRing, [radius + ringdistance + ringraddist  * i, granularity], parent, revvector, ringrotvector, ringcolor))
            i += 1
            
        
        
    
    def HandleTime(self, event):
        """When timer is called, we handle all the camera moving.  I chose to make forward, pitch
           and yaw buttons change the velocity of the camera, not the position.  I think this makes
           for less busy work with button clicks."""
           
        if self.camera.GetForward() != 0:
            self.camera.Slide(0, 0, self.camera.GetForward())

        if self.camera.GetPitch() != 0:
            self.camera.Pitch(self.camera.GetPitch())
        
        if self.camera.GetYaw() != 0:
            self.camera.Yaw(self.camera.GetYaw())
            
        self.OnDraw()
        event.Skip()
    