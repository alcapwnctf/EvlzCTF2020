#!/usr/bin/env python

import time

SS = input("What's the phrase amigo? \n").strip()
phrase = "Name's hui, huihui"

if SS == phrase:
    msg = "RECEIVING TRANSMISSION: welcome to the d4rk 5id3 (: ME likey PANGRAM"

    i = 1
    k = 0

    while i<=680:
        time.sleep(1)
        if i%68 == 0:
            print(msg[k])
            k+=1
            i+=1
        else:
            print(".")
            i+=1

if SS != phrase:
    print("NOPIDI NOPE!")
