import asyncio
import serial_asyncio
import time

SERVO_ON = ":01050403FF00F4\r\n"
MOVE_LOC0 = ":01069800000061\r\n"
MOVE_LOC1 = ":01069800000160\r\n"
MOVE_LOC2 = ":0106980000025F\r\n"
MOVE_LOC3 = ":0106980000035E\r\n"
MOVE_LOC4 = ":0106980000045D\r\n"
MOVE_LOC5 = ":0106980000055C\r\n"
CurrentPos =":0103900000026A\r\n"

class OutputProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport

        data = SERVO_ON
        for i in data:
            transport.write(bytearray(i, 'ascii'))

        time.sleep(1000 / 1000)

        data = MOVE_LOC5
        for i in data:
            transport.write(bytearray(i, 'ascii'))
        #transport.write(b'Hello, World!\n')  # Write serial data via transport

        time.sleep(1000 / 1000)

    def data_received(self, data):
        print('data received', repr(data))
        if b'\n' in data:
            self.transport.close()

    def connection_lost(self, exc):
        print('port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('resume writing')

loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(loop, OutputProtocol, "COM4", baudrate=38400, timeout=0.5)
transport, protocol = loop.run_until_complete(coro)
loop.run_forever()
loop.close()
