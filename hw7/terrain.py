"""
Title: Random Terrain Simulator
Author: Krieghan J. Riley
Date: May 19, 2006
Purpose: This program's purpose is to randomly generate terrain in conformance with the 
         Diamond Star algorithm.  The terrain may be viewed either with a wireframe or with
         a shaded skin.

Changes from Hard Copy:
        I made a number of changes to the code after I submitted the hard copy.  I discovered that
        the code was executing very slowly, and wanted to know why.  After doing some digging, I
        found that the KillRepeats function was operating at approximately Order-N-Squared complexity,
        and for N approaching 1024 X 1024, execution was prohibitive.  I initially made KillRepeats
        more efficient by making the assumption that its arguments were sorted.  After thinking more
        on it, however, I decided that executing KillRepeats at all was taking too long.  I inserted
        a few conditionals into the Diamond and Square functions so that we'd never push repeat points
        into the list.  The code now executes astronomically faster.
        
        Still, you'll have problems as the number of iterations increases.  Forming the matrix at all
        is still N^2, though I think there should be some way around that.  On my computer with 3.0 GHz
        and 2 Gig of memory, it still drags a little on the 1024 X 1024.  If you turn skin on for this
        terrain, OpenGL will actually run out of memory (I think because of all the shading going on).
        I can actually get 1024 X 1024 wireframe, as well as 2048 X 2048 wireframe.  On the Linux machines, 
        however, you may have to be content with a smaller terrain.  Also, as always, be aware that the
        timer value isn't necessarily optimized for whatever you're running this on.
         
Based on template.py from C. Andrews 2006

"""

import wx
from wx.glcanvas import GLCanvas
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

#The terrain and terrainpoint classes perform the Diamond Square algorithm and do much of the book keeping.
from dsquare import *

#The same camera class from hw6.
from camera import *




class GLTerrain(GLCanvas):
    """Handles the viewing of our terrain"""
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we can properly initialize the canvas"""
        GLCanvas.__init__(self, parent,-1)
        self.init = 0
        glEnable(GL_NORMALIZE)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TIMER, self.HandleTime)
        
        #Create the terrain, run the algorithm and find all the normals
        self.terrain = Terrain(2, [0, 0, 0, 0])
        self.terrain.Seed()
        self.PushAllNormals()
        
        #Get the height range
        [self.min, self.max] = self.GetHeightRange()
        
        self.wirelist = None
        self.skinlist = None
        
        #Instantiate the camera
        self.camera = Camera([25, 25, 25], [1, 1, 1])
        
        #Start the timer.  The value here may be adjusted for peak peformance for whatever machine you're running this on.
        self.timer = wx.Timer(self)
        self.timer.Start(10)
        
        self.spinangle = 0.0
        self.spinvelocity = 0.0
        
        #Start with a wireframe
        self.skinmode = -1
        
        self.reskin = 1
        self.rewire = 1
        
        return


    def SetupView(self):
        """This function does the actual work to setup the window so we can draw in it. 
        Since we're dealing with a moving camera and world, we are not obliged to set the 
        dimensions of the world window and viewport based on anything in the world.  Therefore, 
        the only hard part here is maintaining aspect ratio.
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


    def SetupLights(self):
        """Sets up the Light in the world"""
        glShadeModel(GL_SMOOTH)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))
        glLightfv(GL_LIGHT0, GL_POSITION, (0,0,1,0))

    def SetupMaterial(self):
        """Sets the material properties of the terrain"""
        glMaterialfv(GL_FRONT, GL_AMBIENT, (.10588, .058824, .113725, 1))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (.427451, .470588, .541176, 1))
        #glMaterialfv(GL_FRONT, GL_SPECULAR,(.3333,.3333,.521569, 1))
        glMaterialfv(GL_FRONT, GL_SHININESS, 9.84615)        
        glEnable(GL_COLOR_MATERIAL)

    def InitGL(self):
        """This function does some of the one time OpenGL initialization we need to perform.         
        """
        self.SetCurrent()
        glClearColor(0.0,0.0,0.0,0.0); # set clear color to black
        glEnable(GL_DEPTH_TEST)
        self.SetupView()
        self.SetupLights()
        self.SetupMaterial()
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
        """This is the main drawing function. This function tests for the 
           skinmode and performs its display based on that.  Display lists are
           formed of both the wireframe and the shade-skinned terrains.  Spinning
           must be done here if at all
        """
        self.SetCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        
        
        glMatrixMode(GL_MODELVIEW)
        
        glLoadIdentity()                
        
        glMultMatrixf(self.camera.matrix)                 
                       
                        
        #self.DrawAxis()
        
        #We use shift here because we want the terrain to be centered on the origin (it makes rotation much easier)
        shift = int((self.terrain.GetSize()) / 2) + 1
        
        #If we have an spin angle, we rotate the picture by that amount.
        if self.spinangle != 0:
            glRotatef(self.spinangle, 0, 1, 0)
        
        #Skin is wireframed
        if self.skinmode == -1:
            glDisable(GL_LIGHTING)
            if self.rewire == 1:
                self.rewire = 0
                if self.wirelist is None:
                    self.wirelist = glGenLists(1)
                glNewList(self.wirelist, GL_COMPILE_AND_EXECUTE)
                "Forming Wire Terrain"
                    
                #self.DrawNormals()
                glColor3f(1, 1, 1)
                i = -shift + 1
                while i < shift:
                    
                    glBegin(GL_LINE_STRIP)
                    j = -shift + 1
                    while j < shift:
                    
                        height = self.terrain.GetMatrixElement(i + shift - 1, j + shift - 1).GetHeight()
                        glColor3f(*self.GetColor(height))
                        glVertex3f(i, height, j)
                        j += 1
                    glEnd()
            
                    i += 1
        
                i = -shift + 1
                while i < shift:
                    glBegin(GL_LINE_STRIP)
                    j = -shift + 1
                    while j < shift:
                        height = self.terrain.GetMatrixElement(j + shift - 1, i + shift - 1).GetHeight()
                        glColor3f(*self.GetColor(height))
                        glVertex3f(j, height, i)
                        j += 1
            
                    i += 1
                    glEnd()
                glEndList()
                print "Done Forming Wire Terrain"
            else:          
                
                glCallList(self.wirelist)
        
        #Skin is the shaded version
        if self.skinmode == 1:
            glEnable(GL_LIGHTING)
            if self.reskin == 1:
                self.reskin = 0
                if self.skinlist is None:
                    self.skinlist = glGenLists(1)
                glNewList(self.skinlist, GL_COMPILE_AND_EXECUTE)
                print "Forming Skin Terrain"
                i = -shift + 1
                glBegin(GL_TRIANGLES)
                while i < shift - 1:
                    
                    j = -shift + 1
                    while j < shift - 1:
                        
                        height = self.terrain.GetMatrixElement(i + shift - 1, j + shift - 1).GetHeight()
                        glNormal3f(*self.terrain.GetMatrixElement(i + shift - 1, j + shift - 1).GetNormal())                        
                        glColor3f(*self.GetColor(height))
                        glVertex3f(i, height, j)
                        height = self.terrain.GetMatrixElement(i + 1 + shift - 1, j + shift - 1).GetHeight()
                        glNormal3f(*self.terrain.GetMatrixElement(i + 1 + shift - 1, j + shift - 1).GetNormal())
                        glColor3f(*self.GetColor(height))
                        glVertex3f(i + 1, height, j)
                        height = self.terrain.GetMatrixElement(i + shift - 1, j + 1 + shift - 1).GetHeight()
                        glNormal3f(*self.terrain.GetMatrixElement(i + shift - 1, j + 1 + shift - 1).GetNormal())
                        glColor3f(*self.GetColor(height))
                        glVertex3f(i, height, j + 1)
                        height = self.terrain.GetMatrixElement(i + shift - 1, j + 1 + shift - 1).GetHeight()
                        glNormal3f(*self.terrain.GetMatrixElement(i + shift - 1, j + 1 + shift - 1).GetNormal())
                        glColor3f(*self.GetColor(height))
                        glVertex3f(i, height, j + 1)
                        height = self.terrain.GetMatrixElement(i + 1 + shift - 1, j + shift - 1).GetHeight()
                        glNormal3f(*self.terrain.GetMatrixElement(i + 1 + shift - 1, j + shift - 1).GetNormal())
                        glColor3f(*self.GetColor(height))
                        glVertex3f(i + 1, height, j)
                        height = self.terrain.GetMatrixElement(i + 1 + shift - 1, j + 1 + shift - 1).GetHeight()
                        glNormal3f(*self.terrain.GetMatrixElement(i + 1 + shift - 1, j + 1 + shift - 1).GetNormal())
                        glColor3f(*self.GetColor(height))
                        glVertex3f(i + 1, height, j + 1)
                        j += 1
                    i += 1
                glEnd()
                glEndList()
                print "Done Forming Skin Terrain"
            else:
                
                glCallList(self.skinlist)
                
            
                    
                    
        self.SwapBuffers()

        return        

    def DoCameraChange(self, id, value):
        """This function is called by the button click handler in hw7.py."""
        
        
        if id == 0:
            self.camera.ChangeForward(value)
        if id == 1:
            self.camera.ChangePitch(value)
        if id == 2:
            self.camera.ChangeYaw(value)
        self.OnDraw()
        
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
        
        
        
        if self.spinvelocity != 0:
            
            self.spinangle = round((self.spinangle + self.spinvelocity) % 360, 2)
            
            
          
        self.OnDraw()
        event.Skip()
        
    def AddSpin(self, spin):    
        """If the user increases spin velocity, we must add that to the
           spinvelocity variable we're keeping"""
           
        self.spinvelocity = round(self.spinvelocity + spin, 2)
        
        
    def DoDisplay(self, iterations):
        """If the user clicks on display, we reform the terrain."""
        if iterations < 2:
            print "Iteration value must be larger than 2"
            return -1
            
        self.terrain = Terrain(iterations, [0, 0, 0, 0])
        self.terrain.Seed()
        self.PushAllNormals()
        
        [self.min, self.max] = self.GetHeightRange()
        
        if self.wirelist is not None:
            glDeleteLists(self.wirelist, 1)
            self.rewire = 1
        if self.skinlist is not None:
            glDeleteLists(self.skinlist, 1)                
            self.reskin = 1
        
        
    
    def ChangeSkin(self):
        """Flips the skin mode"""
        self.skinmode *= -1


    def PushAllNormals(self):
        """Parses the terrain map finding the cross product of all the triangles and pushing the appropriate
           vector into each point.  As a final step, we call each point to find the average vector"""

        print "Calculating Normals for a ", len(self.terrain.GetMatrix()), " X ", len(self.terrain.GetMatrix()), " terrain"
        
        i = 0
        while i < len(self.terrain.GetMatrix()) - 1:
            j = 0
            while j < len(self.terrain.GetMatrix()) - 1:
                vector1 = [1, self.terrain.GetMatrixElement(i + 1, j).GetHeight() - self.terrain.GetMatrixElement(i, j).GetHeight(), 0]
                vector2 = [0, self.terrain.GetMatrixElement(i, j + 1).GetHeight() - self.terrain.GetMatrixElement(i, j).GetHeight(), 1]
                
                
                cross = self.CrossProduct(vector2, vector1)
                #print vector2, vector1, cross
                
                self.terrain.GetMatrixElement(i, j).PushNormal(cross)
                self.terrain.GetMatrixElement(i + 1, j).PushNormal(cross)
                self.terrain.GetMatrixElement(i, j + 1).PushNormal(cross)
                
                vector1 = [-1, self.terrain.GetMatrixElement(i + 1, j).GetHeight() - self.terrain.GetMatrixElement(i + 1, j + 1).GetHeight(), 0]
                vector2 = [0, self.terrain.GetMatrixElement(i, j + 1).GetHeight() - self.terrain.GetMatrixElement(i + 1, j + 1).GetHeight(), -1]
                cross = self.CrossProduct(vector2, vector1)
                
                self.terrain.GetMatrixElement(i + 1, j + 1).PushNormal(cross)
                self.terrain.GetMatrixElement(i + 1, j).PushNormal(cross)
                self.terrain.GetMatrixElement(i, j + 1).PushNormal(cross)
            
                j += 1
            i += 1
        
        print "Averaging Normals"
        for i in self.terrain.GetMatrix():
            for j in i:
                j.CalcNormal()
        
        print "Done Averaging Normals"
        
        print "Done Calculating Normals"
                
    def CrossProduct(self, a, b):
        """Just a Cross Product function for Normal Vectors"""
        
        return [(a[1] * b[2] - a[2] * b[1]), (a[2] * b[0] - a[0] * b[2]), (a[0] * b[1] - a[1] * b[0])]
    
    def DrawNormals(self):
        """Draws the normal vectors for testing purposes"""
        shift = int((self.terrain.GetSize()) / 2) + 1
        glColor3f(1, 0, 0)
        i = -shift + 1
        glBegin(GL_LINES)
        while i < shift - 1:
            j = -shift + 1
            while j < shift - 1:
                        
                   
                normal = self.terrain.GetMatrixElement(i + shift - 1, j + shift - 1).GetNormal()
                #print normal
                glVertex3f(i, self.terrain.GetMatrixElement(i + shift - 1, j + shift - 1).GetHeight(), j)
                glVertex3f(i + normal[0], self.terrain.GetMatrixElement(i + shift - 1, j + shift - 1).GetHeight() + normal[1], j + normal[2])
                normal = self.terrain.GetMatrixElement(i + 1 + shift - 1, j + shift - 1).GetNormal()
                glVertex3f(i + 1, self.terrain.GetMatrixElement(i + 1 + shift - 1, j + shift - 1).GetHeight(), j)
                glVertex3f(i + 1 + normal[0], self.terrain.GetMatrixElement(i + 1 + shift - 1, j + shift - 1).GetHeight() + normal[1], j + normal[2])
                normal = self.terrain.GetMatrixElement(i + shift - 1, j + 1 + shift - 1).GetNormal()
                glVertex3f(i, self.terrain.GetMatrixElement(i + shift - 1, j + 1 + shift - 1).GetHeight(), j + 1)
                glVertex3f(i + normal[0], self.terrain.GetMatrixElement(i + shift - 1, j + 1 + shift - 1).GetHeight() + normal[1], j + 1 + normal[2])
                normal = self.terrain.GetMatrixElement(i + shift - 1, j + 1 + shift - 1).GetNormal()
                glVertex3f(i, self.terrain.GetMatrixElement(i + shift - 1, j + 1 + shift - 1).GetHeight(), j + 1)
                glVertex3f(i + normal[0], self.terrain.GetMatrixElement(i + shift - 1, j + 1 + shift - 1).GetHeight() + normal[1], j + 1 + normal[2])
                normal = self.terrain.GetMatrixElement(i + 1 + shift - 1, j + shift - 1).GetNormal()
                glVertex3f(i + 1, self.terrain.GetMatrixElement(i + 1 + shift - 1, j + shift - 1).GetHeight(), j)
                glVertex3f(i + 1 + normal[0], self.terrain.GetMatrixElement(i + 1 + shift - 1, j + shift - 1).GetHeight() + normal[1], j + normal[2])
                normal = self.terrain.GetMatrixElement(i + 1 + shift - 1, j + 1 + shift - 1).GetNormal()
                glVertex3f(i + 1, self.terrain.GetMatrixElement(i + 1 + shift - 1, j + 1 + shift - 1).GetHeight(), j + 1)
                glVertex3f(i + 1 + normal[0], self.terrain.GetMatrixElement(i + 1 + shift - 1, j + 1 + shift - 1).GetHeight() + normal[1], j + 1 + normal[2])
                j += 1
            i += 1
        glEnd()
    
    def GetHeightRange(self):
        """Finds the min and max height values of the terrain for coloring purposes"""
        min = self.terrain.GetMatrixElement(0, 0).GetHeight()
        max = min
        i = 0
        while i < len(self.terrain.GetMatrix()) - 1:
            j = 0
            while j < len(self.terrain.GetMatrix()) - 1:
                if self.terrain.GetMatrixElement(i, j).GetHeight() < min:
                    min = self.terrain.GetMatrixElement(i, j).GetHeight()
                if self.terrain.GetMatrixElement(i, j).GetHeight() > max:
                    max = self.terrain.GetMatrixElement(i, j).GetHeight()
                j += 1
            i += 1
        
        return [min, max]
                
    
    def GetColor(self, height):
        """Gets the appropriate shade of color for the terrain based on a scaled
           height.  At the last minute, I added more to this function so that we'd not only
           have green, but blue, brown and white.  Because I added this functionality at the
           end of the project, there are some parts about it that I'm not happy about.  In a 
           perfect world, I would have been able to make blue flow into green into brown into
           gray into white.  It's not a perfect world, so at each level the color begins at the
           lowest color level (that is, black).  It can look a little odd, but I think it looks
           much better than my original function with only green."""
           
        distance = self.max - self.min
        if distance == 0:
            self.max = 10
            self.min = 0
        colorscore = (height - self.min) / distance
        
        if colorscore < .2:
            colorscore = colorscore / .18
            return [0, 0, colorscore + .2]
        
        if colorscore > .2 and colorscore < .6:        
            colorscore = (colorscore - .2) / .4
            return [0, colorscore, 0]
        
        if colorscore > .6 and colorscore < .8:
            colorscore = ((colorscore - .6) / .2)
            return [colorscore, .7304 * colorscore, 0]
        
        if colorscore > .8:
            colorscore = (colorscore - .8) / .2
            return [colorscore, colorscore, colorscore]
        
    
        