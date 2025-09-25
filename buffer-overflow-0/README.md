<img width="622" height="476" alt="image" src="https://github.com/user-attachments/assets/2bef9dad-3c1a-446b-973d-51c0cf9d9349" />


Chương trình nhập vào một chuỗi, sau đó kết thúc.<br>

<img width="435" height="107" alt="Pasted image 20250925095851" src="https://github.com/user-attachments/assets/71581f69-6fb6-4f43-bdf0-4aed0bb09431" />

Dùng `file` để kiểm tra, phát hiện đây là ELF 32-bit, little endian:<br>
<img width="1881" height="107" alt="Pasted image 20250925110522" src="https://github.com/user-attachments/assets/d77cca75-63c1-41a8-884c-ccb916010456" />

Dùng `checksec` để kiểm tra defense mechanism, thấy `Stack Canary` OFF:<br>
<img width="1028" height="315" alt="Pasted image 20250925110629" src="https://github.com/user-attachments/assets/a4442ec7-8aa8-42e7-9bf9-7b9900155c10" />

Pseudo-code từ code đã cho sẵn:<br>

```c
void sigsegv_handler(int sig) {
	printf("%s\n", flag);
	fflush(stdout);
	exit(1);
}

void vuln(char *input){
	char buf2[16];
	strcpy(buf2, input);
}

int main(){
	signal(SIGSEGV, sigsegv_handler); // Set up signal handler
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	
	printf("Input: ");
	fflush(stdout);
	char buf1[100];
	gets(buf1);
	vuln(buf1);
	printf("The program will exit now\n");
	return 0;
}
```

Như vậy mục tiêu sẽ là gây overflow, khi đó `signal()` sẽ gửi tín hiệu tới hệ thống, và hàm `sigsegv_handler()` sẽ được gọi để in ra flag.
Ta chỉ cần nhập chuỗi nhiều hơn 16 ký tự. <br>
<img width="713" height="111" alt="Pasted image 20250925154640" src="https://github.com/user-attachments/assets/03ad46b7-e9df-43fa-a55d-9029616bb993" />



