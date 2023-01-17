This code is used to backup virtual machines (VMs) from a source directory to a destination directory.

## Requirements

- Python 3

## Instructions

1. Ensure that the source directory (`SOURCE`) and destination directory (`DESTINATION`) exist.
2. Run the code with `python3 <filename>`.
3. The code will search the source directory for any folders ending in `.pvm` and create a `.tar.gz` archive of each one.
4. The archives will be copied to the destination directory.
5. If an archive with the same name already exists in the destination directory, the existing one will be renamed with a `~` at the end of the file name.
