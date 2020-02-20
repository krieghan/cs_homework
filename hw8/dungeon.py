"""
Title: Dungeon Crawler
Author: Krieghan J. Riley
Date: May 29, 2006
Purpose: This program takes in a map file on the command line, creates the map as a 3D Dungeon, creates
         jewels around the dungeon, and proceeds to allow the user to move around to pick up the jewels.
         When all jewels have been collected, the game stops.

Cool thing: I decided that I wanted to experiment with making wave files play as the user picks up gems.
            I got it working on Windows, but had to nab some code off the internet to make it work in Linux.
            said code is indicated.

C. Andrews 2006

"""

import wx
import sys
import random
import platform
from wx.glcanvas import GLCanvas
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import Image
from struct import pack

from camera import *

file='bottle_x.wav'

windows = 1

if windows == 1:
    from winsound import PlaySound, SND_FILENAME, SND_ASYNC, SND_LOOP, SND_NOSTOP
    
#Code from internet
else:
    from wave import open as waveOpen
    from ossaudiodev import open as ossOpen
    
    

class GLDungeon(GLCanvas):
    """Handles the dungeon and what's being drawn"""
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we can properly initialize the canvas"""
        
        
        
        
        self.unitsize = 10
        self.height = 10
        self.viewfactor = .5
        
        self.clear = 0
        
        #Do the gems need to be redrawn?
        self.regem = 1
        
        #Current angle that the gems are spinning at
        self.gemangle = 0
        
        self.map = []
        
        #Parse the given file and create a map
        self.MakeMap(sys.argv[1])
        
        self.mazelist = None
        self.gemlist = None
        
        self.walls = []
        self.lights = []
        self.start = []
        self.gems = []
        self.gemcandidate = []
        
        #Populate my lists from the map of the dungeon.  The lists will give me more direct insight as to the contents of the dungeon.
        self.FindInfo()
        
        #Place the gems in the dungeon
        self.PlaceGems()
        
        print self.gems
        
        self.length = len(self.map)
        self.width = len(self.map[0])
        
        
        GLCanvas.__init__(self, parent,-1)
        self.init = 0
        glEnable(GL_NORMALIZE)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.HandleTime)
        self.Bind(wx.EVT_KEY_DOWN, self.HandleKey)
        
        
        
        self.crawler = Crawler(Camera([self.start[0], self.viewfactor * self.height, self.start[1]], [self.start[0], self.viewfactor * self.height, 1]), self) 
        self.timer = wx.Timer(self)
        
        #May need to be adjusted on slower machines
        self.timer.Start(20)
        
        return


    def SetupView(self):
        """Sets up the view to fit the client window
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
        
        #Light = Eval('GL_LIGHT' + num)
        
        #I hate that I didn't get this to be more elegant, but I am simply out of time.
        if len(self.lights) > 0:
        
            glEnable(GL_LIGHT0)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
            glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
            glLightfv(GL_LIGHT0, GL_POSITION, (self.lights[0][0], self.viewfactor * self.height, self.lights[0][1], 1))

        if len(self.lights) > 1:
        
            glEnable(GL_LIGHT1)
            glLightfv(GL_LIGHT1, GL_DIFFUSE, (1, 1, 1, 1))
            glLightfv(GL_LIGHT1, GL_SPECULAR, (1, 1, 1, 1))
            glLightfv(GL_LIGHT1, GL_POSITION, (self.lights[1][0], self.viewfactor * self.height, self.lights[1][1],1))
        
        if len(self.lights) > 2:
        
            glEnable(GL_LIGHT2)
            glLightfv(GL_LIGHT2, GL_DIFFUSE, (1, 1, 1, 1))
            glLightfv(GL_LIGHT2, GL_SPECULAR, (1, 1, 1, 1))
            glLightfv(GL_LIGHT2, GL_POSITION, (self.lights[2][0], self.viewfactor * self.height, self.lights[2][1],1))
        
        if len(self.lights) > 3:
        
            glEnable(GL_LIGHT3)
            glLightfv(GL_LIGHT3, GL_DIFFUSE, (1, 1, 1, 1))
            glLightfv(GL_LIGHT3, GL_SPECULAR, (1, 1, 1, 1))
            glLightfv(GL_LIGHT3, GL_POSITION, (self.lights[3][0], self.viewfactor * self.height, self.lights[3][1],1))
        
        if len(self.lights) > 4:
        
            glEnable(GL_LIGHT4)
            glLightfv(GL_LIGHT4, GL_DIFFUSE, (1, 1, 1, 1))
            glLightfv(GL_LIGHT4, GL_SPECULAR, (1, 1, 1, 1))
            glLightfv(GL_LIGHT4, GL_POSITION, (self.lights[4][0], self.viewfactor * self.height, self.lights[4][1],1))
        
        if len(self.lights) > 5:
        
            glEnable(GL_LIGHT5)
            glLightfv(GL_LIGHT5, GL_DIFFUSE, (1, 1, 1, 1))
            glLightfv(GL_LIGHT5, GL_SPECULAR, (1, 1, 1, 1))
            glLightfv(GL_LIGHT5, GL_POSITION, (self.lights[5][0], self.viewfactor * self.height, self.lights[5][1],1))
        
        if len(self.lights) > 6:
        
            glEnable(GL_LIGHT6)
            glLightfv(GL_LIGHT6, GL_DIFFUSE, (1, 1, 1, 1))
            glLightfv(GL_LIGHT6, GL_SPECULAR, (1, 1, 1, 1))
            glLightfv(GL_LIGHT6, GL_POSITION, (self.lights[6][0], self.viewfactor * self.height, self.lights[6][1],1))
        
        if len(self.lights) > 7:
            glEnable(GL_LIGHT7)
            glLightfv(GL_LIGHT7, GL_DIFFUSE, (1, 1, 1, 1))
            glLightfv(GL_LIGHT7, GL_SPECULAR, (1, 1, 1, 1))
            glLightfv(GL_LIGHT7, GL_POSITION, (self.lights[7][0], self.viewfactor * self.height, self.lights[7][1],1))
        
    def SetupMaterial(self):
        """Sets the material properties of the terrain"""
        #Material Ambient (R,G,B) Diffuse (R,G,B) Specular (R,G,B) Shininess.
        #ruby 0.1745 0.0117 0.0117 0.6142 0.0413 0.0413 0.7278 0.6269 0.6269 0.6
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, (.1745, .0117, .0117, 1))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (.6142, .0413, .0413, 1))
        glMaterialfv(GL_FRONT, GL_SPECULAR,(.7278, .06269,.06269, 1))
        glMaterialfv(GL_FRONT, GL_SHININESS, .6)        
        glEnable(GL_COLOR_MATERIAL)



    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform. 
        
        """
        
        self.SetCurrent()
        glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
        glEnable(GL_DEPTH_TEST)        
        self.SetupView()
        self.SetupMaterial()
        
        
        
        
        return

    def SetupTextures(self):
        """This function should be called to 'switch on' this texture."""
        glDisable(GL_TEXTURE_1D)
        glEnable(GL_TEXTURE_2D)

        self.name = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.name)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
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

        
    def DrawAxis(self):
        """Draws a 3D axis for testing purposes"""
        glBegin(GL_LINES)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, -100)
        glVertex3f(0, 0, 100)
        glColor3f(0, 1, 0)
        glVertex3f(0, -100, 0)
        glVertex3f(0, 100, 0)
        glColor3f(1, 0, 0)
        glVertex3f(-100, 0, 0)
        glVertex3f(100, 0, 0)
        glEnd()
        glColor3f(1, 1, 1)

        
    def OnDraw(self):
        """This function actually draws the maze
        """
        
        
        self.SetCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        
        
        glMatrixMode(GL_MODELVIEW)
        
        glLoadIdentity()                
        
        glMultMatrixf(self.crawler.camera.matrix)

        if self.mazelist is None:

            self.mazelist = glGenLists(1)
            glNewList(self.mazelist, GL_COMPILE_AND_EXECUTE)

            self.SetupLights()
            
            self.DrawAxis()
        
            self.SetupTextures()
            
            self.SetTexture("marble1.jpg")           
            self.DrawCeiling()
            
            self.SetTexture("marble4.jpg")
            self.DrawFloor()
            
            self.SetTexture("plate1.jpg")
            self.DrawWalls()
            
            glEndList()
            
            
        else:
            glCallList(self.mazelist)
        
        
        if self.regem == 1:
            if self.gemlist is None:
                self.gemlist = glGenLists(1)
                
            glNewList(self.gemlist, GL_COMPILE_AND_EXECUTE)
            
            #self.SetTexture("marble2.jpg") 
            glDisable(GL_TEXTURE_1D)
            glDisable(GL_TEXTURE_2D)
            self.DrawGems()
            
            
            
            glEndList()
        
        else:
            glCallList(self.gemlist)
                
        
        self.SwapBuffers()

        return

    
    
    def HandleTime(self, event):
        """Spins the gem and redraws"""
        self.gemangle += 5
        self.OnDraw()
        return
    
    def HandleKey(self, event):
        """Handles a keypress"""
        key = event.GetKeyCode()
        #print key
        
        #Again with the inefficiencies.  You really should make your exams easier...
        
        #87 = W
        if key == 87:            
            self.crawler.WalkForward()
        
        #83 = S
        if key == 83:
            self.crawler.WalkBackward()
            
        #65 = A
        if key == 65:
            self.crawler.TurnLeft()
        
        #68 = D        We'll explain this in more detail later.

        if key == 68:
            self.crawler.TurnRight()
            
        #81 = Q
        if key == 81:
            self.crawler.StrafeLeft()
        
        #69 = E
        if key == 69:
            self.crawler.StrafeRight()

        #If I'm out of gems, exit.
        if len(self.gems) == 0:
            print "You Win!"
            PlaySound(file, SND_FILENAME)
            
            sys.exit(1)                            

        self.OnDraw()

    
    def MakeMap(self, filename):
        """Creates the map from the file"""
        f = open(filename, 'r')
        lines = f.read().split('\n')
        self.map = []
        for i in lines:
            self.map.append(i.upper().split())
    
    def DrawCeiling(self):
        """Draws the ceiling"""
        glBegin(GL_QUADS)
        for i in range(0, self.length * self.unitsize, self.unitsize):
            
            for j in range(0, self.width * self.unitsize, self.unitsize):
                
                glNormal3f(0, -1, 0)
                glTexCoord2f(0.,0.)
                glVertex3f(i, self.height, j)
                glNormal3f(0, -1, 0)
                glTexCoord2f(0.,1.)
                glVertex3f(i, self.height, j + self.unitsize)
                glNormal3f(0, -1, 0)
                glTexCoord2f(1.,1.)
                glVertex3f(i + self.unitsize, self.height, j + self.unitsize)
                glNormal3f(0, -1, 0)
                glTexCoord2f(1.,0.)
                glVertex3f(i + self.unitsize, self.height, j)
        glEnd()
    
    
    def DrawFloor(self):
        """Draws the floor"""
        glBegin(GL_QUADS)
        for i in range(0, self.length * self.unitsize, self.unitsize):
            for j in range(0, self.width * self.unitsize, self.unitsize):
                glNormal3f(0, 1, 0)
                glTexCoord2f(0.,0.)
                glVertex3f(i, 0, j)
                glNormal3f(0, 1, 0)
                glTexCoord2f(0.,1.)
                glVertex3f(i, 0, j + self.unitsize)
                glNormal3f(0, 1, 0)
                glTexCoord2f(1.,1.)
                glVertex3f(i + self.unitsize, 0, j + self.unitsize)
                glNormal3f(0, 1, 0)
                glTexCoord2f(1.,0.)
                glVertex3f(i + self.unitsize, 0, j)
        glEnd()                                       
        
        
    def DrawWalls(self):
        """Draws the walls"""
        glBegin(GL_QUADS)
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 'W':
                    #West
                    glNormal3f(1, 0, 0)
                    glTexCoord2f(0.,1.)
                    glVertex3f(i * self.unitsize, 0, j * self.unitsize)
                    glNormal3f(1, 0, 0)
                    glTexCoord2f(0.,0.)
                    glVertex3f(i * self.unitsize, self.height, j * self.unitsize)
                    glNormal3f(1, 0, 0)
                    glTexCoord2f(1.,0.)
                    glVertex3f(i * self.unitsize, self.height, (j + 1) * self.unitsize)
                    glNormal3f(1, 0, 0)
                    glTexCoord2f(1.,1.)
                    glVertex3f(i * self.unitsize, 0, (j + 1) * self.unitsize)
                    
                    
                    #North
                    glNormal3f(0, 0, -1)
                    glTexCoord2f(0.,1.)
                    glVertex3f((i + 1) * self.unitsize, 0, j * self.unitsize)
                    glNormal3f(0, 0, -1)
                    glTexCoord2f(0.,0.)
                    glVertex3f((i + 1) * self.unitsize, self.height, j * self.unitsize)
                    glNormal3f(0, 0, -1)
                    glTexCoord2f(1.,0.)
                    glVertex3f(i * self.unitsize, self.height, j * self.unitsize)
                    glNormal3f(0, 0, -1)
                    glTexCoord2f(1.,1.)
                    glVertex3f(i * self.unitsize, 0, j * self.unitsize)
                    
                    #East
                    glNormal3f(-1, 0, 0)
                    glTexCoord2f(0.,1.)
                    glVertex3f((i + 1) * self.unitsize, 0, (j + 1) * self.unitsize)
                    glNormal3f(-1, 0, 0)
                    glTexCoord2f(0.,0.)
                    glVertex3f((i + 1) * self.unitsize, self.height, (j + 1) * self.unitsize)
                    glNormal3f(-1, 0, 0)
                    glTexCoord2f(1.,0.)
                    glVertex3f((i + 1) * self.unitsize, self.height, j * self.unitsize)
                    glNormal3f(-1, 0, 0)
                    glTexCoord2f(1.,1.)
                    glVertex3f((i + 1) * self.unitsize, 0, j * self.unitsize)
                
                    #South
                    glNormal3f(0, 0, 1)
                    glTexCoord2f(0.,1.)
                    glVertex3f(i * self.unitsize, 0, (j + 1) * self.unitsize)
                    glNormal3f(0, 0, 1)
                    glTexCoord2f(0.,0.)
                    glVertex3f(i * self.unitsize, self.height, (j + 1) * self.unitsize)
                    glNormal3f(0, 0, 1)
                    glTexCoord2f(1.,0.)
                    glVertex3f((i + 1) * self.unitsize, self.height, (j + 1) * self.unitsize)
                    glNormal3f(0, 0, 1)
                    glTexCoord2f(1.,1.)
                    glVertex3f((i + 1) * self.unitsize, 0, (j + 1) * self.unitsize)
                    
                    
        glEnd()

        
    
    def DrawGems(self):
        """Draws the gems"""
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_DST_ALPHA)
        for i in self.gems:
            glPushMatrix()
            glTranslatef(i[0] + .5 * self.unitsize, .5 * self.height, i[1] + .5 * self.unitsize)
            glScalef(.35, .5, .35)
            glRotatef(self.gemangle, 0, 1, 0)
            glBegin(GL_TRIANGLES)
            
            glColor4f(1, 0, 0, 1)
            glNormal3f(0, 1, 0)
            glVertex3f(0 , .5 * self.height, 0)
            glNormal3f(-1, 0, 1)
            glVertex3f(-.5 * self.unitsize, 0, .5 * self.unitsize)
            glNormal3f(-1, 0, -1)
            glVertex3f(-.5 * self.unitsize, 0, -.5 * self.unitsize)
            
            glNormal3f(0, 1, 0)
            glVertex3f(0, .5 * self.height, 0)
            glNormal3f(-1, 0, -1)
            glVertex3f(-.5 * self.unitsize, 0, -.5 * self.unitsize)
            glNormal3f(1, 0, -1)
            glVertex3f(.5 * self.unitsize, 0, -.5 * self.unitsize)
            
            glNormal3f(0, 1, 0)
            glVertex3f(0 , .5 * self.height, 0)
            glNormal3f(1, 0, -1)
            glVertex3f(.5 * self.unitsize, 0, -.5 * self.unitsize)
            glNormal3f(1, 0, 1)
            glVertex3f(.5 * self.unitsize, 0, .5 * self.unitsize)
            
            glNormal3f(0, 1, 0)
            glVertex3f(0 , .5 * self.height, 0)
            glNormal3f(1, 0, 1)
            glVertex3f(.5 * self.unitsize, 0, .5 * self.unitsize)
            glNormal3f(-1, 0, 1)
            glVertex3f(-.5 * self.unitsize, 0, .5 * self.unitsize)
            
            glNormal3f(-1, 0, 1)
            glVertex3f(-.5 * self.unitsize, 0, .5 * self.unitsize)
            glNormal3f(-1, 0, -1)
            glVertex3f(-.5 * self.unitsize, 0, -.5 * self.unitsize)
            glNormal3f(0, -1, 0)
            glVertex3f(0 , -.5 * self.height, 0)
            
            glNormal3f(-1, 0, -1)
            glVertex3f(-.5 * self.unitsize, 0, -.5 * self.unitsize)
            glNormal3f(1, 0, -1)
            glVertex3f(.5 * self.unitsize, 0, -.5 * self.unitsize)
            glNormal3f(0, -1, 0)
            glVertex3f(0 , -.5 * self.height, 0)
            
            
            glNormal3f(1, 0, -1)
            glVertex3f(.5 * self.unitsize, 0, -.5 * self.unitsize)
            glNormal3f(1, 0, 1)
            glVertex3f(.5 * self.unitsize, 0, .5 * self.unitsize)
            glNormal3f(0, -1, 0)
            glVertex3f(0 , -.5 * self.height, 0)
            
            glNormal3f(1, 0, 1)
            glVertex3f(.5 * self.unitsize, 0, .5 * self.unitsize)
            glNormal3f(-1, 0, 1)
            glVertex3f(-.5 * self.unitsize, 0, .5 * self.unitsize)
            glNormal3f(0, -1, 0)
            glVertex3f(0 , -.5 * self.height, 0)
            
            glEnd()
            
            glPopMatrix()
        glDisable(GL_BLEND)
    
    def FindInfo(self):
        """Give me more information about the map."""
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == 'W':
                    self.walls.append([i * self.unitsize, j * self.unitsize])
            
                if self.map[i][j] == 'L':
                    self.lights.append([i * self.unitsize, j * self.unitsize])
                    self.gemcandidate.append([i * self.unitsize, j * self.unitsize])
                    self.clear += 1
                    
                if self.map[i][j] == 'S':
                    self.start = [i * self.unitsize, j * self.unitsize]
       
                if self.map[i][j] == 'E':
                    self.gemcandidate.append([i * self.unitsize, j * self.unitsize])
                    self.clear += 1
                

    def PlaceGems(self):
        """Go through and place the gems logically"""
        #print self.gemcandidate
        self.SetupMaterial()
        gemstoplace = int(self.clear / 32)
        
        i = 0
        while i < gemstoplace:
           
            index = int(random.random() * (len(self.gemcandidate) - i))
            self.gems.append(self.gemcandidate[index])
            self.gemcandidate.pop(index)
            i += 1
        
        
        
    def SetTexture(self, filename):
        self.SetupTextures()
        image = Image.open(filename)
        (ix, iy) = image.size
        data = image.tostring("raw","RGBX")

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    
    
    
            
class Crawler:
    """This class's main purpose is to handle collisions"""
    def __init__(self, camera, dungeon):
        self.camera = camera
        self.dungeon = dungeon
        self.forward = 1
        self.forwardchange = 1
        self.thrust = 1
        self.thrustchange = 1
        self.turn = 1
        self.turnchange = 1
        self.startposition = self.camera.GetStart()
        self.startposition.append(1)
        
        
        
    
    def WalkForward(self):
        gemstone = self.TestCollisions(0, 0, -self.forward, self.dungeon.gems)
        
        if gemstone != 0:
            self.RemoveGems(gemstone)
        
            
            
        
        if self.TestCollisions(0, 0, -self.forward, self.dungeon.walls) == 0:
            self.camera.Slide(0, 0, -self.forward)
            
        self.CycleSpeed()
        
        
    def WalkBackward(self):
        gemstone = self.TestCollisions(0, 0, self.forward, self.dungeon.gems)
        
        if gemstone != 0:
            self.RemoveGems(gemstone)
            
        if self.TestCollisions(0, 0, self.forward, self.dungeon.walls) == 0:
            self.camera.Slide(0, 0, self.forward)
        self.CycleSpeed()
        
    def StrafeLeft(self):
        
        gemstone = self.TestCollisions(-self.thrust, 0, 0, self.dungeon.gems)
        
        if gemstone != 0:
            self.RemoveGems(gemstone)
        
        if self.TestCollisions(-self.thrust, 0, 0, self.dungeon.walls) == 0:
            self.camera.Slide(-self.thrust, 0, 0)
        self.CycleSpeed()
        
    def StrafeRight(self):
        gemstone = self.TestCollisions(self.thrust, 0, 0, self.dungeon.gems)
        
        if gemstone != 0:
            self.RemoveGems(gemstone)
        
        if self.TestCollisions(self.thrust, 0, 0, self.dungeon.walls) == 0:
            self.camera.Slide(self.thrust, 0, 0)
        self.CycleSpeed()
        
    def TurnLeft(self):
        self.camera.Yaw(self.turn)
        self.CycleSpeed()
        
    def TurnRight(self):
        self.camera.Yaw(-self.turn)
        self.CycleSpeed()
        
    def CycleSpeed(self):
        """Okay, so this is my attempt to make movement a bit more realistic.
           Speed of walking, strafing and turning oscilates."""
        if self.forward <= 4:
            self.forwardchange = .2
        if self.forward >= 7:
            self.forwardchange = -.2
        
        if self.forwardchange >= 0:
            self.forwardchange += .2
            self.forward += self.forwardchange
            
        if self.forwardchange < 0:
            self.forwardchange -= .2
            self.forward += self.forwardchange
        
        
        if self.thrust <= 2:
            self.thrustchange = .2
        if self.thrust >= 5:
            self.thrustchange = -.2
        
        if self.thrustchange >= 0:
            self.thrustchange += .2
            self.thrust += self.thrustchange
            
        if self.thrustchange < 0:
            self.thrustchange -= .2
            self.thrust += self.thrustchange
        
        if self.turn <= 3:
            self.turnchange = .4
        if self.turn >= 3:
            self.turnchange = -.1
        
        if self.turnchange >= 0:
            self.turnchange += .2
            self.turn += self.turnchange
            
        if self.turnchange < 0:
            self.turnchange -= .2
            self.turn += self.turnchange
    
    def RemoveGems(self, gemstone):
        self.dungeon.gems.remove(gemstone)
        self.dungeon.regem = 1
        if self.dungeon.gemlist is not None:
            glDeleteLists(self.dungeon.gemlist, 1)
        
        if windows == 1:
            PlaySound(file, SND_FILENAME|SND_ASYNC|SND_NOSTOP)
        
        #More code from internet
        else:
            s = waveOpen('tada.wav','rb')
            (nc,sw,fr,nf,comptype, compname) = s.getparams( )
            dsp = ossOpen('/dev/dsp','w')
            try:
                from ossaudiodev import AFMT_S16_NE
            except ImportError:
                if byteorder == "little":
                    AFMT_S16_NE = ossaudiodev.AFMT_S16_LE
                else:
                    AFMT_S16_NE = ossaudiodev.AFMT_S16_BE
            dsp.setparameters(AFMT_S16_NE, nc, fr)
            data = s.readframes(nf)
            s.close()
            dsp.write(data)
            dsp.close()
    
    def TestCollisions(self, x, y, z, set):
        buffer = 0
        currentmatrix = numpy.identity(4, 'f')
        currentmatrix[3][0] = x
        currentmatrix[3][1] = y
        currentmatrix[3][2] = z
        
        currentpoint = self.camera.GetEye()
        
        #for i in range(len(currentpoint)):
        #    currentpoint[i] = round(currentpoint[i], 2)
        
            
        newpoint = self.camera.CalcSlide(x, y, z)
        
            
        
       
        
        for i in set:
            #print "Wall: ", i
            if newpoint[0] + buffer <= i[0] + self.dungeon.unitsize or newpoint[0] - buffer <= i[0] + self.dungeon.unitsize:
                if newpoint[0] + buffer >= i[0] or newpoint[0] - buffer >= i[0]:
                    if newpoint[2] + buffer <= i[1] + self.dungeon.unitsize or newpoint[2] - buffer <= i[1] + self.dungeon.unitsize:
                        if newpoint[2] + buffer >= i[1] or newpoint[2] - buffer >= i[1]:
                            #print "Collision!"
                            return i
        
        
        return 0
    
            