import tkinter as tk
import serial
import time
import sys, threading, queue
#from StartUp import *
#from ControlButtonFunctions import *

global ser
global ConnectionStateMessage
global arduinoQueue
global localQueue
global ConnectionState
global SerialReq

################################################################################################
## Define some functions
################################################################################################
def ReadInputs():
    #reads inputs from text entries and passes them as a tuple
    twistAngle = TwistAngle_entry.get()
    tubeLength = TubeLength_entry.get()
    tubeDiameter = TubeDiameter_entry.get()
    coldDrawRatio = coldDrawRatio_entry.get()
    FRAngle = FRAngle_entry.get()
    coilAngle = CoilAngle_entry.get()
    MandrelDiameter = MandrelDiameter_entry.get()
    return (twistAngle, tubeLength, tubeDiameter, coldDrawRatio, FRAngle, coilAngle,MandrelDiameter)

def packAndSendMsg(Command):
    #Packs together our message, taking the command character and the text entries and sends it over serial
    global ser
    Parameters = ReadInputs()
    msg = Command  # Add command indicator to msg

    for i in Parameters:
        msg = msg + ',' + i  # add the parameters to the message

    msg = msg + 'Z'  # add end of message indicator

    ser.write(bytes(str(msg), 'UTF-8'))

arduinoQueue = queue.Queue()
localQueue = queue.Queue()

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


ConnectionState = False #default we are not connected

def ConnectSerial(PortString):
    global ser
    global ConnectionStateMessage
    global ConnectionState

    ConnectionStateMessage.set("...")
    try:
        ser = serial.Serial(port= PortString, baudrate=9600, timeout=10)  # create Serial Object, baud = 9600, read times out after 10s
        time.sleep(.1)  # delay 3 seconds to allow serial com to get established

        ConnectionStateMessage.set("Connected")
        ConnectionState = True
    except:
        ConnectionStateMessage.set("Connection Failed")
        ConnectionState = False

def runStartUp():
    global ConnectionState
    global ConnectionStateMessage
    #global SerialReq

    # Build GUI to take Com Port------------------------------------------------------------------------------------------------------------
    tkTop = tk.Tk()  # Create GUI Box
    tkTop.geometry('600x200')  # size of GUI
    tkTop.title("PTCA-Machine Startup")  # title in top left of window

    #define some global Vars
    ConnectionStateMessage = tk.StringVar()
    ConnectionStateMessage.set("Not Connected")

    # Title on top middle of screen
    Title = tk.Label(text='Please Select a Com Port', font=("Courier", 14, 'bold')).pack()

    BodyFrame = tk.Frame(master=tkTop, width=400) # create frame for the entry controls
    BodyFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    ComPortInput_Label = tk.Label(master=BodyFrame, text='Com Port:', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=0, pady=0)
    ComPortInput_entry = tk.Entry(BodyFrame)
    ComPortInput_entry.insert(0, 'com4')
    ComPortInput_entry.pack(side='left', ipadx=0, padx=0, pady=0)
    ComPortExample_Label = tk.Label(master=BodyFrame, text='(Example: com3)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=0, pady=0)


    ButtonFrame=tk.Frame(master=tkTop, width=400) # create frame for the entry controls
    ButtonFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    ConnectButton = tk.Button(ButtonFrame,
                                       text="Connect",
                                       command=lambda: ConnectSerial(ComPortInput_entry.get()),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       )
    ConnectButton.pack(side='left', ipadx=10, padx=10, pady=40)

    ConnectionState_Label = tk.Label(master=ButtonFrame, textvariable=ConnectionStateMessage, font=("Courier", 10)).pack(side='left', ipadx=0, padx=0, pady=0)


    ExitStartup_Button = tk.Button(ButtonFrame,
                                       text="Done",
                                       command=tkTop.destroy,
                                       height=4,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       )
    ExitStartup_Button.pack(side='right', ipadx=10, padx=10, pady=40)

    SerialReq = tk.IntVar()
    checkbutton = tk.Checkbutton(master=ButtonFrame, text="Disable Serial Req", variable=SerialReq, onvalue=True, offvalue=False)
    checkbutton.pack(side='right', ipadx=10, padx=10, pady=40)

    tk.mainloop()
    return ConnectionState, SerialReq.get()

################################################################################################
## set up Serial Coms
################################################################################################
ComsState = False
SerialReq = 0

while not ComsState and SerialReq== 0:
    ComsState, SerialReq = runStartUp()


################################################################################################
## Robot Controls
################################################################################################
# Build GUI to take Com Port---------------------------------------------
tkTop = tk.Tk()  # Create GUI Box
tkTop.geometry('600x600')  # size of GUI
tkTop.title("PTCA-Machine Controller")  # title in top left of window

Title = tk.Label(text='PTCA Machine Controller', font=("Courier", 14, 'bold')).pack()

###############################
## Tube Properties
###############################
TubePropertiesFrame = tk.Frame(master=tkTop, width=400)
TubePropertiesFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

TubeFrame_Label = tk.Label(master=TubePropertiesFrame, text='Tube Properties', font=("Courier", 12, 'bold')).pack(side='top', ipadx=0, padx=0, pady=0)

TubeLengthFrame = tk.Frame(master=TubePropertiesFrame, width=400)
TubeLengthFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

TubeLength_Label = tk.Label(master=TubeLengthFrame, text='Tube Length (mm)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
TubeLength_entry = tk.Entry(TubeLengthFrame)
TubeLength_entry.insert(0,'100')
TubeLength_entry.pack(side='left', ipadx=0, padx=0, pady=0)

TubeDiameterFrame = tk.Frame(master=TubePropertiesFrame, width=400)
TubeDiameterFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
TubeDiameter_Label = tk.Label(master=TubeDiameterFrame, text='Tube Diameter (mm)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
TubeDiameter_entry = tk.Entry(TubeDiameterFrame)
TubeDiameter_entry.insert(0,'3.175')
TubeDiameter_entry.pack(side='left', ipadx=0, padx=0, pady=0)

MandrelDiameterFrame = tk.Frame(master=TubePropertiesFrame, width=400)
MandrelDiameterFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
MandrelDiameter_Label = tk.Label(master=MandrelDiameterFrame, text='Mandrel Diameter (mm)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
MandrelDiameter_entry = tk.Entry(MandrelDiameterFrame)
MandrelDiameter_entry.insert(0,'3.0')
MandrelDiameter_entry.pack(side='left', ipadx=0, padx=0, pady=0)
###############################
## Muscle Properties
###############################
MusclePropertiesFrame = tk.Frame(master=tkTop, width=400)
MusclePropertiesFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

MuscleFrame_Label = tk.Label(master=MusclePropertiesFrame, text='Muscle Properties', font=("Courier", 12, 'bold')).pack(side='top', ipadx=0, padx=0, pady=0)

TwistAngleFrame = tk.Frame(master=MusclePropertiesFrame, width=400)
TwistAngleFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
TwistAngle_Label = tk.Label(master=TwistAngleFrame, text='Twist Angle (Deg)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
TwistAngle_entry = tk.Entry(TwistAngleFrame)
TwistAngle_entry.insert(0,'35')
TwistAngle_entry.pack(side='left', ipadx=0, padx=0, pady=0)

FRAngleFrame = tk.Frame(master=MusclePropertiesFrame, width=400)
FRAngleFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
FRAngle_Label = tk.Label(master=FRAngleFrame, text='FR Pitch (mm)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
FRAngle_entry = tk.Entry(FRAngleFrame)
FRAngle_entry.insert(0,'7')
FRAngle_entry.pack(side='left', ipadx=0, padx=0, pady=0)

coldDrawRatioFrame = tk.Frame(master=MusclePropertiesFrame, width=400)
coldDrawRatioFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
coldDrawRatio_Label = tk.Label(master=coldDrawRatioFrame, text='Cold Draw Ratio', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
coldDrawRatio_entry = tk.Entry(coldDrawRatioFrame)
coldDrawRatio_entry.insert(0,'3')
coldDrawRatio_entry.pack(side='left', ipadx=0, padx=0, pady=0)

CoilAngleFrame = tk.Frame(master=MusclePropertiesFrame, width=400)
CoilAngleFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
CoilAngle_Label = tk.Label(master=CoilAngleFrame, text='Coil Pitch (mm)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
CoilAngle_entry = tk.Entry(CoilAngleFrame)
CoilAngle_entry.insert(0,'8')
CoilAngle_entry.pack(side='left', ipadx=0, padx=0, pady=0)

###############################
## Controls
###############################
ControlsFrame = tk.Frame(master=tkTop, width=400)
ControlsFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

ControlsFrame_Label = tk.Label(master=ControlsFrame, text='Controls', font=("Courier", 12, 'bold')).pack(side='top', ipadx=0, padx=0, pady=0)

TopRowControlsFrame=tk.Frame(master=ControlsFrame, width=400)
TopRowControlsFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

HomeButton = tk.Button(TopRowControlsFrame,
                                       text="Home",
                                       command= lambda: packAndSendMsg('A'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=10)

ColdDrawButton = tk.Button(TopRowControlsFrame,
                                       text="Cold Draw",
                                       command= lambda: packAndSendMsg('B'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=10)

FrButton = tk.Button(TopRowControlsFrame,
                                       text="Fiber Reinforce",
                                       command= lambda: packAndSendMsg('C'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=10)

TwistButton = tk.Button(TopRowControlsFrame,
                                       text="Twist",
                                       command= lambda: packAndSendMsg('D'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=10)

CoilButton = tk.Button(TopRowControlsFrame,
                                       text="Coil",
                                       command= lambda: packAndSendMsg('E'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=10)

MiddleRowControlsFrame=tk.Frame(master=ControlsFrame, width=400)
MiddleRowControlsFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
JogFollowerUpButton = tk.Button(MiddleRowControlsFrame,
                                       text="Follower Up",
                                       command= lambda: packAndSendMsg('G'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=10)

#JogFollowerUpButton.bind()

JogFollowerDownButton = tk.Button(MiddleRowControlsFrame,
                                       text="Follower Down",
                                       command= lambda: packAndSendMsg('H'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=10)

JogRunnerUpButton = tk.Button(MiddleRowControlsFrame,
                                       text="Runner Up",
                                       command= lambda: packAndSendMsg('I'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=10)

JogRunnerDownButton = tk.Button(MiddleRowControlsFrame,
                                       text="Runner Down",
                                       command= lambda: packAndSendMsg('J'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=10)

BottomRowControlsFrame=tk.Frame(master=ControlsFrame, width=400)
BottomRowControlsFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
StopButton = tk.Button(BottomRowControlsFrame,
                                       text="Stop",
                                       command= lambda: packAndSendMsg('F'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='red'
                                       ).pack(side='top', ipadx=10, padx=10, pady=10)

tk.mainloop()