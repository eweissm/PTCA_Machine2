import tkinter as tk
import serial
import time
from StartUp import *

global ser
global ConnectionStateMessage

################################################
## set up Serial Coms
################################################
ComsState = False

while not ComsState:
    ComsState = runStartUp()


print(ComsState)