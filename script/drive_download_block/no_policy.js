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