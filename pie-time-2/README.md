# PIE TIME 2
Challenge cung cấp file binary và mã nguồn. Đầu tiên tôi kiểm tra file cơ bản file binary: <br>
![alt text](image.png)
<br>
Khi chạy, chương trình yêu cầu nhập tên, sau đó địa chỉ để nhảy tới địa chỉ đó<br>
![alt text](image-1.png)
<br>
Kiểm tra thử mã nguồn xem có gì đặc biệt. <br>
![alt text](image-2.png)
<br>
Khi printf() chương trình không có format string. Ta có thể tận dụng lỗi này.<br>
Như vậy, quy trình sẽ là:<br>
- Dùng lỗi **format-string** để leak các địa chỉ hàm `main()` hoặc `call_functions()`
- Từ địa chỉ leak ra, tính offset tới hàm `win()`
- Truy cập vào hàm `win()`
<br>
Tôi dùng **gdb** để debug chương trình. Cần lưu ý là khi debug bằng gdb, PIE và ASLR sẽ được tắt để tiện debug hơn. Như vậy cũng giúp ta tính offset dễ hơn.<br>
![alt text](image-3.png)
<br>
Áp dụng payload: `%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p,%p`
<br>
Ta được các địa chỉ sau:
![alt text](image-4.png)
<br>
Chú ý ô được tô đỏ, địa chỉ này rất gần xuất hiện trong hàm main, cụ thể đó là `<main+65>`<br>
![alt text](image-5.png)
<br>
Từ đây ta tính offset từ <main+65> tới win.
<br>
![alt text](image-6.png)
<br>
![alt text](image-7.png)
<br>

Như vậy, để truy cập vào win, ta chỉ cần leak ra địa chỉ <main+65> sau đó trừ đi offset. Giờ tôi kết nối tới server.
<br>
![alt text](image-8.png)