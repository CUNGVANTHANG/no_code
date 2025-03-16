## Cách tải file pdf trên google drive bị chặn tải xuống

Đầu tiên chúng ta cần tải load hiển thị hết các trang trong file pdf đó. Hãy kéo tới cuối trang pdf

![Screenshot 2025-03-16 225119](https://github.com/user-attachments/assets/4c1ae3dc-bcc6-4ca2-8e59-4366fdcdacd3)

Sau đó ta mở console của trình duyệt rồi paste đoạn mã này vào. Nếu không dán được hãy gõ lệnh để paste vào

```
allow pasting
```

Đoạn mã đầu tiên dùng trong trường hợp trình duyệt cấm

```js
const policy = trustedTypes.createPolicy("default", {
    createScriptURL: (url) => url
});

let jspdf = document.createElement("script");

jspdf.onload = function () {
    let pdf = new jsPDF();
    let elements = document.getElementsByTagName("img");

    for (let i in elements) {
        let img = elements[i];
        if (!/^blob:/.test(img.src)) {
            continue;
        }

        let can = document.createElement('canvas');
        let con = can.getContext('2d');
        can.width = img.width;
        can.height = img.height;
        con.drawImage(img, 0, 0);

        let imgData = can.toDataURL("image/jpeg", 1.0);
        pdf.addImage(imgData, 'JPEG', 0, 0);
        pdf.addPage();
    }

    pdf.save(document.title.split('.pdf - ')[0] + ".pdf");
};

jspdf.src = policy.createScriptURL('https://gdrive.vip/wp-content/uploads/2020/jspdf.debug.js');

document.body.appendChild(jspdf);
```

hoặc đoạn mã tiếp theo trình duyệt đã bỏ chức năng cấm rồi

```js
let jspdf = document.createElement("script");

jspdf.onload = function () {

    let pdf = new jsPDF();
    let elements = document.getElementsByTagName("img");
    for (let i in elements) {
        let img = elements[i];
        if (!/^blob:/.test(img.src)) {
            continue;
        }
        let can = document.createElement('canvas');
        let con = can.getContext('2d');
        can.width = img.width;
        can.height = img.height;
        con.drawImage(img, 0, 0);
        let imgData = can.toDataURL("image/jpeg", 1.0);
        pdf.addImage(imgData, 'JPEG', 0, 0);
        pdf.addPage();
    }

    pdf.save(document.title.split('.pdf - ')[0]+".pdf");
};

jspdf.src = 'https://gdrive.vip/wp-content/uploads/2020/jspdf.debug.js';
document.body.appendChild(jspdf);
```

![Screenshot 2025-03-16 224050](https://github.com/user-attachments/assets/40f6b0a9-b34f-459b-8e63-583e2e64956e)

