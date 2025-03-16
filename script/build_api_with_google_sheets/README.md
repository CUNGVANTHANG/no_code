# Xây dựng API bằng google sheets giúp test API nhanh trên front end

Tạo data trên google sheet, xong đó vào App Script

![image](https://github.com/user-attachments/assets/d6055901-594d-4a63-9621-46639aef7ff3)

Paste đoạn mã nãy vào 

```gs
const toJson = (values = []) => {
    if (!values || values.length <= 1) return [];
    const [keys, ...data] = values;
    const result = data.map(
        (row) => {
            const object = {};
            keys.forEach((key, index) => object[key] = row[index]);
            return object;
        }
    );
    return JSON.stringify(result);
}

const doGet = () => {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const json = toJson(sheet.getDataRange().getValues());
    return ContentService.createTextOutput(json).setMimeType(ContentService.MimeType.JSON);
}
```

![image](https://github.com/user-attachments/assets/d36a0625-b67e-4f0f-a500-e31cd59214fa)

Xong đó deploy dưới dạng ứng dụng web để lấy URL như sau

```
https://script.google.com/macros/s/AKfycbxLFFluZPA3W1ByZGyOrGC-_dEX38eO5ZLJarfmcBl7Lz8wO1CvgHW3L_tytdHaf9iR/exec
```

Vào postman kiểm tra và đây là kết quà

![image](https://github.com/user-attachments/assets/51949776-ae77-4b87-b410-5964758f9863)

