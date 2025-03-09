import os
import requests
from bs4 import BeautifulSoup
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog, messagebox, Radiobutton


def create_session():
    """
    Tạo một session HTTP với cơ chế retry.
    """
    session = requests.Session()
    retries = requests.adapters.Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount("https://", requests.adapters.HTTPAdapter(max_retries=retries))
    return session


def get_audio_url(word, accent):
    """
    Tìm liên kết đến tệp MP3 phát âm từ Cambridge Dictionary.
    :param word: Từ cần tìm phát âm.
    :param accent: Giọng đọc ('us' hoặc 'uk').
    :return: URL tệp MP3.
    """
    url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        messagebox.showerror("Lỗi", f"Không thể truy cập Cambridge Dictionary. Mã lỗi: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    try:
        if accent == "us":
            audio_tag = soup.find("span", {"class": "us dpron-i"}).find("source", {"type": "audio/mpeg"})
        elif accent == "uk":
            audio_tag = soup.find("span", {"class": "uk dpron-i"}).find("source", {"type": "audio/mpeg"})
        else:
            raise ValueError("Accent không hợp lệ.")
        return "https://dictionary.cambridge.org" + audio_tag["src"]
    except AttributeError:
        messagebox.showerror("Lỗi", f"Không tìm thấy phát âm cho từ '{word}' và giọng đọc '{accent.upper()}'.")
        return None


def download_audio(url, word, accent, save_path):
    """
    Tải tệp MP3 từ liên kết và lưu vào máy.
    :param url: URL tệp MP3.
    :param word: Từ cần tải phát âm.
    :param accent: Giọng đọc ('us' hoặc 'uk').
    :param save_path: Thư mục lưu tệp.
    """
    session = create_session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = session.get(url, headers=headers, stream=True, timeout=10)
        if response.status_code == 200:
            filename = os.path.join(save_path, f"{word}_{accent}.mp3")
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            messagebox.showinfo("Thành công", f"Tệp đã được lưu tại: {filename}")
        else:
            messagebox.showerror("Lỗi", f"Không thể tải tệp MP3. Mã lỗi: {response.status_code}")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tải tệp: {e}")


def select_folder():
    """
    Mở hộp thoại để chọn thư mục lưu tệp.
    """
    folder_selected = filedialog.askdirectory()
    save_path_var.set(folder_selected)


def start_download():
    """
    Bắt đầu quá trình tải tệp MP3.
    """
    word = word_var.get().strip()
    accent = accent_var.get()
    save_path = save_path_var.get()

    if not word:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ cần tải.")
        return

    if not save_path:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn thư mục lưu tệp.")
        return

    audio_url = get_audio_url(word, accent)
    if audio_url:
        download_audio(audio_url, word, accent, save_path)


# Tạo cửa sổ GUI
root = Tk()
root.title("Tải Phát Âm Cambridge Dictionary")

# Biến lưu trữ
word_var = StringVar()
accent_var = StringVar(value="us")
save_path_var = StringVar()

# Giao diện người dùng
Label(root, text="Nhập từ cần tải phát âm:").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=word_var, width=30).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Chọn giọng đọc:").grid(row=1, column=0, padx=10, pady=5)
Radiobutton(root, text="US", variable=accent_var, value="us").grid(row=1, column=1, sticky="w")
Radiobutton(root, text="UK", variable=accent_var, value="uk").grid(row=1, column=1, sticky="e")

Label(root, text="Thư mục lưu tệp:").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=save_path_var, width=30).grid(row=2, column=1, padx=10, pady=5)
Button(root, text="Chọn...", command=select_folder).grid(row=2, column=2, padx=10, pady=5)

Button(root, text="Tải về", command=start_download).grid(row=3, column=0, columnspan=3, pady=10)

# Chạy ứng dụng
root.mainloop()
