import tkinter as tk
from tkinter import messagebox
import time
import serial
from serial import Serial
from serial.threaded import ReaderThread, Protocol
SERVO_ON = ":01050403FF00F4\r\n"
MOVE_LOC0 = ":01069800000061\r\n"
MOVE_LOC1 = ":01069800000160\r\n"
MOVE_LOC2 = ":0106980000025F\r\n"
MOVE_LOC3 = ":0106980000035E\r\n"
MOVE_LOC4 = ":0106980000045D\r\n"
MOVE_LOC5 = ":0106980000055C\r\n"
CurrentPos =":0103900000026A\r\n"

def startCallBack():
   #messagebox.showinfo( "Hello Python", "Hello World")
   # Initiate serial port

   data = SERVO_ON
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))

   data = CurrentPos
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))

   time.sleep(1)


   data = MOVE_LOC0
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))

   data = CurrentPos
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))

   time.sleep(300/1000)

   data = MOVE_LOC1
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))

   data = CurrentPos
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))

   time.sleep(300/ 1000)

   data = MOVE_LOC2
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))
   data = CurrentPos
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))

   time.sleep(300/ 1000)

   data = MOVE_LOC3
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))
   data = CurrentPos
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))
   time.sleep(300/1000)

   data = MOVE_LOC4
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))
   data = CurrentPos
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))
   time.sleep(300 / 1000)

   data = MOVE_LOC5
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))
   data = CurrentPos
   for i in data:
        serial_port.write(bytearray(i, 'ascii'))
   time.sleep(300/1000)

app = tk.Tk()
label = tk.Label(text="A Label")
B = tk.Button(app, text ="Start", command = startCallBack)
label.pack()
B.pack()

class SerialReaderProtocolRaw(Protocol):
    port = None

    def connection_made(self, transport):
        """Called when reader thread is started"""
        print("Connected, ready to receive data...")

    def data_received(self, data):
        """Called with snippets received from the serial port"""
        print("RX DATA")
        updateLabelData(data)

def updateLabelData(data):
    #data = data.decode("ascii")
    label['text'] = data
    app.update_idletasks()

serial_port = serial.Serial("COM4", baudrate=38400, timeout=0.5)

# Initiate ReaderThread
reader = ReaderThread(serial_port, SerialReaderProtocolRaw)
# Start reader
reader.start()

app.mainloop()