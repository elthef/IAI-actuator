import tkinter as tk
import time
import threading
from serial import Serial
from serial.threaded import ReaderThread, Protocol, LineReader

HOME =":0105040BFF00EC\r\n"
SERVO_ON = ":01050403FF00F4\r\n"
MOVE_LOC0 = ":01069800000061\r\n"
MOVE_LOC1 = ":01069800000160\r\n"
MOVE_LOC2 = ":0106980000025F\r\n"
MOVE_LOC3 = ":0106980000035E\r\n"
MOVE_LOC4 = ":0106980000045D\r\n"
MOVE_LOC5 = ":0106980000055C\r\n"
CurrentPos =":0103900000026A\r\n"

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
    print("in MovePos")
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

    data = MOVE_LOC5
    for i in data:
        serial_port.write(bytearray(i, 'ascii'))
    # data = CurrentPos
    # for i in data:
    #      serial_port.write(bytearray(i, 'ascii'))
    time.sleep(1)

def MoveCallBack():
   #messagebox.showinfo( "Hello Python", "Hello World")
   # data = CurrentPos
   # for i in data:
   #      serial_port.write(bytearray(i, 'ascii'))
   t1 = threading.Thread(target=MovePos)
   t2 = threading.Thread(target=readPostCallBack)

   t1.start()
   time.sleep(0.1)
   # t2.start()
   # Create a list of jobs and then iterate through
   # the number of threads appending each thread to
   # the job list
   # jobs = []
   # for i in range(5):
   #  thread = threading.Thread(target=readPostCallBack)
   #  jobs.append(thread)
   #  # Start the threads (i.e. calculate the random number lists)
   # for j in jobs:
   #      j.start()
   #      #time.sleep(1)
   #
   #  # Ensure all of the threads have finished
   # for j in jobs:
   #      j.join()

def readPostCallBack():
    data = CurrentPos
    for i in data:
         serial_port.write(bytearray(i, 'ascii'))

class MainFrame(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        scrollbar = tk.Scrollbar(self, orient="vertical")
        self.listbox = tk.Listbox(self,width=50, height=20, yscrollcommand=scrollbar.set)
        #self.listbox = tk.Listbox(self)
        self.button = tk.Button(app, text="Start", command=startCallBack)
        self.button.pack()
        self.button1 = tk.Button(app, text="Move", command=MoveCallBack)
        self.button1.pack()
        self.buttonRead = tk.Button(app, text="Read Position", command=readPostCallBack)
        self.buttonRead.pack()
        self.listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.pack()

    def on_data(self, data):
        print("Called from tk Thread:", data)

        try:
            if data[3] == '3':
                print("22")
                pos_data = data[6:14]
                strings = [str(pos) for pos in pos_data]
                a_string = "".join(strings)
                an_integer = int(a_string,16)*0.01
                print(f"postition: {an_integer} mm")
                self.listbox.insert(tk.END, an_integer)
        except:
            print("error",len(data))




    # Initiate serial port
serial_port = Serial("COM4", baudrate=38400, timeout=0.5)

if __name__ == '__main__':

    app = tk.Tk(className='IAI Actuator Control')
    # set window size
    app.geometry("300x300")

    main_frame = MainFrame()
    # Set listener to our reader
    SerialReaderProtocolRaw.tk_listener = main_frame
    # SerialReaderProtocolLine.tk_listener = main_frame
    # # Initiate serial port
    # serial_port = Serial("COM4", baudrate=38400, timeout=0.5)

    # Initiate ReaderThread
    reader = ReaderThread(serial_port, SerialReaderProtocolRaw)
    # Start reader
    reader.start()

    app.mainloop()