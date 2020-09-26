"""A Hypervisor for EmzMachine.
"""
import random
import os
import threading
from .vm import EmzMachine

FLAG = os.getenv("FLAG", "evlz{1mm4_b4d_d3v1c3}ctf")

GPU_VRAM = 800

class EmzGpu:
    """Gpu for EmzMachine Hypervisor. """
    def __init__(self, **kwargs):
        self.vram = bytearray(bytes(GPU_VRAM))
        self.dma_handler = kwargs.get('dma_handler')
    
    def dma(self, lin_addr: int, size: int):
        vram_buf = self.dma_handler(lin_addr, size)
        for idx, (item) in enumerate(vram_buf[:GPU_VRAM]):
            self.vram[idx] = item
        
class EmzHypervisor:
    """Run a hypervisor to run EmzMachine VMs. """
    
    HYPERVISOR_ALLOC = 64
    """Space for hypervisor.
    """

    DEFAULT_EMZVM_IP = 0
    """EmzMachine VM instruction pointer. """
    
    DEFAULT_EMZVM_MEMSIZE = 1024
    """EmzMachine VM memsize """
    
    DEFAULT_EMZVM_MACHINE_STATE = {
        'A': 0,
        'B': 0,
        'C': 0,
        'TEXT': b'', 
        'FB': b'',
        'EXIT': 0,
        'HASGPU': 0,
        'VIRTUALIZED': 1,
        'EXIT': 0,
        'ERROR': 0,
    }
    """EmzMachine VM machine state with virtualization extensions. """
    
    HYPERCALLS = {
        'GETGPU': 0xAD,
    }
    
    def __init__(self, memsize):
        self.memsize = memsize
        self.memory = bytearray(memsize + self.HYPERVISOR_ALLOC)
        self.mem_lock = threading.Lock()
        self.vms = list()
        self._init_hypervisor_space()

        self.gpu = None
        self.gpu_assigned = -1
        self._init_gpu()

    def dma_handler(self, lin_addr: int, size: int):
        vm = self.vms[self.gpu_assigned]
        lower = vm[1]
        upper = vm[2]

        start = lower + lin_addr
        end = lower + lin_addr + size

        if (start < 0 or end > self.memsize + self.HYPERVISOR_ALLOC):
            return b''

        return self.memory[start:end]

    def hypercall_handler(self, vm_id: int, hypcall: int):
        if hypcall in self.HYPERCALLS.values():
            if hypcall == self.HYPERCALLS['GETGPU']:
                if self.gpu_assigned == -1:
                    self.gpu_assigned = vm_id
                    return self.gpu
                return None
        
    def _init_hypervisor_space(self):
        self.mem_lock.acquire()
        mem_idx = 0
        for char in FLAG:
            self.memory[mem_idx] = ord(char)
            mem_idx += 1

        self.mem_lock.release()
 
    def _init_gpu(self):
        self.gpu = EmzGpu(
            dma_handler=self.dma_handler
        )
 
    def _get_new_vm_bounds(self):
        base = self.HYPERVISOR_ALLOC
        lower = base + len(self.vms)*self.DEFAULT_EMZVM_MEMSIZE
        upper = lower + self.DEFAULT_EMZVM_MEMSIZE

        return lower, upper
 
    def add_vm(self, name: str, program: bytearray):
        lower, upper = self._get_new_vm_bounds()

        self.mem_lock.acquire()
        idx = lower
        for item in program[:self.DEFAULT_EMZVM_MEMSIZE]:
            self.memory[idx] = item
            idx += 1
        self.mem_lock.release()
        
        self.vms.append((name, lower, upper, EmzMachine(
            vm_id=len(self.vms),
            memory=self.memory[lower:upper],
            ip=int(self.DEFAULT_EMZVM_IP),
            machine_state=dict(self.DEFAULT_EMZVM_MACHINE_STATE),
            hypercall_handler=self.hypercall_handler
        )))

    def schedule(self):
        threads = [
            threading.Thread(target=vm_tuple[3].start)
            for vm_tuple in self.vms
        ]
        
        for vm_thread in threads:
            vm_thread.start()
        
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    HYPERVISOR_SIZE = 2048
    
    """Regular Code with GPU """
    PROGRAM = b'\xFD\xAD\xFC\x0A\x12\xFC\x0B\x22\xFC\x0C\x22\xF8\x65\x55\x00\xF9\x65\x55\xFF\xF7\xF6\xFF'

    """DMA Code """
    CONTROL_PROGRAM = b'\xFD\xAD\xF5\x00\x00\xa0\xFF'
    
    hyp = EmzHypervisor(
        HYPERVISOR_SIZE
    )

    vms = [
        threading.Thread(target=hyp.add_vm, args=('CONTROL', CONTROL_PROGRAM,)),
        threading.Thread(target=hyp.add_vm, args=('USER', PROGRAM,))
    ]
    random.shuffle(vms)

    for vm in vms:
        vm.start()
    for vm in vms:
        vm.join()

    hyp.schedule()

    for vm in hyp.vms:
        print(vm[0], vm[3].machine_state)
