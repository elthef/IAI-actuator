import tkinter as tk
import time
import threading
from serial import Serial
from serial.threaded import ReaderThread, Protocol, LineReader
import customtkinter

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

speed_combValues = ['5 mm/s', '10 mm/s', '15 mm/s']

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
        if self._should_continue: # Code could have been running when cancel was called.
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
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.cancel()
        else:
            print("Timer never started or failed to initialize.")
    def stop(self):
        if self.thread is not None:
            self._should_continue = False # Just in case thread is running and cancel fails.
            self.thread.stop()

class SerialReaderProtocolRaw(Protocol):
    tk_listener = None

    def connection_made(self, transport):
        """Called when reader thread is started"""
        if self.tk_listener is None:
            raise Exception("tk_listener must be set before connecting to the socket!")
        print("Connected, ready to receive data...")

    def data_received(self, data):
        """Called with snippets received from the serial port"""
        self.tk_listener.after(0, self.tk_listener.on_data, data.decode())


class SerialReaderProtocolLine(LineReader):
    tk_listener = None
    TERMINATOR = b'\n\r'

    def connection_made(self, transport):
        """Called when reader thread is started"""
        if self.tk_listener is None:
            raise Exception("tk_listener must be set before connecting to the socket!")
        super().connection_made(transport)
        print("Connected, ready to receive data...")

    def handle_line(self, line):
        """New line waiting to be processed"""
        # Execute our callback in tk
        self.tk_listener.after(0, self.tk_listener.on_data, line)

def startCallBack():
    # Initiate serial port
    # messagebox.showinfo( "Hello Python", "Hello World")
    data = SERVO_ON
    for i in data:
        serial_port.write(bytearray(i, 'ascii'))

def MovePos():
    global t
    #print("in MovePos")
    data = MOVE_LOC0
    for i in data:
        serial_port.write(bytearray(i, 'ascii'))

    # data = CurrentPos
    # for i in data:
    #      serial_port.write(bytearray(i, 'ascii'))
    #
    # time.sleep(1)
    #
    # data = MOVE_LOC1
    # for i in data:
    #      serial_port.write(bytearray(i, 'ascii'))
    #
    # # data = CurrentPos
    # # for i in data:
    # #      serial_port.write(bytearray(i, 'ascii'))
    #
    # time.sleep(1)
    #
    # data = MOVE_LOC2
    # for i in data:
    #      serial_port.write(bytearray(i, 'ascii'))
    # # data = CurrentPos
    # # for i in data:
    # #      serial_port.write(bytearray(i, 'ascii'))
    #
    # time.sleep(1)
    #
    # data = MOVE_LOC3
    # for i in data:
    #      serial_port.write(bytearray(i, 'ascii'))
    # # data = CurrentPos
    # # for i in data:
    # #      serial_port.write(bytearray(i, 'ascii'))
    # time.sleep(1)
    #
    # data = MOVE_LOC4
    # for i in data:
    #      serial_port.write(bytearray(i, 'ascii'))
    # # data = CurrentPos
    # # for i in data:
    # #      serial_port.write(bytearray(i, 'ascii'))
    #
    time.sleep(1)

    data = MOVE_LOC5#FiftymmPos#FiftymmPos#MOVE_LOC5
    for i in data:
        serial_port.write(bytearray(i, 'ascii'))
    # data = CurrentPos
    # for i in data:
    #      serial_port.write(bytearray(i, 'ascii'))
    time.sleep(1)

    # create a thread timer object
    # timer = Timer(3, task, args=('Hello world',))
    # timer = threading.Timer(0.5, readPostCallBack)
    # timer = RepeatTimer(1, dummyfn)
    # timer.start()
    t = InfiniteTimer(0.001, readPostCallBack)
    t.start()


def MoveCallBack(pos):
   global MF_tgt_pos

   MF_tgt_pos = float(pos)
   #tgt_pos = 180 # in mm
   #print(f"text entry: {pos}")
   t1 = threading.Thread(target=MovePos)

   # Start the threads
   t1.start()


def readPostCallBack():
    data = CurrentPos
    for i in data:
         serial_port.write(bytearray(i, 'ascii'))

def lrCCheck():
    pass

class MainFrame(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # scrollbar = tk.Scrollbar(self, orient="vertical")
        # self.listbox = tk.Listbox(self,width=50, height=20, yscrollcommand=scrollbar.set)
        #self.listbox = tk.Listbox(self)

        self.frame = customtkinter.CTkFrame(master=app, width=600, height=240, corner_radius=15)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)
        # combo box
        # Label
        self.speedlabel = customtkinter.CTkLabel(master=self.frame,text="Speed (mm/s)", justify=tk.LEFT)
        self.speedlabel.place(x=80.5, y=20.5, anchor=tk.CENTER)
        self.speedlabel.grid(row=2, column=0, columnspan=1, padx=10, pady=10, sticky="e")
        
        combobox_speedvar = customtkinter.StringVar(value='5 mm/s')  # set initial value
        self.combobox_speed = customtkinter.CTkComboBox(master=self.frame,values=speed_combValues,
                                                        command=self.combobox_speed_selection)
        self.combobox_speed.grid(row=2, column=1, columnspan=1, pady=5, padx=5, sticky="e")

        self.label = customtkinter.CTkLabel(master=self.frame,text="Position (mm)", justify=tk.LEFT)
        self.label.place(x=20.5, y=20.5, anchor=tk.CENTER)
        self.label.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="e")

        int_var = tk.IntVar()
        self.entry = customtkinter.CTkEntry(master=self.frame, textvariable=int_var)
        self.entry.place(x=50.5, y=100.5, anchor=tk.CENTER)
        self.entry.grid(row=3, column=1, columnspan=1, padx=10, pady=10, sticky="e")

        self.button = customtkinter.CTkButton(master=self.frame, text="Start",command=startCallBack)
        self.button.place(x=20.5, y=0.5, anchor=tk.CENTER)
        self.button.grid(row=5, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")

        self.buttonMove = customtkinter.CTkButton(master=self.frame, text="Move",command = lambda: MoveCallBack(int_var.get()))
        self.buttonMove.grid(row=6, column=0, columnspan=2, padx=20, pady=10, sticky="ew")


    def on_data(self, data):
        #print("Called from tk Thread:", data)

        try:
            if data[3] == '3':
                #print("22")
                pos_data = data[6:14]
                strings = [str(pos) for pos in pos_data]
                a_string = "".join(strings)
                an_integer = int(a_string,16)*0.01
                print(f"tgt position {MF_tgt_pos:.2f} postition: {an_integer:.2f} mm ")
                if   an_integer >= MF_tgt_pos:
                    print("stop")
                    t.stop()
        except:
            pass
            #print("error",len(data))


    def combobox_speed_selection(self,event):
        # Three methods here all get the same value.
        #print("change")
        print(event)

if __name__ == '__main__':
    customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"
    app = customtkinter.CTk(className='IAI Actuator Control')
    # set window size
    app.geometry("400x300")
    app.title("IAI control")
    #
    # app = tk.Tk(className='IAI Actuator Control')
    #
    # app.geometry("300x300")

    main_frame = MainFrame()
    # Set listener to our reader
    #SerialReaderProtocolRaw.tk_listener = main_frame
    # SerialReaderProtocolLine.tk_listener = main_frame
    # # Initiate serial port
    # serial_port = Serial("COM4", baudrate=38400, timeout=0.5)

    # Initiate ReaderThread
#    reader = ReaderThread(serial_port, SerialReaderProtocolRaw)
    # Start reader
#    reader.start()

    app.mainloop()
