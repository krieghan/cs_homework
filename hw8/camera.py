import numpy
import math

class Camera:                        
    """This class handles the camera, which allows us to change our
    point of view in the world"""
    
    def __init__(self, eyelist, looklist, uplist = [0, 1, 0]):
        self.forward = 0
        self.pitch = 0
        self.yaw = 0
        self.roll = 0
        
        self.startposition = eyelist
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
    
    def GetEye(self):
        return self.eyelist
    
    def GetStart(self):
        return self.startposition
    
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


    def CalcSlide(self, delU, delV, delN):
        eye = []
        eye.append(delU * self.u[0] + delV * self.v[0] + delN * self.n[0])
        eye.append(delU * self.u[1] + delV * self.v[1] + delN * self.n[1])
        eye.append(delU * self.u[2] + delV * self.v[2] + delN * self.n[2])
        
        return [self.eyelist[0] + eye[0], self.eyelist[1] + eye[1], self.eyelist[2] + eye[2]]

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
    
    
