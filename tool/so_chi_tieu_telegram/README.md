# Sổ chi tiêu Telegram

BotFather trên Telegram là một bot chính thức do Telegram cung cấp, dùng để tạo, quản lý và cấu hình các chatbot trên nền tảng Telegram.

<image src="https://github.com/user-attachments/assets/6c96cd8d-ac02-4a5e-a5ad-64fc2b127d36" width="600px" >

Bước 1: Đặt tên cho bot

<image src="https://github.com/user-attachments/assets/9d8b1e8a-0fb9-4686-9aae-bd56f9fe0560" width="600px" >

Bước 2: Đặt id (Chú ý cần có từ `bot` ở cuối id)

<image src="https://github.com/user-attachments/assets/31cc4423-734c-4225-8aae-992d2be5d4fe" width="600px" >

Token ở đâu là `7845056102:AAGZyE4x_jTcEbhoJuQVy40TPYpE81YRC94`

```gs
const TOKEN = `7845056102:AAGZyE4x_jTcEbhoJuQVy40TPYpE81YRC94`;
```

Bước 3: Tạo sheet

<image src="https://github.com/user-attachments/assets/0073d9b0-2c7f-4481-a11a-c0fa93e1394f" width="600px" >

vào Extensions chọn App Script

<image src="https://github.com/user-attachments/assets/424f06d3-42b9-4e19-8bc8-357fbe1f4e0e" width="600px" >

Bước 4: Copy paste đoạn mã `.gs`

<image src="https://github.com/user-attachments/assets/fed49e41-1a13-44e5-b2ab-32492c46f9b3" width="600px" >

Chúng ta sẽ thêm TOKEN vào đoạn mã

```gs
const TOKEN = `7845056102:AAGZyE4x_jTcEbhoJuQVy40TPYpE81YRC94`;
```

Bước 5: Lấy id chatbot của ta bằng cách bấm vào 

<image src="https://github.com/user-attachments/assets/4ffd8556-1573-46fb-af5a-04ffd2d3082b" width="600px" >

Xong bấm bắt đầu chat

<image src="https://github.com/user-attachments/assets/a6a19639-9192-43b5-8c9e-ee6d1a998345" width="600px" >

Quay lại App Script chúng ta chọn chạy function `getChatId` để lấy id

<image src="https://github.com/user-attachments/assets/d81e2e1f-909c-4da6-bb73-9e7b9b19d628" width="600px" >

Xong đó nhớ cấp quyền thực thi 

<image src="https://github.com/user-attachments/assets/db015ed7-d711-45f4-8f38-b770641a6ebc" width="600px" >

Nếu chưa hiển thị id thì chúng ta vào lại Telegram chat 1 câu bất kỳ và chạy lại App Script

<image src="https://github.com/user-attachments/assets/8ed7d676-f256-4662-ac94-7b91868a46f6" width="600px" >

Rồi lấy id thêm vào đoạn mã

```gs
const CHAT_ID = '8191743207';
```

Xong đó Deploy bằng Web app

<image src="https://github.com/user-attachments/assets/95675636-b152-4c45-b1d0-706a772d2c15" width="600px" >

Xong copy URL

<image src="https://github.com/user-attachments/assets/9fb09569-3a2b-4f3b-8553-d7d23f495dc7" width="600px" >

Xong đó paste vào

```gs
const DEPLOYED_URL = 'https://script.google.com/macros/s/AKfycbwMTa-c1aQcDQ4vW2HbU-Vr21X-ydlieCgs9HpWIduHZYkDHIFjtp80k9lU-spPu1lb/exec';
```

<image src="https://github.com/user-attachments/assets/d89db829-2da3-4678-8266-db39fbccf693" width="600px" >

Xong đó chọn `setWebhook` rồi run

Bây giờ chúng ta có thể chat

<image src="https://github.com/user-attachments/assets/b7e15db5-7634-4d9d-8fd7-893e67b80a42" width="600px" >

và kết quả

<image src="https://github.com/user-attachments/assets/96fecfd4-f472-4267-a462-dcd78a1fe104" width="600px" >

