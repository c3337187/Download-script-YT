# Download-script-YT

Utility to queue links from the clipboard and download them with yt-dlp.

1. Run `python main_windows_strict.py` on Windows.
2. A tray icon will appear. Use **Ctrl+B** to add the selected link to `download-list`.
3. Use **Ctrl+Shift+B** or the "Скачать" tray menu item to download all queued links.
4. Choose "Выход" in the tray menu to quit.

### Building an executable

Use PyInstaller to bundle the script. Include the tray icon file:

```bash
pyinstaller --onefile --windowed --icon=ico.ico --add-data "ico.ico;." main_windows_strict.py
```

Ensure all dependencies are installed **before** building:

```bash
pip install yt_dlp pyperclip requests beautifulsoup4 pystray keyboard pillow pywin32
```

Install `pywin32` only on Windows so the tray icon works correctly.

