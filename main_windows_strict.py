import os
import sys
import subprocess
import pyperclip
from urllib.parse import urlparse

# === Проверка и установка необходимых пакетов ===
required_packages = ['yt_dlp', 'pyperclip', 'requests', 'beautifulsoup4']
for package in required_packages:
    try:
        __import__(package if package != 'beautifulsoup4' else 'bs4')
    except ImportError:
        print(f"⏳ Устанавливается пакет: {package}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

import yt_dlp
import requests
from bs4 import BeautifulSoup

# === Путь к папке Downloads в текущей директории ===
def get_base_folder():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def get_video_url():
    url = pyperclip.paste().strip()
    if url.startswith('http'):
        print(f"Ссылка взята из буфера: {url}")
        return url
    else:
        try:
            url = input("В буфере нет корректной ссылки. Введите URL:\n").strip()
            if url.startswith('http'):
                return url
            else:
                print("Некорректный URL. Завершаем.")
                sys.exit(1)
        except Exception:
            print("Ошибка при вводе. Завершаем.")
            sys.exit(1)

def download_video(url, folder):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Ошибка при скачивании YouTube-содержимого: {e}")

def download_playlist(url, folder):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'quiet': False,
        'no_warnings': True,
        'yes_playlist': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        print(f"Ошибка при скачивании плейлиста: {e}")

def download_pinterest_image(url, folder):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        img_tag = soup.find('img')
        if img_tag and img_tag.get('src'):
            img_url = img_tag['src']
            print(f"Скачиваем изображение: {img_url}")
            img_data = requests.get(img_url).content
            filename = os.path.join(folder, os.path.basename(img_url.split("?")[0]))
            with open(filename, 'wb') as f:
                f.write(img_data)
            print(f"Изображение сохранено как: {filename}")
        else:
            print("Не удалось найти изображение на странице Pinterest.")
    except Exception as e:
        print(f"Ошибка при скачивании изображения с Pinterest: {e}")

def main():
    base_folder = get_base_folder()
    downloads_folder = os.path.join(base_folder, 'Downloads')
    videos_folder = os.path.join(downloads_folder, 'Videos')
    playlist_folder = os.path.join(videos_folder, 'Playlist Videos')
    pictures_folder = os.path.join(downloads_folder, 'Pictures')

    os.makedirs(videos_folder, exist_ok=True)
    os.makedirs(playlist_folder, exist_ok=True)
    os.makedirs(pictures_folder, exist_ok=True)

    url = get_video_url()
    hostname = urlparse(url).hostname or ""
    hostname = hostname.lower()

    if "youtube.com/playlist" in url:
        print(f"Это плейлист YouTube. Скачиваем всё в: {playlist_folder}")
        download_playlist(url, playlist_folder)

    elif "youtube.com" in hostname or "youtu.be" in hostname:
        print(f"Это видео YouTube. Скачиваем в: {videos_folder}")
        download_video(url, videos_folder)

    elif "pinterest.com" in hostname:
        print(f"Это Pinterest ссылка. Пытаемся скачать...")
        download_pinterest_image(url, pictures_folder)

    else:
        print("Сайт не поддерживается этим скриптом.")

    print("Скачивание завершено!")

    try:
        input("⚠️ Нажмите Enter, чтобы закрыть окно...")
    except:
        pass

if __name__ == '__main__':
    main()
