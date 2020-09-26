"""Wrapper for emzvm.hypervisor to run a program with control program controlling I/O devices.
"""

import random
import time
from emzvm.hypervisor import EmzHypervisor
import threading

HYPERVISOR_SIZE = 2048

def run_program(program: bytes):
    random.seed(time.perf_counter())
    hyp = EmzHypervisor(HYPERVISOR_SIZE)

    """DMA Code """
    CONTROL_PROGRAM = b'\xFD\xAD\xF5\x00\x00\xa0\xf4\xFF'
    
    hyp = EmzHypervisor(
        HYPERVISOR_SIZE
    )

    vms = [
        threading.Thread(target=hyp.add_vm, args=('CONTROL', CONTROL_PROGRAM,)),
        threading.Thread(target=hyp.add_vm, args=('USER', program,))
    ]
    shuffle = random.random()
    if shuffle < 0.2:
        random.shuffle(vms)

    for vm in vms:
        vm.start()
    for vm in vms:
        vm.join()

    hyp.schedule()

    return hyp

if __name__ == "__main__":
    """Run an EmzMachine program in the EmzVm.
    """
    USER_PROGRAM = bytearray.fromhex(input('Input EMZ8000 Program\n'))

    hyp = run_program(USER_PROGRAM)

    for vm in hyp.vms:
        if vm[0] == 'USER':
            print(vm[3].machine_state)
