# PRIMARY_Backup_v2

Program to automate backup sorting and moving of files.

## Program Features:
- [x] Pre-Sort files and folders
- [x] Copy the files over to new folder if they DO NOT exist
- [x] Copy Metadata between two drives 
- [x] (Mac Only) Copy color tag labels[Using TAG]
- [x] Verify data has been written correctly to new location
- [ ] Compare files and if we have an updated version, Delete old file and replace with new one


## Dependencies

- PYTHON3: Runs the script, not included in all OS
- XCODE Command Line Tools: (To Install TAG)
- TAG: Used when running on OSX to copy color tags

## Installation

XCODE Command Line Utilities and TAG needed for color tag copying

Install Command Line tools from Terminal on Mac:

```

$ xcode-select --install

```

Install TAG:
Install via included package or Download from https://github.com/jdberry/tag or 

## Usage

Mac/Linux

Run __PRIMARY_Backup_v2.py__ script and use GUI interface to select FROM and TO folder.

Program will take all the folders and files in the FROM directory
Check it's index(ex. A,B,D) and place in TO folder inside an indexed folder(ex. A-Clients,B-Clients,D-Clients)

python3 & location_of_script


```

$ python3 /Users/YouUserName/PRIMARY_Backup_v2/PRIMARY_Backup_v2.py

```

Windows 

TODO: Finish writing instructions for Windows users.

```

$ python3 

```
 
