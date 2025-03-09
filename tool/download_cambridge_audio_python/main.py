import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os

def create_session():
    """Tạo một session HTTP với cơ chế retry."""
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount("https://", HTTPAdapter(max_retries=retries))
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
        print(f"Không thể truy cập từ điển Cambridge. Mã lỗi: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    """
    Tìm theo class 'us dpron-i' hoặc 'uk dpron-i'
    """
    # Tìm thẻ audio MP3 theo accent
    if accent == "us":
        audio_tag = soup.find("span", {"class": "us dpron-i"}).find("source", {"type": "audio/mpeg"})
    elif accent == "uk":
        audio_tag = soup.find("span", {"class": "uk dpron-i"}).find("source", {"type": "audio/mpeg"})
    else:
        print("Accent không hợp lệ. Chỉ chấp nhận 'us' hoặc 'uk'.")
        return None

    if audio_tag and "src" in audio_tag.attrs:
        return "https://dictionary.cambridge.org" + audio_tag["src"]
    else:
        print(f"Không tìm thấy phát âm cho {accent.upper()}.")
        return None

def download_audio(url, word, accent):
    """
    Tải tệp MP3 từ liên kết và lưu vào máy.
    :param url: URL tệp MP3.
    :param word: Từ cần tải phát âm.
    :param accent: Giọng đọc ('us' hoặc 'uk').
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    session = create_session()
    try:
        response = session.get(url, headers=headers, stream=True, timeout=10)
        if response.status_code == 200:
            """
            Đường dẫn hiện tại
            """
            save_path = "/home/lts/Downloads"
            filename = os.path.join(save_path, f"{word}_{accent}.mp3")
            # filename = f"{word}_{accent}.mp3"
            with open(filename, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Tải thành công: {filename}")
        else:
            print(f"Không thể tải tệp MP3. Mã lỗi: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi tải tệp: {e}")

def main():
    """
    Chương trình chính để tải phát âm từ Cambridge Dictionary.
    """
    print("Công cụ tải phát âm từ Cambridge Dictionary")
    word = input("Nhập từ cần tải phát âm: ").strip()
    """
    Tùy chọn hoặc để mặc định là 'us'
    """
    # accent = input("Chọn giọng đọc (uk/us): ").strip().lower()
    accent = "us"

    if not word or accent not in ["uk", "us"]:
        print("Vui lòng nhập từ và chọn giọng đọc hợp lệ ('uk' hoặc 'us').")
        return

    audio_url = get_audio_url(word, accent)
    if audio_url:
        print(f"Đang tải tệp MP3 từ: {audio_url}")
        download_audio(audio_url, word, accent)

if __name__ == "__main__":
    main()