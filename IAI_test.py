import serial
import time

SERVO_ON = ":01050403FF00F4\r\n"
MOVE_LOC0 = ":01069800000061\r\n"
MOVE_LOC1 = ":01069800000160\r\n"
MOVE_LOC5 = ":0106980000055C\r\n"
if __name__ == '__main__':
    s = serial.Serial("COM4", baudrate=38400, timeout=0.5)
    time.sleep(1)
    for count in range(3):
        data = SERVO_ON
        for i in data:
            s.write(bytearray(i,'ascii'))
        time.sleep(1)

        data = MOVE_LOC0
        for i in data:
            s.write(bytearray(i,'ascii'))

        time.sleep(2)
        data = MOVE_LOC1
        for i in data:
            s.write(bytearray(i,'ascii'))

        time.sleep(2)
        data = MOVE_LOC5
        for i in data:
            s.write(bytearray(i,'ascii'))