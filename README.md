# Satella Unlocked

Created by **Ｄｉａ！♪～☆**.

**Satella Unlocked** removes expired launch counters from compatible **BS-X Satellaview ROM images**, letting you play No Intro BS-X ROMs with a real BSX Cartridge and Memory pack, or also games that have broken timers (eg they had soundlink or in game timers and the launch period has expired) that were dumped from a real BS-X cartridge.

## Features

- Detects recognised BS-X headers at standard LoROM and HiROM locations.
- Supports ROMs with or without a 512-byte copier header (no intro ROMs).
- Changes the expired launch-counter value `0x8000` to `0x0000` (unlimited starts).
- Names output files **`UNLOCKED - [original filename]`**.
- Accepts individual files or a folder of `.bs`, `.sfc`, `.smc`, or `.bin` files.

## Download and requirements

- **Python 3** is required to run from source.
- **Tkinter** is required for the graphical interface (usually bundled with Python on Windows).
- The included Windows `.bat` launcher runs the Python script; it is not a compiled executable.
- Or just download the precompiled version in the Releases tab

Keep `Satella-Unlocked.py` and `Satella-Unlocked.bat` in the same directory.

## Usage

### Windows graphical interface

Double-click `Satella-Unlocked.bat` and choose **Select ROM(s)** or **Select Folder**.

You can also drag ROM files onto `Satella-Unlocked.bat` to process them directly.

### Command line

```bash
python Satella-Unlocked.py "game.bs"
```

Process a folder:

```bash
python Satella-Unlocked.py "C:\path\to\roms"
```

Inspect without writing:

```bash
python Satella-Unlocked.py --dry-run "game.bs"
```

### Output

Input:

```text
ROM.bs
```

Output:

```text
UNLOCKED - ROM.bs
```

The patched copy is placed beside the original. An existing output file is never overwritten.

## Tested

The following ROMs have been tested:

**BS Fire Emblem: Archanea Saga : パレス陥落**
**BS Fire Emblem: Archanea Saga : 赤い竜騎士**
**BS Fire Emblem: Archanea Saga : 正義の盗賊団**
**BS Fire Emblem: Archanea Saga : 始まりのとき**
**BS Legend of Zelda**

if anything else works just send a PR.

## Limitations

- It literally changes one byte. If your ROM still does not boot then the expired timer is not the issue.

## Building a Windows executable

If you have `Build-Standalone.bat`, run it on a Windows PC with Python 3 installed. It installs PyInstaller if required and builds `dist/Satella-Unlocked.exe`. The resulting executable should run without Python installed on the target PC.

## Credits and references

See [CREDITS.md](CREDITS.md) for project attribution, technical references, and acknowledgements.

## Disclaimer

Satella Unlocked is an independent preservation/homebrew utility, not affiliated with or endorsed by Nintendo, St.GIGA, Intelligent Systems, or other rights holders. No commercial game ROMs or BIOS files are included. Use it only with files you are authorised to use.
