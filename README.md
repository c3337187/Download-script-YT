# Download-script-YT

Utility to queue links from the clipboard and download them with yt-dlp.

Before using the script make sure all required packages are installed. Run:

```bash
python check_packages.py
```

Or install them manually:

```bash
pip install yt_dlp pyperclip requests beautifulsoup4 pystray keyboard pillow pywin32
```

Install `pywin32` only on Windows.

1. Run `python main_windows_strict.py` on Windows.
2. A tray icon will appear. Use **Ctrl+B** (or your configured hotkey) to add the selected link to `download-list.txt`.
3. Use **Ctrl+Shift+B** or the "Скачать" tray menu item to download all queued links.
4. The tray menu also lets you open the downloads folder, view `download-list.txt`, change the hotkey, or select another downloads path.
5. Choose "Выход" in the tray menu to quit.

The script stores settings in `config.json` next to the executable. By default
files are saved to a `Downloads` folder in the same location. Use the tray menu
item "Изменить папку загрузки" to select a different directory. Subfolders for
videos, playlists and pictures will be created automatically.

### Building an executable

Use PyInstaller to bundle the script. Include the tray icon file and the
pystray Windows backend:

```bash
pyinstaller --onefile --windowed --icon=ico.ico \
    --add-data "ico.ico;." --hidden-import pystray._win32 \
    main_windows_strict.py
```

Ensure all dependencies are installed **before** building. Either run
`python check_packages.py` or install them manually as shown above.

Error messages are written to `script.log` in the script folder.

