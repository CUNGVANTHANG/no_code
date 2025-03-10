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