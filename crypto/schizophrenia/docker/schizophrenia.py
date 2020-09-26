#!/usr/bin/env python

import os
import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

"""  
    Implements a compressed challenge-response authentication protocol.

    Alice wants to talk to Bob,
    both of them want to prove their identity to each other.
"""
PROTOCOL_TEXT = """ 
    A is Alice's Identity
    B is Bob's Identity

    Kab is the pre-shared secret key between Alice and Bob.
    This secret key is used encrypt challenges received by Alice or Bob,
    and the encrypted text is sent back as the response to the challenge.

    Ra is the challenge sent by Alice to Bob
    Rb is the challenge sent by Bob to Alice.

    Kab(Ra) is Bob's response to Alice's challenge.
    Kab(Rb) is Alice's response to Bob's challenge

    Protocol

        1. Alice ------- [ A, Ra ]  -------> Bob
        2. Alice <---- [ Rb, Kab(Ra) ] ----- Bob
        3. Alice ------ [ Kab(Rb) ]  ------> Bob

    Implementation
        - AES-256-GCM used for encryption using Kab.
        - The IV is fixed to 16 null bytes.
    """

FLAG = "evlz{sch1z0phr3n1a_0r_jus7_m3nt4l_1lln3s5}ctf"

PSK_FILE = "/home/schizophrenia/.PSK"

AUTHENTICATED = False

CHALLENGE_NAME = "Alice"

FIXED_IV = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

class Bob:
    """ Implements Bob in the challenge-response authentication protcol. """
    
    def __init__(self, *args, **kwargs):
        self.psk = b'\x71\x5a\x73\xd8\x4e\xed\xf9\xac\xa6\x92\x84\x78\xae\x2d\xa5\x80'

    def encrypt(self, buffer):
        """ encrypt the buffer using self.cipher 
        @param bytes buffer: buffer to encrypt (base64)

        @return bytes: encrypted buffer
        """
        cipher = AES.new(self.psk, AES.MODE_GCM, FIXED_IV)
        ct_bytes = cipher.encrypt(pad(buffer, AES.block_size))
        return base64.b64encode(ct_bytes)

    def decrypt(self, buffer):
        """ decrypt the buffer using self.cipher 
        @param str buffer: buffer to decrypt (base64)
        
        @return bytes: decrypted buffer
        """
        try:
            ct = base64.b64decode(buffer)
        except:
            print('f a i l')
            return bytes('fail')

        cipher = AES.new(self.psk, AES.MODE_GCM, FIXED_IV)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt

bob = Bob()

def challenge():
    global AUTHENTICATED

    print('Who are you?')

    name = str(input("Name?: "))
    print(f"You are {name}?")

    if name != CHALLENGE_NAME:
        print("Bob not talk to you! Get out!")
        return

    challenge = str(input('Challenge for Bob (in Base64): ')).rstrip()
    
    try:
        challenge_ct = bob.encrypt(base64.b64decode(challenge))
    except:
        print("f a i l")
        return
    
    bob_challenge = get_random_bytes(32)
    bob_challenge_ct = bob.encrypt(bob_challenge)
    
    print(f"Response: {challenge_ct.decode()}")
    print(f"Bob challenge to {name}: {base64.b64encode(bob_challenge).decode()}")

    response = input("Response for Bob: ")
    if response == bob_challenge_ct.decode():
        print("Hi Alice! Bob has been waiting for you so long.")
        AUTHENTICATED = True
    else:
        print("Bob don't know you!")

def read_flag():
    if AUTHENTICATED:
        print()
        print(f'Flag: {FLAG}')
    else:
        ct = bob.encrypt(bytes(FLAG, encoding='utf-8'))
        print()
        print(f'Encrypted Flag: {ct.decode()}')

def protocol():
    print(PROTOCOL_TEXT)

def bob_out():
    exit(0)

ACTION_STRATEGY = {
    '1': challenge,
    '2': read_flag,
    '3': protocol,
    '4': bob_out,
}

if __name__ == "__main__":
    print('Hi, I am Bob! Are you Alice? Bob only talks to Alice.\nChallenge me if you are Alice!\n')

    while True:
        print('1. Challenge me!\n2. Read flag\n3. Protocol\n4. Exit\n')
        choice = str(input('Select: '))
        action = ACTION_STRATEGY.get(choice, None)
        if action is not None:
            action()
