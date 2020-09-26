#!/usr/bin/env python

from Crypto.Protocol.SecretSharing import Shamir
import Crypto.Cipher.AES as aes
import binascii
import base64
import random

PTs = [
     "You miss 100% of the shots you don't take. - Wayne Gretzky - Michael Scott",
     "That has sort of an oaky afterbirth.",
     "I'm an early bird and I'm a night owl so I'm wise and I have worms.",
     "I learned a while back that if I do not text 911 people do not return my calls. Um, but not people always return my calls because they think that something horrible has happened.",
     "I... Declare... Bankruptcy!",
     "I's Britney, bitch",
     "Where are the turtles?!",
     "You don't know me, you've just seen my penis.",
     "The worst thing about prison was the Dementors. They were flying all over the place and they were scary and they'd come down and they'd suck the soul out of your body and it hurt!",
     "And I knew exactly what to do. But in a much more real sense, I had no idea what to do.",
     "I feel like all my kids grew up and then they married each other. It's every parent's dream.",
     "I love inside jokes. I hope to be a part of one someday.",
     "If I had a gun with two bullets and I was in a room with Hitler, Bin Laden, and Toby, I would shoot Toby twice.",
     "You know what they say. 'Fool me once, strike one, but fool me twice...strike three.",
     "You cheated on me?....When I specifically asked you not to?",
     "I'm not superstitious, but I am a little stitious.",
     "Sometimes I'll start a sentence and I don't even know where it's going. I just hope I find it along the way.",
     "I am Beyonce, always.",
     "I have cause. It is beCAUSE I hate him.",
     "Would I rather be feared or loved? Easy. Both. I want people to be afraid of how much they love me.",
     "That's what she said.",
     "It is St. Patrick's Day. And here in Scranton, that is a huge deal. It is the closest that the Irish will ever get to Christmas.",
     "Society teaches us that having feelings and crying is bad and wrong. Well, that's baloney, because grief isn't wrong. There's such a thing as good grief. Just ask Charlie Brown.",
     "Wikipedia is the best thing ever. Anyone in the world can write anything they want about any subject so you know you are getting the best possible information.",
     "Do I need to be liked? Absolutely not. I like to be liked. I enjoy being liked. I have to be liked. But it's not like this compulsive need to be like my need to be praised."
    ]

def pad(pt):
    while len(pt)%16 != 0:
        pt+="x"
    return(pt)

print("\nHuiHui Industries is on a hiring spree of freshers for the role of a true Assistant to the Network Administrator.")
print("Their test is very basic. Wanna try?\n")

flag = "xxxxx cjumz evlz{Y0u_4r3_h1r3d}ctf fwmadug "
key = "huiRandom_Keyhui".encode()
cipher = aes.new(key, aes.MODE_ECB)
encrypted_flag = binascii.hexlify(cipher.encrypt(pad(flag).encode())).decode()

n = random.randint(20,24)
shares = Shamir.split(19, n, key, ssss=True)
score = 0

for i in range(n):
    cipher = aes.new(shares[i][1], aes.MODE_ECB)
    random_pt = PTs[random.randint(0,24)]
    encrypted_random_pt = binascii.hexlify(cipher.encrypt(pad(random_pt).encode())).decode()
    
    ED = random.randint(0,1)

    if ED == 0:
        print("haiyaa! Encrypt this: ")
        print(random_pt)
        print("using:", binascii.hexlify(shares[i][1]).decode())
        
        received_encrypted_random_pt = input("Enter Entrypted text(hex encoded, For padding use \"x\"): ")
        
        if received_encrypted_random_pt.strip() == encrypted_random_pt:
            print("Not impressed yet! \n")
            score += 1
        else:
            print("You are not qualified enough for the job. Go update firewall policies, n00b")
            break
    
    if ED == 1:
        print("huiyaa! Decrypt this: ")
        print(encrypted_random_pt)
        print("using: ", binascii.hexlify(shares[i][1]).decode())
        
        received_random_pt = input("Enter Decrypted version(Remove the pseudo-pad): ")
        
        if received_random_pt.strip() == random_pt:
            print("Not impressed yet! \n")
            score += 1
        else:
            print("You are not qualified enough for the job. Go update firewall policies, n00b")
            break
            
if (score == n):
    cipher = aes.new(key, aes.MODE_ECB)
    print(".\n.\nOkay, I'm impressed :] \nDecrypt this to receive your joining letter: ")
    print(encrypted_flag)

if (score != n):
    print("We wish you all the best for your future endaevours!")

exit(0)
