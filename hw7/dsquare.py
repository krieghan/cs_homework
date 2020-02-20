import random
import math


class TerrainPoint:
    """This class keeps track of each point on the terrain.  Having a class for this means
       that each terrain may determine its own height and normal vector based on outside
       information
    """
    
    def __init__(self, height, gauss):
        self.adders = []
        self.normals = []
        self.averagenormal = []
        self.gauss = gauss
        self.height = height
    
    def GetHeight(self):
        return self.height
    
    def SetHeight(self, height):
        self.height = height
    
    def GetGauss(self):
        return self.gauss
        
    def SetGauss(self, gauss):
        self.gauss = gauss
       
    def GetAdders(self):
        return self.adders
    
    def PushAdder(self, adder):
        """In determining each point's height, the dsquare algorithm pushes
           other points heights and averages them.  This function does the 
           pushing"""
           
        self.adders.append(adder)

        
    def GetNormal(self):
        return self.averagenormal
    
    def PushNormal(self, normal):
        """In determining each point's normal, we push the normal of each triangle that
        this point is a part of and average each component"""
        
        self.normals.append(normal)
        
    def CalcHeight(self):
        """Average the heights that have been pushed"""
        sum = float(0)
        #print self.adders
        for i in self.adders:
            sum += i
            #print i
        
        
        average = sum / len(self.adders)    
        
        #print self.gauss
        
        self.height = random.gauss(average, self.gauss)
        
        #self.height = random.gauss(average, 0)
        
        #rand = random.random() * (self.range[1] - self.range[0]) + self.range[0]
        #self.height = average + rand
        
    def CalcNormal(self):
        """Average the normals that have been pushed"""
        
        
        sum = self.normals[0]
        #print self.normals[0]
        
        for normal in range(1, len(self.normals)):
            #print self.normals[normal]
            for element in range(len(self.normals[normal])):
                sum[element] += self.normals[normal][element]
        
        for element in range(len(sum)):
            sum[element] /= len(self.normals)
        
        
        self.averagenormal = sum
        
        
        #print "Average: ", self.averagenormal
        #print ""
        
        
class Terrain:
    """This class keeps track of a terrain and does the basic work of running
       the dsquare algorithm"""
       
    def __init__(self, sizeiteration = 0, corners = [0, 0, 0, 0]):
        self.matrix = []
        self.points = []
        self.sizeiteration = sizeiteration
        
        self.size = int(math.pow(2, sizeiteration) + 1)
        
       
        print "Building Matrix: ", self.size, " X ", self.size, " = ", self.size ** 2
        for i in range(self.size):
            self.matrix.append([])
            for j in range(self.size):
                self.matrix[i].append(TerrainPoint(0, [-1, 1]))

        print "Matrix Complete"
        
        #Seed the terrain with the four corners
        self.matrix[0][0].SetHeight(corners[0])
        self.matrix[0][self.size - 1].SetHeight(corners[1])
        self.matrix[self.size - 1][self.size - 1].SetHeight(corners[2])
        self.matrix[self.size - 1][0].SetHeight(corners[3])
    
    def GetSize(self):
        return self.size
    
    def GetMatrix(self):
        return self.matrix        

    def GetMatrixElement(self, i, j):
        return self.matrix[i][j]
        
    def Seed(self):
        """Iterate through the terrain using the dsquare algorithm and find the
           heights of all points"""
           
        self.points.append([0, 0])
        self.points.append([0, self.size - 1])
        self.points.append([self.size - 1, self.size - 1])
        self.points.append([self.size - 1, 0])
        
        #The starting value for Gauss.  Note that we can change the denominator.  Increasing it makes the terrain flatter, while
        #decreasing it makes the terrain more jagged.  Prof. Andrews (that would be you) suggested a value of 5 for the denominator.
        #Based on a very short survey, I like it around 5 as well.
        
        gauss = (math.pow(2, self.sizeiteration) + 1) / 5.0
        
        #math.pow(self.sizeiteration, 2)
        
        for i in range(self.sizeiteration):
            #Distance is the number of units from a point to the next point in the search (ie, the distance from each of the
            #Four corners to the center point, or the distance from the center point to any of the next points)
            distance = int(math.pow(2, (self.sizeiteration - i) - 1))                
            self.__Square(distance, gauss)
            self.__Diamond(distance, gauss)
            gauss /= 2
            
        print "Algorithm Complete"
    
    def __Square(self, distance, gauss):
        """This function runs the square step, finding the height of all
           points for the next iteration"""
        temp = []
        
        print "Square distance:", distance
        
        #gauss = (math.pow(2, self.sizeiteration) + 1) / math.pow(self.sizeiteration, 2)
        #print self.sizeiteration, self.sizeiteration ^ 2
        
        #For each point that the algorithm has already hit
        for i in self.points:
            height = self.matrix[i[0]][i[1]].GetHeight()
            #We want to visit all points that this point contributes a height to, pushing this point's height into
            #their list of heights to average
            if i[0] + distance < self.size:                
                if i[1] + distance < self.size:                    
                    new1 = [i[0] + distance, i[1] + distance]
                    temp.append(new1)
                    #print "Push New1: ", new1
                    self.matrix[new1[0]][new1[1]].PushAdder(height)
                    self.matrix[new1[0]][new1[1]].SetGauss(gauss)
                if i[1] - distance >= 0:
                    new2 = [i[0] + distance, i[1] - distance]
                    if not (new2[0] - distance >= 0 and new2[1] - distance >= 0):
                        #print "Push New2: ", new2
                        temp.append(new2)
                    self.matrix[new2[0]][new2[1]].PushAdder(height)
                    self.matrix[new2[0]][new2[1]].SetGauss(gauss)
            if i[0] - distance >= 0:
                
                if i[1] + distance < self.size:
                    new3 = [i[0] - distance, i[1] + distance]
                    if not ((new3[0] - distance >= 0 and new3[1] - distance >= 0) or (new3[0] - distance >= 0 and new3[1] + distance < self.size)):
                        temp.append(new3)
                        #print "Push New3: ", new3
                    self.matrix[new3[0]][new3[1]].PushAdder(height)
                    self.matrix[new3[0]][new3[1]].SetGauss(gauss)
                if i[1] - distance >= 0:
                    new4 = [i[0] - distance, i[1] - distance]
                    if not ((new4[0] - distance >= 0 and new4[1] - distance >= 0) or (new4[0] - distance >= 0 and new4[1] + distance < self.size) or (new4[0] + distance < self.size and new4[1] - distance >= 0)):
                        temp.append(new4)
                        #print "Push New4: ", new4
                    self.matrix[new4[0]][new4[1]].PushAdder(height)
                    self.matrix[new4[0]][new4[1]].SetGauss(gauss)
        
        
        #Temp keeps track of the points we hit on this turn, and there are going to be repeats.
        #So, make them go away.
        
        
        
        
        #For each point that we hit, find the height by averaging all pushed adders.  
        #Append all points that we hit on the points[] list
        print "Calcing Height"
        for i in temp:
            self.matrix[i[0]][i[1]].CalcHeight()    
            self.points.append(i)
        print "Heights calced"
        
        
    
    def __Diamond(self, distance, gauss):
        """Much like __Square, but this step goes straight up, down, left and 
           right for its next points"""
           
        temp = []
        
        print "Diamond distance:", distance
        #This value is used for the stdev in the average function for each point that we hit.  Each point could have a different
        #stdev for determining the average, but that isn't the case right now.
        
        #gauss = (math.pow(2, self.sizeiteration) + 1) / math.pow(self.sizeiteration, 2)     
       
        
        for i in self.points:
            flag = 0
            height = self.matrix[i[0]][i[1]].GetHeight()
            if i[1] + distance < self.size:
                new1 = [i[0], i[1] + distance]
                
                temp.append(new1)                
                self.matrix[new1[0]][new1[1]].PushAdder(height)
                self.matrix[new1[0]][new1[1]].SetGauss(gauss)
            if i[0] + distance < self.size:
                new2 = [i[0] + distance, i[1]]
                if not new2[1] - distance >= 0:
                    temp.append(new2)                    
                   
                self.matrix[new2[0]][new2[1]].PushAdder(height)
                self.matrix[new2[0]][new2[1]].SetGauss(gauss)
            if i[1] - distance >= 0:
                new3 = [i[0], i[1] - distance]
                if not (new3[1] - distance >= 0 or new3[0] - distance >= 0):
                    temp.append(new3)
                    
                self.matrix[new3[0]][new3[1]].PushAdder(height)
                self.matrix[new3[0]][new3[1]].SetGauss(gauss)
            if i[0] - distance >= 0:
                new4 = [i[0] - distance, i[1]]
                if not (new4[1] - distance >= 0 or new4[0] - distance >= 0 or new4[1] + distance < self.size):
                    temp.append(new4)
                    
                    
                self.matrix[new4[0]][new4[1]].PushAdder(height)
                self.matrix[new4[0]][new4[1]].SetGauss(gauss)

        
           
        
        print "Calcing Heights"
        for i in temp:
            self.matrix[i[0]][i[1]].CalcHeight()
            self.points.append(i)
        print "Heights Calced"
         
         
    def KillRepeats(self, list):
        """This function is no longer part of my program, and is here for nostalgia's sake (and because
           it's in my program listing).  The fact of the matter is that this thing takes just too damn
           long as the size increases (it's not N-Squared, but it still takes time to chug through).  
           Instead, I have some extra conditionals in Diamond and Square to ensure that repeats
           never get appended to temp."""
        print "Size: ", len(list)
        i = 0
        while (i < len(list) - 1):
                if list[i] == list[i + 1]:
                    list.pop(i + 1)
                else:
                    i += 1
                



            