import timeit
from serial import Serial

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

# Data for Function Code 05
SERVO_ON = 'FF'
SERVO_OFF = '00'


#Function Code (06) Start address list
PMCR = '9800' # Position movement command register

#Positioning Data Direct Writing
PCMD ='9900' #Target position specification register

#Special characters
CR = 0x0D # carriage return '\r'
LF = 0x0A # line feed '\n'
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
    #print(int(temp_data[4],16))

    w = [total := total + int(i, 16) for i in temp_data]
    value = -w[-1] & 0xFF # mask off the FF
    #print(data, total, w, hex(value), [w[-1]])
    return value


def send_data(data):
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
    data.insert(0, 0X3A) # ASCII :
    data.insert(15,CR) # start address
    data.insert(16,LF) # start address

    try:

        serial_port.write(data.decode('string-escape'))
#        print(stringtosend)

    except:
        pass
        #raise HerkulexError("could not communicate with motors")

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
    data.append(tgt_pos[4])
    # print(f' before {data}')
    result = checksum(data)
    temp = f'{result:x}'  # remove the x
    # print(temp,temp[0])
    data.append(temp[0])
    data.append(temp[1])
    # print(data)
    send_data(data)

if __name__ == "__main__":
   servo_On()
   serial_port = Serial("COM4", baudrate=38400, timeout=0.5)
   MOVE_LOC5 = ":0106980000055C\r\n"
   num = 0
   test = f"{num:04}"
   move_loc(test)
   dist = 50 * 100

   move2Pos(tgt_pos)
#move_loc5=[0x01,0x06,0x98,0x00,0x00,0x05]
#data1 = [0x01,0x03,0x90,0x00,0x00,0x02]

# # arr2 = bytes(data1, 'ascii')
# # #s =str(data1).encode()L
# # print(arr2)
#i =[data1[i:i + 1] for i in range(0, len(data1), 1)]
#print(f"i {i}")
#result = checksum(data1)
#print(result)
# # w=zip(data1[::2], data1[1::2])
# # print(list(map(''.join, w)))
# # print(i)
# # print(w)
# # #lrCCheck('010390020001')
# #
# # print(timeit.Timer("data1 = '010390020001';[data1[i:i + 2] for i in range(0, len(data1), 2)]").repeat())
# # print(timeit.Timer("data1 = '010390020001';list(map(''.join,zip(data1[::2], data1[1::2])))").repeat())
# value=int(input("enter hexa decimal value for getting compliment values:="))
# value = str(value)
# highest_value="F"*len(value)
# print(highest_value)
# resulting_decimal=int(highest_value,16)-int(value,16)
# ones_compliment=hex(resulting_decimal)
# twos_compliment=hex(resulting_decimal+1)
# print(f'ones compliment={ones_compliment}\n twos complimet={twos_compliment}')
