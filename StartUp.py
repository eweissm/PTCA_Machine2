import tkinter as tk


def ConnectSerial(PortString):
    ConnectionStateMessage.set("Connected")


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
