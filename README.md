# PythonCenteringWindows
A python script able to center windows based on Xorg Server

## Install

Install required modules with:

```bash
pip install -r requirements.txt
```

## Usage

You can run this script with:

```bash
python main.py [args]
```

Without no arguments this script center and resize the window.<br>
With `--noresize` argument this script centere the window and keeps his size.

**WARNING:** This script is tested only with XFCE4 and it works for now !

## Xfce4 configuration

You can set a keyboard shortcut for this script like this:

1. Open Settings Manager
2. Select Keyboard
3. Under Application Shortcut use the add button to add a new shortcut
4. Add `python path/of/dir` (or `python path/to/dir --noresize`)
5. Choose a shortcut: SUPER + K
6. DONE

