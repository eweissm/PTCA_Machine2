import tkinter as tk
import serial
import time
from StartUp import *

global ser
global ConnectionStateMessage

################################################################################################
## set up Serial Coms
################################################################################################
ComsState = False

while not ComsState:
    ComsState = runStartUp()

################################################################################################
## Robot Controls
################################################################################################
# Build GUI to take Com Port---------------------------------------------
tkTop = tk.Tk()  # Create GUI Box
tkTop.geometry('1200x800')  # size of GUI
tkTop.title("PTCA-Machine Controller")  # title in top left of window

Title = tk.Label(text='PTCA Machine Controller', font=("Courier", 14, 'bold')).pack()

###############################
## Tube Properties
###############################
TubePropertiesFrame = tk.Frame(master=tkTop, width=400)
TubePropertiesFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

TubeFrame_Label = tk.Label(master=TubePropertiesFrame, text='Tube Properties', font=("Courier", 12, 'bold')).pack(side='top', ipadx=0, padx=0, pady=0)

TubeLength_Label = tk.Label(master=TubePropertiesFrame, text='Tube Length (mm)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=0, pady=0)
TubeLength_entry = tk.Entry(TubePropertiesFrame).pack(side='left', ipadx=0, padx=0, pady=0)

TubeRadius_Label = tk.Label(master=TubePropertiesFrame, text='Tube Radius (mm)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
TubeRadius_entry = tk.Entry(TubePropertiesFrame).pack(side='left', ipadx=0, padx=0, pady=0)
###############################
## Muscle Properties
###############################
MusclePropertiesFrame = tk.Frame(master=tkTop, width=400)
MusclePropertiesFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

MuscleFrame_Label = tk.Label(master=MusclePropertiesFrame, text='Muscle Properties', font=("Courier", 12, 'bold')).pack(side='top', ipadx=0, padx=0, pady=0)

TwistAngle_Label = tk.Label(master=MusclePropertiesFrame, text='Twist Angle (Deg)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=0, pady=0)
TwistAngle_entry = tk.Entry(MusclePropertiesFrame).pack(side='left', ipadx=0, padx=0, pady=0)

FRAngle_Label = tk.Label(master=MusclePropertiesFrame, text='FR Angle (Deg)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=0, pady=0)
FRAngle_entry = tk.Entry(MusclePropertiesFrame).pack(side='left', ipadx=0, padx=0, pady=0)

coldDrawRatio_Label = tk.Label(master=MusclePropertiesFrame, text='Cold Draw Ratio', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=0, pady=0)
coldDrawRatio_entry = tk.Entry(MusclePropertiesFrame).pack(side='left', ipadx=0, padx=0, pady=0)

CoilAngle_Label = tk.Label(master=MusclePropertiesFrame, text='Coil Angle (Deg)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=0, pady=0)
CoilAngle_entry = tk.Entry(MusclePropertiesFrame).pack(side='left', ipadx=0, padx=0, pady=0)

###############################
## Controls
###############################
ControlsFrame = tk.Frame(master=tkTop, width=400)
ControlsFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

tk.mainloop()