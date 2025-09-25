
![[Pasted image 20250925154725.png]]


Chương trình nhập vào một chuỗi, sau đó kết thúc.

![[Pasted image 20250925095851.png]]

Dùng `file` để kiểm tra, phát hiện đây là ELF 32-bit, little endian:
![[Pasted image 20250925110522.png]]

Dùng `checksec` để kiểm tra defense mechanism, thấy `Stack Canary` OFF:
![[Pasted image 20250925110629.png]]

Pseudo-code từ code đã cho sẵn:

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
Ta chỉ cần nhập chuỗi nhiều hơn 16 ký tự.
![[Pasted image 20250925154640.png]]


