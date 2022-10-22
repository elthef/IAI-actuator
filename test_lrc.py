import timeit
MOVE_LOC5 = ":0106980000055C\r\n"
CurrentPos =":0103900000026A\r\n"
def lrCCheck(data):
    sum = 0
    # for value in data:
    #     an_integer = int(value, 16)
    #
    #     hex_value = hex(an_integer)
    #     sum |= hex_value
    #     print(f'sum {~(sum)} {sum} value{hex_value} ')
    w = [sum := sum + i for i in data]
    value = -w[-1] &0xFF
    print(hex(value),[w[-1]])

move_loc5=[0x01,0x06,0x98,0x00,0x00,0x05]
data1 = [0x01,0x03,0x90,0x00,0x00,0x02]

# # arr2 = bytes(data1, 'ascii')
# # #s =str(data1).encode()
# # print(arr2)
#i =[data1[i:i + 1] for i in range(0, len(data1), 1)]
#print(f"i {i}")
result = lrCCheck(data1)
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
    datalength = len(data)
    csm1 = checksum1(data, datalength)
    csm2 = checksum2(csm1)
    data.insert(0, 0xFF)
    data.insert(1, 0xFF)
    data.insert(5, csm1)
    data.insert(6, csm2)
    stringtosend = ""
    for i in range(len(data)):
        byteformat = '%02X' % data[i]
        stringtosend = stringtosend + "\\x" + byteformat

    try:

        SERPORT.write(stringtosend.decode('string-escape'))
#        print(stringtosend)

    except:
        raise HerkulexError("could not communicate with motors")
