import ctypes
import time

libfullpath = '/home/pi/pickledpicam/kellerp_i2c/libread_keller_ld.so'
keller_LD = ctypes.CDLL(libfullpath)

open_keller_LD = keller_LD.open_keller_LD
close_keller_LD = keller_LD.close_keller_LD
close_keller_LD.argtypes = [ctypes.c_int]
read_keller_LD = keller_LD.read_keller_LD
read_keller_LD.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_char),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double),ctypes.POINTER(ctypes.c_double)]

rx = ctypes.create_string_buffer(5)
p = ctypes.c_double()
T = ctypes.c_double()
stime = ctypes.c_double()
sensor = open_keller_LD()
while True:
    time.sleep(1)
    read_keller_LD(sensor,rx,ctypes.byref(p),ctypes.byref(T),ctypes.byref(stime))
    
close_keller_LD(sensor)
