from _future_ import print_function
from pynq import Overlay
from pynq import MMIO
import numpy as np
import struct
import binascii
import cmath
import random
import matplotlib.pyplot as plt
import sys
import time

overlay = Overlay("/home/xilinx/IPBitFile/matrix_multiply.bit")
overlay.download()
regIP = overlay.matrix_multiply_0
def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])
def hex_to_float(f):
    return float(struct.unpack('<f', struct.pack('<I', f))[0])


A = np.random.rand(3,3);
B = np.random.rand(3,3);
C_gold = A @ B

for i in range(3):
    for j in range(3):
        regIP.write(0x40 + 4*(i*3+j), int(float_to_hex(A[i][j]), 0))
        regIP.write(0x80 + 4*(i*3+j), int(float_to_hex(B[i][j]), 0))

time.sleep(1)

C_ans = np.zeros((3,3))

for i in range(3):
    for j in range(3):
        c = regIP.read(0xc0 + 4*(i*3+j))
        C_ans [i][j] = hex_to_float(c)

print ('-------Start Simulation-------')
print ('Input A : ')
print (A)
print ('Input B : ')
print (B)
print ('Golden C : ')
print (C_gold)
print ('Your C : ')
print (C_ans)
print ('--------End Simulation--------')