# -*- coding: utf-8 -*-
"""
Spyder Editor

Compute the md5 hash of a string input
"""

### Imports 
import bitarray
import struct
import numpy as np
import sys

### Functions used during the md5 process
F = lambda x, y, z: (x & y) | (~x & z)
G = lambda x, y, z: (x & z) | (y & ~z)
H = lambda x, y, z: x ^ y ^ z
I = lambda x, y, z: y ^ (x | ~z)
modular_add = lambda a, b: (a + b) % pow(2, 32)
rotate_left = lambda x, n: (x << n) | (x >> (32 - n))

### Constant added at each iteration
K = [int(2**32*np.sin(i + 1)) for i in range(0,63)]

s=sys.argv[1]
"""
Step1 of the md5 hash process. 
We pad our input with 0 until the rest of the division of len(input) by 512 is equal to 448
"""
def step1(s):
    sb = bitarray.bitarray()
    sb.frombytes(s.encode('utf-8'))
    sb = sb + bitarray.bitarray('1')
    while (len(sb)%512)!=448:
        sb = sb + bitarray.bitarray('0')
    return sb

"""
Step2 of the md5 hash process
We pad the input with its initial length, coded on 68 bits, making the sequence 512 bits long
"""
def step2(s,sb):
    length = len(s) * 8
    length_bit_array = bitarray.bitarray(endian="little")
    length_bit_array.frombytes(struct.pack("<Q", length))
    sb = sb + length_bit_array
    return sb
"""
Step3 of the md5 hash process
Loop over 32 chunk of 16 bits then loop 64 times to compute so operations mixing 
the initial values A,B,C,D and the chunks of the message
"""
def step3(sb):
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
                    B = modular_add(rotate_left((A + temp + K[i*j] + sb[(chunk_index*16)+g]), s[i]), s[i]+B)
                    A = temp
            AA = A
            BB = B
            CC = C
            DD = D
    return AA,BB,CC,DD


"""
Step4 of the md5 process
Concatenate the output of the previous loop
"""
def step4(A,B,C,D):
    message_digest = str(hex(A)) + str(hex(B)) + str(hex(C)) + str(hex(C))
    message_digest = message_digest[1:].replace("0x","")
    return message_digest


if __name__ == "__main__":
    sb = step1(s)
    sb = step2(s,sb)
    A,B,C,D = step3(sb)
    message_digest = step4(A,B,C,D)
    print(message_digest)
