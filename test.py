from struct import *
record = b'raymond   \x32\x12\x08\x01\x08'
print(type(record))
name, serialnum, school, gradelevel = unpack('<10sHHb', record)
print(name,serialnum,school,gradelevel)
from collections import namedtuple
Student = namedtuple('Student', 'name serialnum school gradelevel')
Student._make(unpack('<10sHHb', record))