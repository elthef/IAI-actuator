import tkinter
import tkinter as tk
from tkinter import messagebox
import customtkinter
import time
import timeit
from serial import Serial
import threading
from serial.threaded import ReaderThread, Protocol, LineReader
from datetime import datetime

HOME =":0105040BFF00EC\r\n"
SERVO_ON = ":01050403FF00F4\r\n"
MOVE_LOC0 = ":01069800000061\r\n"
MOVE_LOC1 = ":01069800000160\r\n"
MOVE_LOC2 = ":0106980000025F\r\n"
MOVE_LOC3 = ":0106980000035E\r\n"
MOVE_LOC4 = ":0106980000045D\r\n"
MOVE_LOC5 = ":0106980000055C\r\n"
CurrentPos =":0103900000026A\r\n"
FiftymmPos =":0110990000020400001388B5\r\n"

# Addresses
SLAVE_ADDRESS = '01' # refer pg215
# Function Codes
READ_COIL_STATUS = '01' #30H31H. READ COIL STATUS READ COILS/DOS.
READ_INPUT_STATUS ='02' #30H32H. READ INPUT STATUS READ INPUT STATUSES/DIS.
READ_HOLDING_REGISTERS = '03' # 30H33H. READ HOLDING REGISTERS READ HOLDING REGISTERS.
READ_INPUT_REGISTERS = '04' # 30H34H. READ INPUT REGISTERS READ INPUT REGISTERS.
FORCE_SINGLE_COIL= '05' # 30H35H. FORCE SINGLE COIL WRITE ONE COIL/DO.
PRESET_SINGLE_REGISTER= '06' # 30H36H. PRESET SINGLE REGISTER WRITE HOLDING REGISTER.
READ_EXCEPTION= '07' #30H37H. READ EXCEPTION STATUS READ EXCEPTION STATUSES.
FORCE_MULTIPLE_COILS= '0F' #30H46H. FORCE MULTIPLE COILS WRITE MULTIPLE COILS/DOS AT ONCE.
PRESET_MULTIPLE_REGISTERS = '10' # 31H30H.  WRITE MULTIPLE HOLDING REGISTERS AT ONCE.
REPORT_SLAVE_ID = '11' #31H31H. REPORT SLAVE ID QUERY A SLAVE’S ID.
READ_WRITE_REGISTERS= '17' # 31H37H. READ / WRITE REGISTERS READ/WRITE REGISTERS

# Function Code (05) PG291
SON_H = '04'  # Servo ON  High byte command PG286
SON_L = '03' # Servo ON  Low byte command PG286
HOME_H = '04' #Home H return command
HOME_L = '0B' #Home L return command
Alarm_reset_H = '04' # Alarm reset H
Alarm_reset_L = '07' # Alarm reset L

# Data for Function Code 05
SERVO_ON = 'FF'
SERVO_OFF = '00'


#Function Code (06) Start address list
PMCR = '9800' # Position movement command register

#Positioning Data Direct Writing
PCMD ='9900' #Target position specification register
# tgt_pos_band = '000A'  # Position band 0.01 mm pg 377
# tgt_pos_vel  = '2710'  # Velocity 0.01 mm/s
# tgt_pos_acc  = '001E'  # Acceleration 0.01 G
# PNOW
CPM = '9000'

#Special characters
CR = '\r' #0x0D # carriage return '\r'
LF = '\n' #0x0A # line feed '\n'

# constant parameters
speed_combValues = ['2.5 mm/s', '4 mm/s', '5.2 mm/s','10 mm/s','100 mm/s']
max_distance = 200
tgt_pos_band = '000A'  # Position band 0.01 mm pg 377
tgt_pos_vel  = '2710'  # Velocity 0.01 mm/s
tgt_pos_acc  = '001E'  # Acceleration 0.01 G

def connect(portname,baudrate):
    #connect to serial port
    global serial_port
    try:
        serial_port = Serial(portname, baudrate=baudrate, timeout=0.5)
    except:
        pass #tkinter.messagebox.showerror(title="Error", message="Cannot Open Serial Port Check connection")
    return (serial_port)

def close():
    # Close serial port
    try:
        serial_port.close()
    except:
        pass#tkinter.messagebox.showerror(title="Error", message="Cannot Close Serial Port Check connection")

class InfiniteTimer():
    """A Timer class that does not stop, unless you want it to."""

    def __init__(self, seconds, target):
        self._should_continue = False
        self.is_running = False
        self.seconds = seconds
        self.target = target
        self.thread = None

    def _handle_target(self):
        self.is_running = True
        self.target()
        self.is_running = False
        self._start_timer()

    def _start_timer(self):
        if self._should_continue:  # Code could have been running when cancel was called.
            self.thread = threading.Timer(self.seconds, self._handle_target)
            self.thread.start()

    def start(self):
        if not self._should_continue and not self.is_running:
            self._should_continue = True
            self._start_timer()
        else:
            print("Timer already started or running, please wait if you're restarting.")

    def cancel(self):
        if self.thread is not None:
            self._should_continue = False  # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")

    def stop(self):
        if self.thread is not None:
            self._should_continue = False  # Just in case thread is running and cancel fails.
            self.thread.cancel()


class SerialReaderProtocolRaw(Protocol):
    tk_listener = None

    def connection_made(self, transport):
        """Called when reader thread is started"""
        if self.tk_listener is None:
            raise Exception("tk_listener must be set before connecting to the socket!")
        print("Connected raw, ready to receive data...")

    def data_received(self, data):
        """Called with snippets received from the serial port"""
        try:
            self.tk_listener.after(0, self.tk_listener.on_data, data.decode())
        except:
             pass
            #print("data received ",data)

# class SerialReaderProtocolLine(LineReader):
#     tk_listener = None
#     TERMINATOR = b'\n\r'
#
#     def connection_made(self, transport):
#         """Called when reader thread is started"""
#         if self.tk_listener is None:
#             raise Exception("tk_listener must be set before connecting to the socket!")
#         super().connection_made(transport)
#         print("Connected, ready to receive data...")
#
#     def handle_line(self, line):
#         """New line waiting to be processed"""
#         # Execute our callback in tk
#         self.tk_listener.after(0, self.tk_listener.on_data, line)


'''
def checksum(data)
Generate Check Sum
    Connect to serial port to which Herkulex Servos are attatched
    Args:
        portname (str): The serial port name
        baudrate (int): The serial port baudrate
    Raises:
        SerialException: Error occured while opening serial port
'''
def checksum(data):
    total = 0
    #join every two strings digits  '1' '2' '3' '4 -> '12' '34'

    temp_data = [''.join(data[i:i+2]) for i in range(0, len(data), 2)]
    #print('print_tem-data',temp_data)
    #print('checksum',int(temp_data[4],16))

    w = [total := total + int(i, 16) for i in temp_data]
    value = -w[-1] & 0xFF # mask off the FF
    #print('checksum1',data, total, w, hex(value), [w[-1]])
    return value


def send_data(data):
    global serial_port
    """ Send data to herkulex
    Paketize & write the packet to serial port
    Args:
        data (list): the data to be sent
    Raises:
        SerialException: Error occured while opening serial port
        ff
        ff
        data.append(0x0C)
        data.append(servoid)
        data.append(I_JOG_REQ)
        data.append(goalposition_lsb)
        data.append(goalposition_msb)
        csm1
        csm2
        data.append(led)
        data.append(servoid)   0xdb
        data.append(goaltime)
        send_data(data)
    """
    data.insert(0,':') # ASCII :
    data.append(CR) # start address
    data.append(LF) # start address
    #print(data)
    string2send = ""
    for i in range(len(data)):
        #pass
#        print(data[i])
#       byteformat = '%02X'% data[i]
#       string2send = string2send +"\\x" + byteformat
       string2send = string2send + data[i].upper()
#        string2send =":0106980000055C\r\n"
    #print('send_data',string2send)
    try:
        #print(string2send.decode('string-escape'))
        for i in data:
            serial_port.write(bytearray(string2send,'ascii'))
#

    except:
        #pass
        print("send error")
        #raise HerkulexError("could not communicate with motors")
        #messagebox.showerror("Error","data cannot be send")

def servo_On():
    """ servo_On command
        Args:

    """
    data = []
    data.append(SLAVE_ADDRESS[0])
    data.append(SLAVE_ADDRESS[1])
    data.append(FORCE_SINGLE_COIL[0])
    data.append(FORCE_SINGLE_COIL[1])
    data.append(SON_H[0])
    data.append(SON_H[1])
    data.append(SON_L[0])
    data.append(SON_L[1])
    data.append(SERVO_ON[0])
    data.append(SERVO_ON[1])
    data.append('0')
    data.append('0')

    #print(f' before {data}')
    result = checksum(data)
    temp = f'{result:x}'  # remove the x
    #print(temp,temp[0])
    data.append(temp[0])
    data.append(temp[1])
    #print(data)
    send_data(data)

def move_loc(value):
    """ servo_On command
        Args:
            value : the change value in string
    """
    data = []
    data.append(SLAVE_ADDRESS[0])
    data.append(SLAVE_ADDRESS[1])
    data.append(PRESET_SINGLE_REGISTER[0])
    data.append(PRESET_SINGLE_REGISTER[1])
    data.append(PMCR[0])
    data.append(PMCR[1])
    data.append(PMCR[2])
    data.append(PMCR[3])
    data.append(value[0])
    data.append(value[1])
    data.append(value[2])
    data.append(value[3])
    #print(f' before {data}')
    result = checksum(data)
    temp = f'{result:x}'  # remove the x
    #print(temp,temp[0])
    data.append(temp[0])
    data.append(temp[1])
    #print(data)
    send_data(data)

def move2Pos(tgt_pos):
    """ servo_On command
           Args:
               value : the change value in string

               Slave address [H]   2
               Function code [H]   2
               Start address [H]   4
               Number of registers [H]  4
               Number of bytes [H]      2
               Changed data 1 [H]       4
               Changed data 2 [H]       4
               Changed data 3 [H]       4

       """
    data = []
    data.append(SLAVE_ADDRESS[0])
    data.append(SLAVE_ADDRESS[1])
    data.append(PRESET_MULTIPLE_REGISTERS[0])
    data.append(PRESET_MULTIPLE_REGISTERS[1])
    data.append(PCMD[0])
    data.append(PCMD[1])
    data.append(PCMD[2])
    data.append(PCMD[3])
    data.append('0')
    data.append('0')
    data.append('0')
    data.append('2')
    data.append('0')
    data.append('4')
    data.append('0')
    data.append('0')
    data.append('0')
    data.append('0')
    data.append(tgt_pos[0])
    data.append(tgt_pos[1])
    data.append(tgt_pos[2])
    data.append(tgt_pos[3])
    # print(f' before {data}')
    result = checksum(data)
    temp = f'{result:x}'  # remove the x
    # print(temp,temp[0])
    data.append(temp[0])
    data.append(temp[1])
    print(data)
    send_data(data)

def move2PoswifSpeed(tgt_pos,tgt_pos_band,tgt_pos_vel,tgt_pos_acc):
    """ move2PoswifSpeed command
           Args:
               move2PoswifSpeed(tgt_pos,tgt_pos_band,tgt_pos_vel,tgt_pos_acc) : the change value in string

               Slave address [H]   2
               Function code [H]   2
               Start address [H]   4
               Number of registers [H]  4
               Number of bytes [H]      2
               Changed data 1 [H]       4
               Changed data 2 [H]       4
               Changed data 3 [H]       4

       """
    data = []
    data.append(SLAVE_ADDRESS[0])
    data.append(SLAVE_ADDRESS[1])
    data.append(PRESET_MULTIPLE_REGISTERS[0])
    data.append(PRESET_MULTIPLE_REGISTERS[1])
    data.append(PCMD[0])
    data.append(PCMD[1])
    data.append(PCMD[2])
    data.append(PCMD[3])
    data.append('0')
    data.append('0')
    data.append('0')
    data.append('7')
    data.append('0')
    data.append('E')
    data.append('0')
    data.append('0')
    data.append('0')
    data.append('0')
    data.append(tgt_pos[0])
    data.append(tgt_pos[1])
    data.append(tgt_pos[2])
    data.append(tgt_pos[3])
    data.append('0')
    data.append('0')
    data.append('0')
    data.append('0')
    data.append(tgt_pos_band[0])
    data.append(tgt_pos_band[1])
    data.append(tgt_pos_band[2])
    data.append(tgt_pos_band[3])
    data.append('0')
    data.append('0')
    data.append('0')
    data.append('0')
    data.append(tgt_pos_vel[0])
    data.append(tgt_pos_vel[1])
    data.append(tgt_pos_vel[2])
    data.append(tgt_pos_vel[3])
    data.append(tgt_pos_acc[0])
    data.append(tgt_pos_acc[1])
    data.append(tgt_pos_acc[2])
    data.append(tgt_pos_acc[3])
    #print(f' before {data} length {len(data)}')
    result = checksum(data)
    temp = f'{result:x}'  # remove the x
    #print(temp,temp[0],len(temp))
    # data.append(temp[0])
    # data.append(temp[1])
    if (len(temp)>=2):
        data.append(temp[0])
        data.append(temp[1])
    else:
        data.append('0')
        data.append(temp[0])
    #print(data)
    send_data(data)

def ALRS():
    """ ALRS command
               Args:
                   void  : the change value in string

                   Slave address [H]   2
                   Function code [H]   2
                   Start address [H]   4
                   Number of registers [H]  4
                   Number of bytes [H]      2
                   Changed data 1 [H]       4
                   Changed data 2 [H]       4
                   Changed data 3 [H]       4

           """
    data = []
    data.append(SLAVE_ADDRESS[0])
    data.append(SLAVE_ADDRESS[1])
    data.append(FORCE_SINGLE_COIL[0]) # 0
    data.append(FORCE_SINGLE_COIL[1]) # 5
    data.append(Alarm_reset_H[0])     # 0
    data.append(Alarm_reset_L[1])     # 4
    data.append(SON_L[0])             # 0
    data.append(SON_L[1])             # 7
    data.append('F')
    data.append('F')
    data.append('0')
    data.append('0')

    # print(f' before {data}')
    result = checksum(data)
    temp = f'{result:x}'  # remove the x
    # print(temp,temp[0])
    data.append(temp[0])
    data.append(temp[1])
    # print(data)
    send_data(data)

def PNOW():
    # data = CurrentPos
    # for i in data:
    #     serial_port.write(bytearray(i, 'ascii'))

    """ PNOW command
    Read Current Postion Now
    CurrentPos =":01 03 9000 0002 6A\r\n"
                   Args:
                       void  : the change value in string

                       Slave address [H]   2
                       Function code [H]   2
                       Start address [H]   4
                       Number of registers [H]  4
                       Number of bytes [H]      2
                       Changed data 1 [H]       4
                       Changed data 2 [H]       4
                       Changed data 3 [H]       4

               """
    data = []
    data.append(SLAVE_ADDRESS[0])
    data.append(SLAVE_ADDRESS[1])
    data.append(READ_HOLDING_REGISTERS[0])  # 0
    data.append(READ_HOLDING_REGISTERS[1])  # 3
    data.append(CPM[0])  # 9
    data.append(CPM[1])  # 0
    data.append(CPM[2])  # 0
    data.append(CPM[3])  # 0
    data.append('0')  # 0
    data.append('0')  # 7
    data.append('0')
    data.append('2')

    #print(f' before {data}')
    result = checksum(data)
    temp = f'{result:x}'  # remove the x
    # print(temp,temp[0])
    if (len(temp) >= 2):
        data.append(temp[0])
        data.append(temp[1])
    else:
        data.append('0')
        data.append(temp[0])
    #print(data)
    send_data(data)
def startCallBack():
    # Initiate serial port
    # messagebox.showinfo( "Hello Python", "Hello World")
    # data = SERVO_ON
    # for i in data:
    #     serial_port.write(bytearray(i, 'ascii'))
    servo_On()

def MovePos():
    global t
    num = 1
    test = f"{num:04}"
    move_loc(test.upper())
    t = InfiniteTimer(0.001, readPostCallBack)
    t.start()

def MoveCallBack(pos):
    global MF_tgt_pos
    global t1

    MF_tgt_pos = (pos)
    print("position",pos)
    if MF_tgt_pos > 0 and MF_tgt_pos <= max_distance:
        dist = MF_tgt_pos * 100
        tgt_pos = str(f'{int(dist):0>4x}')
        move2Pos(tgt_pos)
        #move2PoswifSpeed(tgt_pos,tgt_pos_band,tgt_pos_vel, tgt_pos_acc)
        time.sleep(0.1)
        #t1 = threading.Thread(target=IAI.move2PoswifSpeed,args=(tgt_pos,tgt_pos_band, tgt_pos_vel, tgt_pos_acc,))
        # Start the threads
        #t1.start()
        print("Inside loop",tgt_pos)
        #readPostCallBack()
        t1 = InfiniteTimer(0.02, readPostCallBack)
        t1.start()
    else:
        messagebox.showerror("Error",f'The Position value entered {MF_tgt_pos} mm \n must be between 0 and 200' )

def ResetCallBack():
    ALRS()

def readPostCallBack():
    global  serial_port
    #pass
    #print("1")
    #PNOW()
    data = CurrentPos
    for i in data:
        serial_port.write(bytearray(i, 'ascii'))

class MainFrame(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.frame = customtkinter.CTkFrame(master=app, width=600, height=300, corner_radius=15)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        # combo box
        # Label
        self.speedlabel = customtkinter.CTkLabel(master=self.frame, text="Speed (mm/s)", justify=tk.LEFT)
        self.speedlabel.place(x=80.5, y=20.5, anchor=tk.CENTER)
        self.speedlabel.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="e")

        self.combobox_speedvar = customtkinter.StringVar(value='5 mm/s')  # set initial value
        self.combobox_speed = customtkinter.CTkComboBox(master=self.frame, values=speed_combValues,
                                                        command=self.combobox_speed_selection)
        self.combobox_speed.grid(row=2, column=1, columnspan=1, pady=5, padx=5, sticky="e")

        self.label = customtkinter.CTkLabel(master=self.frame, text="Position (mm)", justify=tk.LEFT)
        self.label.place(x=20.5, y=20.5, anchor=tk.CENTER)
        self.label.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky="e")

        int_var = tk.IntVar()
        self.slider_dist = customtkinter.CTkSlider(master=self.frame, from_=0, to=200, height = 10, width=100,
                                                   orient="horizontal",command = self.slider_event)
        self.slider_dist.place(x=20.5, y=20.5, anchor=tk.CENTER)
        self.slider_dist.grid(row=3, column=1, columnspan=1, pady=25, padx=25, sticky="n")

        self.slider_value = self.slider_dist.get()
        self.slider_dist_label = customtkinter.CTkLabel(master=self.frame, text=str(self.slider_value), justify=tk.LEFT)
        self.slider_dist_label.place(x=230, y=60.5, anchor=tk.CENTER)

        self.button = customtkinter.CTkButton(master=self.frame, text="Start", command=startCallBack)
        self.button.place(x=20.5, y=0.5, anchor=tk.CENTER)
        self.button.grid(row=5, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")

        self.buttonMove = customtkinter.CTkButton(master=self.frame, text="Move",
                                                  command=lambda: MoveCallBack(self.slider_dist.get()))
        self.buttonMove.grid(row=6, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        self.buttonReset = customtkinter.CTkButton(master=self.frame, text="Reset",
                                                  command=lambda: ResetCallBack())
        self.buttonReset.grid(row=7, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        self.connectionStatuslabel = customtkinter.CTkLabel(master=self.frame, text="Not Connected", justify=tk.LEFT)
        self.connectionStatuslabel.place(x=80.5, y=20.5, anchor=tk.CENTER)
        self.connectionStatuslabel.grid(row=8, column=0, columnspan=1, padx=10, pady=10, sticky="e")

    def on_data(self, data):
        global t1
        print("Called from on_data ", data)
        lock = threading.Lock()
        lock.acquire()
        #t1.stop()
        try:
            if data[3] == '3':
                pos_data = data[6:14]
                strings = [str(pos) for pos in pos_data]
                a_string = "".join(strings)
                an_integer = int(a_string, 16) * 0.01
                ts = datetime.timestamp(dt) * 1000
                print(f"tgt position {MF_tgt_pos:.2f} position: {an_integer:.2f} mm {ts} ms")
                if an_integer >= MF_tgt_pos:
                    print("stop")
                    t1.cancel()
        except:
            pass
            #print("error",len(data))

        lock.release()

    def combobox_speed_selection(self, event):
        global tgt_pos_vel
        # Three methods here all get the same value.
        #print("change")
        #print(event)
        #speed_combValues = ['2.5 mm/s', '4 mm/s', '5.2 mm/s', '10 mm/s']
        match event:
            case '2.5 mm/s':
                print('2.5 mm/s')
                temp = 2.5 * 100
            case '4 mm/s':
                temp = 4 * 100
                print('4 mm/s')
            case '5.2 mm/s':
                temp = 5.2 * 100
                print('5.2 mm/s')
            case '10 mm/s':
                temp = 10 * 100
                print('10 mm/s')
            case _:
                temp = 100 * 100
                print("default 100 mm/s")

        tgt_pos_vel = str(f'{int(temp):0>4x}')

    def slider_event(self,value):
        self.slider_dist_label.configure(text= str(f"{value:.2f}"))
        # print(value)

if __name__ == '__main__':
    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    app = customtkinter.CTk(className='IAI Actuator Control')
    # set window size
    app.geometry("440x450")
    app.title("IAI control")
    #
    # app = tk.Tk(className='IAI Actuator Control')
    #
    # app.geometry("300x300")

    # # SerialReaderProtocolLine.tk_listener = main_frame
    # # Initiate serial port

    # Getting the current date and time
    dt = datetime.now()


    print("Date and time is:", dt.strftime(("%d %B, %Y, %H:%M:%S")))
    # timestamp in milliseconds
    # getting the timestamp
    ts = datetime.timestamp(dt) * 1000
    print(ts)

    main_frame = MainFrame()
    # Set listener to our reader
    while True:
        serial_port = connect(portname="COM4", baudrate=38400)
        if serial_port.isOpen():
            main_frame.connectionStatuslabel.configure(text="Connected")
            break
        else:
            main_frame.connectionStatuslabel.configure(text="Not Connected")
            main_frame.connectionStatuslabel.showerror("Error",f'Please Check Seria port' )

    SerialReaderProtocolRaw.tk_listener = main_frame
    reader = ReaderThread(serial_port, SerialReaderProtocolRaw)
    reader.start()
    # SerialReaderProtocolLine.tk_listener = main_frame
    # # Initiate serial port
    # serial_port = IAI_MODBUSascii_20221104.connect(portname="COM4", baudrate=38400)


    # Initiate ReaderThread
    #reader = IAI_MODBUSascii_20221104.ReaderThread(serial_port,IAI_MODBUSascii_20221104.SerialReaderProtocolRaw)
    # Start reader
    #reader.start()

    app.mainloop()