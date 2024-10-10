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
################################################################################################
## Define some functions
################################################################################################
def ReadInputs():
    twistAngle = TwistAngle_entry.get()
    tubeLength = TubeLength_entry.get()
    tubeRadius = TubeRadius_entry.get()
    coldDrawRatio = coldDrawRatio_entry.get()
    FRAngle = FRAngle_entry.get()
    coilAngle = CoilAngle_entry.get()

    return (twistAngle, tubeLength, tubeRadius, coldDrawRatio, FRAngle, coilAngle)

def packAndSendMsg(Command):
    global ser
    Parameters = ReadInputs()
    msg = Command  # Add command indicator to msg

    for i in Parameters:
        msg = msg + ',' + i  # add the parameters to the message

    msg = msg + 'Z'  # add end of message indicator

    print(msg)
    ser.write(bytes(str(msg), 'UTF-8'))

# def Home():
#     global ser
#     Parameters = ReadInputs()
#     msg = 'A' #Add command indicator to msg
#
#     for i in Parameters:
#         msg = msg+','+i #add the parameters to the message
#
#     msg = msg + 'Z' # add end of message indicator
#
#     print(msg)
#     ser.write(bytes( str(msg), 'UTF-8'))
#
# def ColdDraw(TubeInitialLength, ColdDrawRatio):
#     global ser
#     Parameters = ReadInputs()
#     msg = 'B'  # Add command indicator to msg
#
#     for i in Parameters:
#         msg = msg + ',' + i  # add the parameters to the message
#
#     msg = msg + 'Z'  # add end of message indicator
#
#     print(msg)
#     ser.write(bytes(str(msg), 'UTF-8'))
#
# def FiberReinforce(FR_Angle, TubeRadius):
#     print("test")
#
# def Twist(TwistAngle, TubeInitialLength, ColdDrawRatio):
#     print("test")
#
# def Coil(CoilAngle):
#     print("test")
#
# def Stop():
#     print("test")

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
        time.sleep(3)  # delay 3 seconds to allow serial com to get established

        ConnectionStateMessage.set("Connected")
        ConnectionState = True
    except:
        ConnectionStateMessage.set("Connection Failed")
        ConnectionState = False

def runStartUp():
    global ConnectionState
    global ConnectionStateMessage

    # Build GUI to take Com Port------------------------------------------------------------------------------------------------------------
    tkTop = tk.Tk()  # Create GUI Box
    tkTop.geometry('400x200')  # size of GUI
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

    tk.mainloop()
    return ConnectionState

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
TubeLength_entry.pack(side='left', ipadx=0, padx=0, pady=0)

TubeRadiusFrame = tk.Frame(master=TubePropertiesFrame, width=400)
TubeRadiusFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
TubeRadius_Label = tk.Label(master=TubeRadiusFrame, text='Tube Radius (mm)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
TubeRadius_entry = tk.Entry(TubeRadiusFrame)
TubeRadius_entry.pack(side='left', ipadx=0, padx=0, pady=0)

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
TwistAngle_entry.pack(side='left', ipadx=0, padx=0, pady=0)

FRAngleFrame = tk.Frame(master=MusclePropertiesFrame, width=400)
FRAngleFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
FRAngle_Label = tk.Label(master=FRAngleFrame, text='FR Angle (Deg)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
FRAngle_entry = tk.Entry(FRAngleFrame)
FRAngle_entry.pack(side='left', ipadx=0, padx=0, pady=0)

coldDrawRatioFrame = tk.Frame(master=MusclePropertiesFrame, width=400)
coldDrawRatioFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
coldDrawRatio_Label = tk.Label(master=coldDrawRatioFrame, text='Cold Draw Ratio', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
coldDrawRatio_entry = tk.Entry(coldDrawRatioFrame)
coldDrawRatio_entry.pack(side='left', ipadx=0, padx=0, pady=0)

CoilAngleFrame = tk.Frame(master=MusclePropertiesFrame, width=400)
CoilAngleFrame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
CoilAngle_Label = tk.Label(master=CoilAngleFrame, text='Coil Angle (Deg)', font=("Courier", 12, 'bold')).pack(side='left', ipadx=0, padx=10, pady=0)
CoilAngle_entry = tk.Entry(CoilAngleFrame)
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
                                       ).pack(side='left', ipadx=10, padx=10, pady=40)

ColdDrawButton = tk.Button(TopRowControlsFrame,
                                       text="Cold Draw",
                                       command= lambda: packAndSendMsg('B'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=40)

FrButton = tk.Button(TopRowControlsFrame,
                                       text="Fiber Reinforce",
                                       command= lambda: packAndSendMsg('C'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=40)

TwistButton = tk.Button(TopRowControlsFrame,
                                       text="Twist",
                                       command= lambda: packAndSendMsg('D'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=40)

CoilButton = tk.Button(TopRowControlsFrame,
                                       text="Coil",
                                       command= lambda: packAndSendMsg('E'),
                                       height=3,
                                       fg="black",
                                       width=10,
                                       bd=5,
                                       activebackground='green'
                                       ).pack(side='left', ipadx=10, padx=10, pady=40)

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
                                       ).pack(side='bottom', ipadx=10, padx=10, pady=40)

tk.mainloop()