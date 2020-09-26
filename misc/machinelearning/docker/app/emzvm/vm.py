import os
import traceback
from typing import List, Dict, Tuple, Callable

"""EMZ8000 Machine Emulator

EMZ8000 Features

- Popek/Goldberg virtualization theorem conformant
- Attach IO Devices
- Emz intuitive ISA.

"""
DEBUG_VM = os.getenv('DEBUG_VM', False)


class OpHandlerNotFoundError(Exception):
    pass

class EmzMachine:
    """EmzMachine accepts a memory area and instruction pointer, executes the instructions in memory.

    If EmzMachine is virtualized, a hypercall can attach a GPU to the machine via the hypervisor. 
    """
    BYTEORDER = 'big'
    
    DEFAULT_MACHINE_STATE = {
        'A': 0,
        'B': 0,
        'C': 0,
        'TEXT': b'', 
        'FB': b'',
        'HASGPU': 0,
        'VIRTUALIZED': 0,
        'EXIT': 0,
        'ERROR': 0,
    }

    REGISTER_IDENTIFIERS = {
        0x0A: 'A',
        0x0B: 'B',
        0x0C: 'C',
    }

    FB_TERMINATOR = 0xFF
    TEXT_TERMINATOR = 0x00

    INSTRUCTIONS = {
        'EXIT': 0xFF,
        'HYPCALL': 0xFD,
        'SETREG': 0xFC,
        'ADDREG': 0xFB,
        'MULREG': 0xFA,
        'FILLFB': 0xF9,
        'FILLTEXT': 0xF8,
        'WRTEXT': 0xF7,
        'WRFB': 0xF6,
        'REQGPUDMA': 0xF5,
        'GPUWRFB': 0xF4,
    }

    OPCODES = {
        value: key
        for key, value in INSTRUCTIONS.items()
    }

    HYPERCALLS = {
        'GETGPU': 0xAD,
    }
    
    def _to_bytes(self, int_val: int) -> bytes:
        return (int_val).to_bytes(1, self.BYTEORDER)

    def _next(self):
        self.ip += 1
    
    def _byte(self) -> int:
        return self.memory[self.ip]
    
    def _next_byte(self) -> int:
        self._next()
        return self._byte()
    
    def _stdout(self, val):
        self.stdout.append(val)
    
    @property
    def virtualized(self):
        return self.machine_state['VIRTUALIZED']
    
    def __init__(self, memory: bytearray, ip: int, **kwargs):
        self.memory = memory
        self.ip = ip
        self.machine_state = kwargs.get('machine_state', self.DEFAULT_MACHINE_STATE)
        self.hypercall_handler = kwargs.get('hypercall_handler')
        self.vm_id = kwargs.get('vm_id')
        self.INST_HANDLERS = {
            'EXIT': self.exit_handler,
            'HYPCALL': self.hypcall_handler,
            'SETREG': self.setreg_handler,
            'ADDREG': self.addreg_handler,
            'MULREG': self.mulreg_handler,
            'FILLFB': self.fillfb_handler,
            'FILLTEXT': self.filltext_handler,
            'WRTEXT': self.wrtext_handler,
            'WRFB': self.wrfb_handler,
            'REQGPUDMA': self.reqgpudma_handler,
            'GPUWRFB': self.gpuwrfb_handler,
        }

        """Attach GPU via GETGPU hypercall.
        """
        self.gpu = None
        self.stdout = list()

    def exit_handler(self):
        self.machine_state['EXIT'] = 1

    def hypcall_handler(self):
        if self.virtualized:
            hypcall = self._next_byte()
            if hypcall in self.HYPERCALLS.values():
                response = self.hypercall_handler(self.vm_id, hypcall)
                if hypcall == self.HYPERCALLS['GETGPU']:
                    if response is not None:
                        self.gpu = response
                        self.machine_state['HASGPU'] = 1
    
    def setreg_handler(self):
        reg_id = self._next_byte()
        reg_val = self._next_byte()

        if reg_id in self.REGISTER_IDENTIFIERS:
            self.machine_state[self.REGISTER_IDENTIFIERS[reg_id]] = reg_val

    def addreg_handler(self):
        reg_first = self._next_byte()
        reg_second = self._next_byte()

        result = reg_first + reg_second

        self._stdout(f'{result}')

    def mulreg_handler(self):
        reg_first = self._next_byte()
        reg_second = self._next_byte()

        result = reg_first * reg_second

        self._stdout(f'{result}')

    def fillfb_handler(self):
        fb = b''
        data = self._next_byte()
        while data != self.FB_TERMINATOR:
            fb += self._to_bytes(data)
            data = self._next_byte()

        self.machine_state['FB'] = fb

    def filltext_handler(self):
        text = b''
        data = self._next_byte()
        while data != self.TEXT_TERMINATOR:
            text += self._to_bytes(data)
            data = self._next_byte()
        
        self.machine_state['TEXT'] = text

    def wrfb_handler(self):
        self._stdout(self.machine_state['FB'])

    def wrtext_handler(self):
        self._stdout(self.machine_state['TEXT'].decode())
    
    def reqgpudma_handler(self):
        if self.machine_state['HASGPU'] and self.gpu is not None:
            addr = self._to_bytes(self._next_byte())
            addr += self._to_bytes(self._next_byte())
            size = self._next_byte()
            
            lin_addr = int.from_bytes(addr, byteorder=self.BYTEORDER, signed=True)
            
            self.gpu.dma(lin_addr, size)

    def gpuwrfb_handler(self):
        if self.machine_state['HASGPU'] and self.gpu is not None:
            self.machine_state['FB'] = bytes(self.gpu.vram)

    def _get_emz_inst_handler(self, inst_opcode: int) -> Callable:
        """Return an instruction handler from self.INST_HANDLERS corresponding to inst_opcode. 
        """
        try:
            return self.INST_HANDLERS[self.OPCODES[inst_opcode]]
        except:
            raise OpHandlerNotFoundError()

    def _machine_loop(self):
        while self.ip <= len(self.memory):
            try:
                opcode = self._byte()
                if DEBUG_VM:
                    print(self.OPCODES[opcode], hex(opcode), self.ip, self.machine_state['HASGPU'])
                try:
                    handler = self._get_emz_inst_handler(opcode)
                    handler()
                except OpHandlerNotFoundError as e:
                    self.machine_state['ERROR'] = 1
                    self._stdout(f'failed executing opcode: {opcode}')
                    if DEBUG_VM:
                        traceback.print_exc()
                    return

                    
                if opcode == self.INSTRUCTIONS['EXIT']:
                    return
                if self.machine_state['ERROR']:
                    self._stdout('Error occured during execution.')
                    return
            except IndexError:
                self.machine_state['ERROR'] = 1
                self._stdout('Error accessing memory.')
                return
            except:
                self.machine_state['ERROR'] = 1
                traceback.print_exc()
                return

            self._next()

    def start(self):
        self._machine_loop()
    

if __name__ == "__main__":
    program = b'\xFC\x0A\x12\xFC\x0B\x22\xFC\x0C\x22\xF8\x65\x55\x00\xF9\x65\x55\xFF\xF7\xF6\xFF'
    
    vm = EmzMachine(
        memory=program,
        ip=0,
    )

    vm.start()

    print(vm.machine_state)
    print(vm.stdout)
