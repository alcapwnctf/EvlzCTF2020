#!/usr/bin/env python3
import json
import base64
from emzmachine import run_program

WELCOME_MESSAGE = """EmzMachine 8000
---------------

Input EmzMachine 8000 OpCodes (as hex string):
"""

if __name__ == "__main__":
    try:
        USER_PROGRAM = bytearray.fromhex(input(WELCOME_MESSAGE))
    except:
        print("Error occured in reading program.\nPlease input program as hexadecimal string.")
        exit(1)
    
    print('Program:', bytes(USER_PROGRAM))
    
    hyp = run_program(USER_PROGRAM)

    for vm in hyp.vms:
        if vm[0] == 'USER':            
            print("result:")
            for item in vm[3].stdout:
                print(item)
                
            print("machine state")
            machine_state = vm[3].machine_state
            machine_state['FB'] = base64.b64encode(machine_state['FB']).decode()
            machine_state['TEXT'] = machine_state['TEXT'].decode()
            print(json.dumps(machine_state))
    exit(0)
