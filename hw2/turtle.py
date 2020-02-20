"""
Title:      Fractal Turtles
Author:     Krieghan J. Riley
Date:       April 6, 2006
Purpose:    The GLPane class in this file modifies C. Andrews' template.py (2006).  
            Basically, we're handed six values - # of iterations, an angle, a seed string, and
            Production Rules for F, X and Y.  We then recurse over the seed string making changes
            supplied by the production rules.  At the end, we use 'F' as a forward command, '+' as a
            'turn by the angle' command, '-' as a 'turn by the negative angle' command, '[' as a 
            'push current point and heading onto the stack' command and ']' as a 'pop current point
            and heading off of the stack and jump there' command.  In the end, we have what is usually
            a very cool self-similar graphic.

Regrets:    I regret not farming out duties in this project to other classes.  Obviously, these projects
            are going to get more and more complex, and simply putting everything into the GLPane class
            is getting kind of tacky (and not very object-oriented at all).  But, to my knowledge everything
            works as prescribed and I am up against the drop-dead-line right now, so I don't want to 
            screw anything up by overediting.          

"""

import wx
from wx.glcanvas import GLCanvas
#from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math




class GLPane(GLCanvas):
    """Basic template for a GLCanvas that can do simple 2D OpenGL drawing"""
    
    #These six variables hold the input entered by the user
    iterations = 0
    angle = 0           #measured in degrees
    seedstring = ""
    f = ""
    x = ""
    y = ""
    
    #After we're done recursing over the production values in the string, this is the value we get
    finalstring = ""
    
    #The direction we're currently moving (measured in degrees)
    currentheading = 0
    
    #The starting place for the graphic
    startingpoint = [100, 100]
    
    #The current point that we're at.
    currentpoint = startingpoint
    
    #The length of each line, passed to NextPoint (doesn't really matter, since we're zooming
    length = 1
    
    #These four values hold the boundaries of the image for our SetupView
    maxleft = currentpoint[0]
    maxright = currentpoint[0] + 100
    maxtop = currentpoint[1] + 100
    maxbottom = currentpoint[1]
    
    #Of course, we need a stack to handle the [ and ] 
    stack = []
    
    def __init__(self, parent):
        """This needs to be given the parent in the GUI hierarchy so we
        can properly initialize the canvas"""
        GLCanvas.__init__(self, parent,-1)
        self.init = 0


        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        return


    def SetupView(self):
        """This function does the actual work to setup the window so we can 
        draw in it.  Most of its task is going to be sizing the Viewport to
        maintain aspect ratio and sizing the World Window to achieve the 
        maximum possible zoom
        """
        size = self.GetClientSizeTuple()
        height = self.maxtop - self.maxbottom
        width = self.maxright - self.maxleft
        
        #The ratio of the width to the height in the client-area
        screenratio = float(size[0]) / float(size[1])
        
        #The ratio of the world window.  Because of divide-by-0, we have to make a special-case assignment
        if height == 0 or width == 0:
            ratio = screenratio
        else:
            ratio = width / height

        #Should seem familiar, since we did it in class...
        if ratio > screenratio:
            glViewport(0, (size[1] - (size[0] / ratio)) / 2, size[0], size[0] / ratio)
        if ratio < screenratio:
            glViewport((size[0] - size[1] * ratio) / 2, 0, size[1] * ratio, size[1])
        
        
        #I need to find an appropriate border value.  It's scaled by the client-area because the world-window zooms, thus skewing any normal border given.
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
        """This function does some of the one time OpenGL initialization we need to perform. 
        Again, we'll describe this in more detail later.
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

        
    def PrepareBoundaries(self):
        """I need to determine the boundaries of the image before SetView.  
        I thus pre-parse the string (ugly, yes, but I found that I couldn't 
        SetView after drawing the image).
        """
        
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
        
            #Yes, for the special case where the last point is actually a boundary, we need to do this post-check
            if self.maxleft > self.currentpoint[0]:
                self.maxleft = self.currentpoint[0]
            if self.maxright < self.currentpoint[0]:
                self.maxright = self.currentpoint[0]
            if self.maxbottom > self.currentpoint[1]:
                self.maxbottom = self.currentpoint[1]
            if self.maxtop < self.currentpoint[1]:
                self.maxtop = self.currentpoint[1]        
                
        #After parsing the string, we set the heading and currentpoint back to their original values.
        self.currentheading = 0
        self.currentpoint = self.startingpoint


    def OnDraw(self):
        """This is the main drawing function. It does the work of plotting the lines based on the 
        characters in finalstring.
		"""
        self.SetCurrent()

        glClear(GL_COLOR_BUFFER_BIT)

        glBegin(GL_LINES)

        glColor3f(1.0, 1.0, 1.0)
        
        
        #Just in case these aren't set back to their starting place yet...
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
        """This gets called by the button-handler in hw2.py.  It's passed
           the values entered by the user.  It then proceeds to generate the
           finalstring, setup the view, and draw the picture
        """
        
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
        """Recursive function that replaces F, X and Y by their production values.
           I use lower() for each replacement because I need to keep track of what
           variables are still validly replaceable on this level (If I replaced
           F by XY, I wouldn't want to replace X or Y with anything until the next
           level down).  Everything is eventually capitalized again.
        """
            
        if i <= 0:
            return string
		
        string = string.replace("F", (self.f).lower())        
        string = string.replace("X", (self.x).lower())
        string = string.replace("Y", (self.y).lower())
        
        
        string = string.upper()
        string = self.GenerateString(i - 1, string)

        return string
        
    def NextPoint(self, currentpoint, length, angle):
        """This function determines the next point based on the
        current point, the distance between the next point and the
        current point, and the heading
        """
        x = length * math.degrees(math.cos(math.radians(angle)))
        y = length * math.degrees(math.sin(math.radians(angle)))
        return [currentpoint[0] + x, currentpoint[1] + y]