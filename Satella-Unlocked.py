#!/usr/bin/env python3
"""Satella Unlocked — BS-X ROM launch-counter patcher by Ｄｉａ！♪～☆."""

import argparse
from pathlib import Path
import sys

EXTENSIONS = {'.bs', '.sfc', '.smc', '.bin'}
HEADER_BASES = (0x7FB0, 0xFFB0)


def find_headers(data):
    copier = 512 if len(data) % 0x8000 == 512 else 0
    found = []
    for base in HEADER_BASES:
        pos = base + copier
        if pos + 0x30 > len(data):
            continue
        head = data[pos:pos + 0x30]
        # Satellaview's identifying fixed byte and a complementary checksum.
        if head[0x2A] != 0x33:
            continue
        check = int.from_bytes(head[0x2E:0x30], 'little')
        inverse = int.from_bytes(head[0x2C:0x2E], 'little')
        if check + inverse != 0xFFFF:
            continue
        count = int.from_bytes(head[0x24:0x26], 'little')
        found.append((pos, count, check))
    return found


def patch_file(path, dry_run=False):
    original = path.read_bytes()
    data = bytearray(original)
    headers = find_headers(data)
    if not headers:
        return f'SKIP {path.name}: no recognised BS-X header'
    expired = [(pos, count) for pos, count, _ in headers if count == 0x8000]
    if not expired:
        return f'OK   {path.name}: no expired 0x8000 counter detected'
    for pos, _ in expired:
        data[pos + 0x24:pos + 0x26] = b'\x00\x00'
    if dry_run:
        return f'FOUND {path.name}: {len(expired)} expired header(s)'
    output = path.with_name('UNLOCKED - ' + path.name)
    if output.exists():
        return f'SKIP {path.name}: output already exists ({output.name})'
    output.write_bytes(data)
    assert output.read_bytes() == bytes(data)
    assert len(original) == output.stat().st_size
    return f'SAVED {output.name}: {len(expired)} counter(s) unlocked; original preserved'


def process(paths, dry_run=False):
    for item in paths:
        if item.is_dir():
            candidates = sorted(p for p in item.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS and not p.name.startswith('UNLOCKED - '))
        elif item.is_file():
            candidates = [item]
        else:
            print(f'ERROR {item}: not found')
            continue
        for path in candidates:
            try:
                print(patch_file(path, dry_run))
            except (OSError, ValueError) as error:
                print(f'ERROR {path.name}: {error}')


def gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox
    root = tk.Tk()
    root.title('Satella-Unlocked')
    root.geometry('580x350')
    tk.Label(root, text='Satella Unlocked', font=('Arial', 16, 'bold')).pack(pady=(22, 8))
    tk.Label(root, text='Unlocks expired 0x8000 launch counters. Originals are never overwritten.').pack()
    log = tk.Text(root, height=10, wrap='word')
    log.pack(fill='both', expand=True, padx=16, pady=15)

    def run(items):
        for path in items:
            try:
                log.insert('end', patch_file(Path(path)) + '\n')
            except (OSError, ValueError) as error:
                log.insert('end', f'ERROR {path}: {error}\n')
        log.see('end')

    buttons = tk.Frame(root)
    buttons.pack(pady=(0, 14))
    tk.Button(buttons, text='Select ROM(s)', width=18, command=lambda: run(filedialog.askopenfilenames(filetypes=[('SNES ROMs', '*.bs *.sfc *.smc *.bin'), ('All files', '*.*')]))).pack(side='left', padx=6)

    def choose_folder():
        folder = filedialog.askdirectory()
        if folder:
            files = sorted(p for p in Path(folder).iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS and not p.name.startswith('UNLOCKED - '))
            run(files)

    tk.Button(buttons, text='Select Folder', width=18, command=choose_folder).pack(side='left', padx=6)
    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description='Unlock expired launch counters in BS-X Satellaview ROMs.')
    parser.add_argument('paths', nargs='*', type=Path, help='ROM files or folders (GUI if omitted)')
    parser.add_argument('--dry-run', action='store_true', help='Inspect without writing')
    args = parser.parse_args()
    if args.paths:
        process(args.paths, args.dry_run)
    else:
        try:
            gui()
        except (ImportError, RuntimeError) as error:
            parser.error(f'GUI unavailable ({error}); supply ROM paths for CLI mode')


if __name__ == '__main__':
    main()
