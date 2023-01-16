#!/usr/bin/env python3

import os
import shutil
import subprocess

SOURCE = "/Users/me/Parallels"
DESTINATION = "/Volumes/me/vms"

if not os.path.isdir(SOURCE):
    print(f"{SOURCE} doesn't exist")
    exit(1)

if not os.path.isdir(DESTINATION):
    print(f"{DESTINATION} doesn't exist")
    exit(1)

find_output = subprocess.run(
    ["find", SOURCE, "-type", "d", "-name", "*.pvm", "-print0"],
    capture_output=True,
    text=True,
)

if find_output.returncode != 0:
    print(find_output.stderr)
    exit(1)

for file in find_output.stdout.split("\0"):
    vm = os.path.basename(file)
    vm_archive = vm + ".tar.gz"
    vm_archive_path = os.path.join(SOURCE, vm_archive)
    print(f"VM: {vm}")

    print("(re)create local archive")
    try:
        os.unlink(vm_archive_path)
    except OSError:
        pass

    subprocess.run(
        ["tar", "-czf", vm_archive_path, "-C", file, "."],
        check=True,
        cwd=file,
    )

    backup_path = os.path.join(DESTINATION, vm_archive)
    if os.path.exists(backup_path):
        print(f"Rename existing backup")
        shutil.move(backup_path, backup_path + "~")

    print(f"Copy backup file to destination")
    shutil.copy(vm_archive_path, DESTINATION
