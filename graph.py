import pygame
from math import sin, cos, sqrt, pow, asin, radians

class graph1 :
    def __init__(self, screen, dist, scale) :
        self.values = []
        self.screener = screen
        w, h = screen.get_size()
        self.landmark1 = [(w/2)-scale*(dist/2),100]
        self.landmark2 = [(w/2)+scale*(dist/2),100]
        self.pose_estimate = []
        self.pose_sensor = []
        self.move_estimate = []
        self.dist_arr = [0, 0]
        self.scale = scale
        self.draw()

    def add_new_pose(self, a, b, thetal, thetar) :
        self.values.append([a,b,thetal, thetar])
        self.__calculate__()
        

    def draw (self):
        pygame.draw.circle(self.screener, (0, 255, 0), (self.landmark1[0], self.landmark1[1]), 10)
        pygame.draw.circle(self.screener, (0, 255, 0), (self.landmark2[0], self.landmark2[1]), 10)
        for i in self.pose_sensor:
            pygame.draw.circle(self.screener, (255, 0, 0), i, 5)
        
        
    def __calculate__(self):
        if (len(self.values) != 0) :
            a, b, thetal, thetar = self.values[len(self.values)-1]
            dist = (a*a)+(b*b)-2*a*b*cos(radians(thetal+thetar))
            dist = sqrt(dist)
            self.dist_arr[0] = ((self.dist_arr[0]*self.dist_arr[1])+dist)/(self.dist_arr[1]+1)
            self.dist_arr[1] = self.dist_arr[1] + 1
            rd = self.dist_arr[0]
            w, h = self.screener.get_size()
            self.landmark1 = [(w/2)-(self.scale)*(rd/2),self.landmark1[1]]
            self.landmark2 = [(w/2)+(self.scale)*(rd/2),self.landmark2[1]]
            print("Distance : " + str(rd))
            print("Value : " + str(b*sin(radians(thetal+thetar))/rd))
            x = self.landmark2[0] - (self.scale)*a*cos(asin(b*sin(radians(thetal+thetar))/rd))
            y = self.landmark2[1] + (self.scale)*a*(b*sin(radians(thetal+thetar))/rd)
            if (len(self.pose_sensor) !=0):
                x1 = self.pose_sensor[len(self.pose_sensor) - 1][0]
                y1 = self.pose_sensor[len(self.pose_sensor) - 1][1]
                something = (x1-x)*(x1-x) + (y1-y)*(y1-y)
                nothing = sqrt(something)
                print("Odometry data: " + str(nothing))
            self.pose_sensor.append([x, y])
            self.draw()


