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
4. The tray menu also lets you open the downloads folder, view `download-list.txt`, open `info.txt`, or change the hotkey.
5. Choose "Выход" in the tray menu to quit.

The script stores settings in `config.json` next to the executable. All files
are always saved to a `Downloads` folder located beside the script. Subfolders
for videos, playlists and pictures are created automatically and this location
cannot be changed.

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

To automate these steps you can use `build_exe.py`:

```bash
python build_exe.py
```

The script checks packages and then runs PyInstaller with the correct
options. When the build finishes you will be prompted to press any key
to close the console.

Error messages are written to `script.log` in the script folder.

