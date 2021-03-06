# -*- coding: utf-8 -*-
"""
Compute the md5 hash of a string input
"""

### Imports
import sys
import bitarray
import struct
import numpy as np


### Functions used during the md5 process
F = lambda x, y, z: (x & y) | (~x & z)
G = lambda x, y, z: (x & z) | (y & ~z)
H = lambda x, y, z: x ^ y ^ z
I = lambda x, y, z: y ^ (x | ~z)
modular_add = lambda a, b: (a + b) % pow(2, 32)
rotate_left = lambda x, n: (x << n) | (x >> (32 - n))


### Constant added at each iteration
K = [int(2 ** 32 * np.sin(i + 1)) for i in range(0, 63)]


### String to encode
s = sys.argv[1]


def step1(*, s: str) -> str:
    """
    Step1 of the md5 hash process.
    We pad our input with 0 until the rest of the division of len(input) by 512 is equal to 448
    Args :
     - s : string to encode
    """
    sb = bitarray.bitarray()
    sb.frombytes(s.encode("utf-8"))
    sb = sb + bitarray.bitarray("1")
    while (len(sb) % 512) != 448:
        sb = sb + bitarray.bitarray("0")
    return sb


def step2(*, s: str, sb: str) -> str:
    """
    Step2 of the md5 hash process
    We pad the input with its initial length, coded on 68 bits, making the sequence 512 bits long
    Args :
     - s : String to encode
     - sb : output of the first step of the md5 algorithm
    """
    length = len(s) * 8
    length_bit_array = bitarray.bitarray(endian="little")
    length_bit_array.frombytes(struct.pack("<Q", length))
    sb = sb + length_bit_array
    return sb


def step3(*, sb: str) -> str:
    """
    Step3 of the md5 hash process
    Loop over 32 chunk of 16 bits then loop 64 times to compute so operations mixing
    the initial values A,B,C,D and the chunks of the message
    Args :
     - sb : output of the 2nd step of encoding
    """
    for w in range(0, len(sb) % 512 + 1):
        A = 0x67452301
        B = 0xEFCDAB89
        C = 0x98BADCFE
        D = 0x10325476
        for chunk_index in range(len(sb) // 16):
            AA = A
            BB = B
            CC = C
            DD = D
            for i in range(0, 4):
                for j in range(1, 16):
                    if i == 0:
                        g = j * i
                        temp = F(B, C, D)
                        s = [7, 12, 17, 22]
                    if i == 1:
                        g = (5 * (i * j) + 1) % 16
                        temp = G(B, C, D)
                        s = [5, 9, 14, 20]
                    if i == 2:
                        g = (3 * (i * j) + 5) % 16
                        temp = H(B, C, D)
                        s = [4, 11, 16, 23]
                    if i == 3:
                        g = (7 * i * j) % 16
                        temp = I(B, C, D)
                        s = [6, 10, 15, 21]
                    D = C
                    C = B
                    B = modular_add(
                        rotate_left(
                            (A + temp + K[i * j] + sb[(chunk_index * 16) + g]), s[i]
                        ),
                        s[i] + B,
                    )
                    A = temp
            AA = A
            BB = B
            CC = C
            DD = D
    return AA, BB, CC, DD


def step4(*, A: str, B: str, C: str, D: str) -> str:
    """
    Step4 of the md5 process
    Concatenate the output of the previous loop to create the digest
    Args :
     -A, B, C, D are the output of the previous step
    """
    message_digest = str(hex(A)) + str(hex(B)) + str(hex(C)) + str(hex(C))
    message_digest = message_digest[1:].replace("0x", "")
    return message_digest


if __name__ == "__main__":
    sb = step1(s=s)
    sb = step2(s=s, sb=sb)
    A, B, C, D = step3(sb=sb)
    message_digest = step4(A=A, B=B, C=C, D=D)
    print(message_digest)
