import os
import sys
import atexit
import time
from urllib.parse import urlparse

import yt_dlp
import requests
from bs4 import BeautifulSoup
import keyboard
import pystray
import pyperclip

from PIL import Image


def get_base_folder() -> str:
    """Returns the folder where persistent files should be stored."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def resource_path(name: str) -> str:
    """Resolve resource path for bundled executables."""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, name)  # type: ignore[attr-defined]
    return os.path.join(get_base_folder(), name)


# === Пути и файлы ===
BASE_FOLDER = get_base_folder()
DOWNLOADS_FOLDER = os.path.join(BASE_FOLDER, 'Downloads')
VIDEOS_FOLDER = os.path.join(DOWNLOADS_FOLDER, 'Videos')
PLAYLIST_FOLDER = os.path.join(VIDEOS_FOLDER, 'Playlist Videos')
PICTURES_FOLDER = os.path.join(DOWNLOADS_FOLDER, 'Pictures')
DOWNLOAD_LIST = os.path.join(BASE_FOLDER, 'download-list.txt')

os.makedirs(VIDEOS_FOLDER, exist_ok=True)
os.makedirs(PLAYLIST_FOLDER, exist_ok=True)
os.makedirs(PICTURES_FOLDER, exist_ok=True)


def ensure_single_instance() -> None:
    """Предотвращает запуск нескольких экземпляров скрипта."""
    if sys.platform.startswith('win'):
        import msvcrt
        lock_path = os.path.join(BASE_FOLDER, 'script.lock')
        lock_file = open(lock_path, 'w')
        try:
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        except OSError:
            print('Скрипт уже запущен.')
            sys.exit(0)

        def release_lock() -> None:
            try:
                msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                lock_file.close()
                os.remove(lock_path)
            except Exception:
                pass

        atexit.register(release_lock)


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


def handle_url(url: str) -> None:
    """Определяет тип ссылки и запускает скачивание."""
    hostname = urlparse(url).hostname or ""
    hostname = hostname.lower()

    if "youtube.com/playlist" in url:
        print(f"Это плейлист YouTube. Скачиваем всё в: {PLAYLIST_FOLDER}")
        download_playlist(url, PLAYLIST_FOLDER)

    elif "youtube.com" in hostname or "youtu.be" in hostname:
        print(f"Это видео YouTube. Скачиваем в: {VIDEOS_FOLDER}")
        download_video(url, VIDEOS_FOLDER)

    elif "pinterest.com" in hostname:
        print("Это Pinterest ссылка. Пытаемся скачать...")
        download_pinterest_image(url, PICTURES_FOLDER)

    else:
        print("Сайт не поддерживается этим скриптом.")


def download_all() -> None:
    """Скачивает все ссылки из файла download-list.txt."""
    if not os.path.exists(DOWNLOAD_LIST):
        print("Файл download-list.txt не найден.")
        return

    with open(DOWNLOAD_LIST, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    if not urls:
        print("Список ссылок пуст.")
        return

    for url in urls:
        handle_url(url)

    open(DOWNLOAD_LIST, 'w', encoding='utf-8').close()
    print("Скачивание завершено!")


def add_link_from_clipboard() -> None:
    """Копирует выделенный текст и сохраняет как ссылку."""
    keyboard.press_and_release('ctrl+c')
    time.sleep(0.1)
    url = pyperclip.paste().strip()
    if not url:
        print("Буфер обмена пуст.")
        return

    with open(DOWNLOAD_LIST, 'a', encoding='utf-8') as f:
        f.write(url + '\n')
    print(f"Добавлено в список: {url}")

def main() -> None:
    """Запускает горячие клавиши и значок в трее."""

    ensure_single_instance()

    def on_download(icon, item):
        download_all()

    def on_exit(icon, item):
        icon.stop()

    icon_path = resource_path('ico.ico')
    image = Image.open(icon_path) if os.path.exists(icon_path) else None
    menu = pystray.Menu(
        pystray.MenuItem('Скачать', on_download),
        pystray.MenuItem('Выход', on_exit),
    )
    tray_icon = pystray.Icon('YTDownloader', image, 'YT Downloader', menu)

    keyboard.add_hotkey('ctrl+b', add_link_from_clipboard)
    keyboard.add_hotkey('ctrl+shift+b', download_all)

    print('Значок размещён в трее. Горячие клавиши Ctrl+B и Ctrl+Shift+B активны.')

    tray_icon.run()

    keyboard.unhook_all_hotkeys()

    print('Скрипт завершён.')

if __name__ == '__main__':
    main()

