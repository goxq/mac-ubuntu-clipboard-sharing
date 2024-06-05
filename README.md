This is a Python tool to synchronize the clipboard between macOS and Ubuntu systems in a local network.

Support both text and image.

## How to Use

1. Clone this repo
2. put `clipboard_mac_client.py`, `clipboard_mac_server.py` on Mac and `clipboard_ubun_client.py`, `clipboard_ubun_server.py` on Ubuntu.
3. Change the `ip` and `port` in all the files dependent on your machines.
4. Install the requirements below and run all the python scripts on Mac and Ubuntu.

## Requirements

Python 3.10 or higher

### On Mac

pip requirements:

- Flask
- requests
- pyobjc

and `brew install pcopy`

### On Ubuntu

pip requirements:

- Flask
- requests
- Pillow
- pygobject

and 

```bash
sudo apt update
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0
```

