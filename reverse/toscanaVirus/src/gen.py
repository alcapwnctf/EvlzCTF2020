import random
flag='evlz{QU!k_h1d3_y0u$_d347h_4ppr04ch35}ctf'
shift= []
counter = 0
for i in range(len(flag)):
    n = random.randint(1,9)
    print("bit_array.push_back({});".format(n))
    shift.append(n)
    counter +=1

counter2 = 0

for i in flag:
     x = ord(i) <<  shift[counter2]
     print("padd_array.push_back({});".format(x))
     counter2+=1

