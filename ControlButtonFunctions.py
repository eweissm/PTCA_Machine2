import tkinter as tk
import serial
import time
import sys, threading, queue

global ser
global arduinoQueue
global localQueue

arduinoQueue = queue.Queue()
localQueue = queue.Queue()
def Home():
    print("test")

def ColdDraw(TubeInitialLength, ColdDrawRatio):
    print("test")

def FiberReinforce(FR_Angle, TubeRadius):
    print("test")

def Twist(TwistAngle, TubeInitialLength, ColdDrawRatio):
    print("test")

def Coil(CoilAngle):
    print("test")

def Stop():
    print("test")

def listenToArduino():
    message = b''
    while True:
        incoming = ser.read()
        if (incoming == b'\n'):
            arduinoQueue.put(message.decode('utf-8').strip().upper())
            message = b''
        else:
            if ((incoming != b'') and (incoming != b'\r')):
                 message += incoming