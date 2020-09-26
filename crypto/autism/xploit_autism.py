#!/usr/bin/env python2

import sys,os
from pwn import *

HOST="crypto.game.alcapwnctf.in"
PORT=5200

def doManip(ct, keyA, keyB):
    pt = int(ct) ^ keyB
    flagchar = hex(pt)[2:].decode("hex")[0]
    ct = str(int(pt) ^ keyA)
    return flagchar,ct

def exploit(r):
    flag = ""

    for i in range(4):
        r.recvline()
    g = int(r.recvline().strip().split(": ")[1])
    p = int(r.recvline().strip().split(": ")[1])
    
    r.recvuntil("key: ")
    A = r.recvline().strip()

    r.recvuntil("key: ")
    B = r.recvline().strip()

    h = process("./helper")
    T = h.recvline().strip()
    
    h.sendline(A)
    keyA =int("".join(hex(x)[2:].zfill(2) for x in [int(y) for y in h.recvline().strip()[1:-1].split()]),16)
    h.sendline(B)
    keyB =int("".join(hex(x)[2:].zfill(2) for x in [int(y) for y in h.recvline().strip()[1:-1].split()]),16)
    h.close()

    for i in range(2):
        r.recvline()
        r.sendline(T)

    while True:
        data = r.recvline().strip().split()
        if "Thank" in data:
            flag = flag.split("?")
            flag = flag[0]+data[-1]+flag[-1]
            break
        else:
            flagchar, ct = doManip(data[-1], keyA, keyB)
            flag += flagchar
            r.recvline()
            r.sendline(ct)
    print flag
    return

if __name__ == "__main__":

    r = remote(HOST, PORT)
    exploit(r)

    sys.exit(0)
