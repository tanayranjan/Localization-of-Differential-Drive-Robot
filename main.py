import pygame
from pygame.constants import K_RETURN
import numpy as np
import time
import serial
from graph import graph1


scale = 100 # (Screen Width in pixels)/(Width in meters)
ratio = 3 # Height to Width
width = 300
phase_mode = 0

a = 0
b = 0
thetal = 0
thetar = 0

receive_flag = 0

pygame.init()
screen = pygame.display.set_mode((width,width*ratio))
pygame.display.set_caption("Map")
arduino = serial.Serial(
    port='COM10',
    baudrate = 9600,
    timeout = 1)
print("Connected")
graph_rep = graph1(screen=screen, dist=0, scale=scale)


def main() :
    run = True
    while(run):
        
        if (arduino.inWaiting() != 0):
            global receive_flag
            receive_flag = 1
            arduino_data = arduino.readline()
            decoded_value = str(arduino_data[0:len(arduino_data)].decode('utf-8'))
            value = decoded_value.split(',')
            value_float = []
            for i in value:
                value_float.append(float(i))
            global a, b, thetal, thetar
            a = value_float[0]
            b = value_float[1]
            thetal = value_float[2]
            thetar = -value_float[3]
            print ("Received Data : ")
            print (value_float)
            screen.fill((0,0,0))
            graph_rep.add_new_pose(a, b, thetal, thetar)

        
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        pygame.display.update()

if __name__ == '__main__' :   
    try:
        main()
    except KeyboardInterrupt:
        pass
    except serial.SerialException:
        pass
