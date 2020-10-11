# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

F = lambda x, y, z: (x & y) | (~x & z)
G = lambda x, y, z: (x & z) | (y & ~z)
H = lambda x, y, z: x ^ y ^ z
I = lambda x, y, z: y ^ (x | ~z)
modular_add = lambda a, b: (a + b) % pow(2, 32)
rotate_left = lambda x, n: (x << n) | (x >> (32 - n))

init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

import bitarray
import struct
import numpy as np

K = [int(2**32*np.sin(i + 1)) for i in range(0,63)]
s='malothalis1997'

sb = bitarray.bitarray()
sb.frombytes(s.encode('utf-8'))
sb = sb + bitarray.bitarray('1')
sb = sb + bitarray.bitarray('0')

while (len(sb)%512)!=448:
    sb = sb + bitarray.bitarray('0')
    
length = (len(s) * 8) % pow(2, 64)
length_bit_array = bitarray.bitarray(endian="little")
length_bit_array.frombytes(struct.pack("<Q", length))
sb = sb + length_bit_array
message_digest = ""

for w in range(0,len(sb)%512 + 1):
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476
    for chunk_index in range(len(sb) // 16):
        AA = A
        BB = B
        CC = C
        DD = D
        for i in range(0,4):
            for j in range(1,16):
                if i==0:
                    g = (j*i)
                    temp = F(B, C, D)
                    s = [7, 12, 17, 22]
                if i==1:
                    g = (5*(i*j)+1)%16
                    temp = G(B,C,D)
                    s = [5,  9, 14, 20]
                if i==2:
                    g = (3*(i*j)+5)%16
                    temp = H(B,C,D)
                    s = [4, 11, 16, 23]
                if i==3: 
                    g = (7*i*j)%16
                    temp = I(B,C,D)
                    s = [6, 10, 15, 21]
                D = C
                C = B
                B = rotate_left((A + temp + K[i*j] + sb[(chunk_index*16)+g]), s[i]) + B
                A = temp
                print(hex(A))
                print(hex(B))
                print(hex(C))
                print(hex(D))
                break
        print("loop left")
        A = AA
        B = BB
        C = CC
        D = DD
        print(hex(AA))
        print(hex(BB))
        print(hex(CC))
        print(hex(DD))
        if chunk_index == 0:
            break
"""
print(hex(AA))
print(hex(BB))
print(hex(CC))
print(hex(DD))
"""

