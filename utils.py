"""Low level interface to Terraria data"""
from struct import unpack, pack, Struct
import sys


is_exe = hasattr(sys, "frozen")
### Parser for .wld data types ###
def decode7bit(bytes):
    lbytes = list(bytes)
    value = 0
    shift = 0
    while True:
        byteval = lbytes.pop(0)
        if (byteval & 128) == 0: break
        value |= ((byteval & 0x7F) << shift)
        shift += 7
    return (value | (byteval << shift))


def encode7bit(value):
    temp = value
    bytes = ""
    while temp >= 128:
        bytes += chr(0x000000FF & (temp | 0x80))
        temp >>= 7
    bytes += chr(temp)
    return bytes


def get_long_string(f):
    namelen = decode7bit(f.read(2))  # int(unpack("<B", f.read(1))[0])
    if namelen < 127:
        f.seek(-1, 1)
    name = unpack("<" + str(namelen) + "s", f.read(namelen))[0].decode()
    return name


formats = (  # ("word" , "<H", 2),
             ("byte", "<B", 1),
             ("short", "<h", 2),
             ("ushort", "<H", 2),
             ("int", "<I", 4),
             ("uint", "<i", 4),
             ("long", "<Q", 8),
             ("double", "<d", 8),
             ("float", "<f", 4),
             )


def get_short(f, num=1):
    if num == 1:
        return unpack("<h", f.read(2))[0]
    return unpack("<" + "h" * num, f.read(2 * num))


def get_ushort(f, num=1):
    if num == 1:
        return unpack("<H", f.read(2))[0]
    return unpack("<" + "H" * num, f.read(2 * num))


def get_uint(f, num=1):
    if num == 1:
        return unpack("<I", f.read(4))[0]
    return unpack("<" + "I" * num, f.read(num * 4))


def get_int(f, num=1):
    if num == 1:
        return unpack("<i", f.read(4))[0]
    return unpack("<" + "i" * num, f.read(num * 4))


def get_long(f, num=1):
    if num == 1:
        return unpack("<Q", f.read(8))[0]
    return unpack("<" + "Q" * num, f.read(num * 8))


def get_byte(f, num=1):
    if num == 1:
        return unpack("<B", f.read(1))[0]
    return unpack("<" + "B" * num, f.read(num))


def get_bool(f):
    return unpack('?', f.read(1))[0]


def get_double(f, num=1):
    if num == 1:
        return unpack("<d", f.read(8))[0]
    return unpack("<" + "d" * num, f.read(num * 8))


def get_float(f, num=1):
    if num == 1:
        return unpack("<f", f.read(4))[0]
    return unpack("<" + "f" * num, f.read(num * 4))


def set_bool(data):
    return pack('?', data)


def set_uint(data):
    return pack("<I", data)


def set_int(data):
    return pack("<i", data)


def set_long(data):
    return pack("<Q", data)


def set_ushort(data):
    return pack("<H", data)


def set_short(data):
    return pack("<h", data)


#def set_word(data):
#    return pack("<H", data)
def set_byte(data):
    return pack("<B", data)


def get_string(f):
    namelen = int(unpack("<B", f.read(1))[0])
    return unpack("<" + str(namelen) + "s", f.read(namelen))[0].decode()


def set_string(data):
    if len(data) > 126:
        return encode7bit(len(data)) + pack("<" + str(len(data)) + "s", str.encode(data))
        #return encode7bit(len(data))+pack("<"+len(data)*"s",*data)
    else:
        return pack("<B", len(data)) + pack("<" + str(len(data)) + "s", str.encode(data))
        #return pack("<B", len(data))+pack("<"+len(data)*"s",*data)


def set_double(data):
    return pack("<d", data)


def set_float(data):
    return pack("<f", data)
