# PythonCenteringWindows

A python "tiling" script for non tiling WMs for X11

## Install

Install required modules with:

```bash
pip install -r requirements.txt
```

Run autoinstall:

```bash
python autoinstall.py
```

## Usage

You can run this script with the following arguments:

```
python main.py --help

usage: main.py [-h] -m {center,tile_left,tile_right,tile_leftcenter,tile_rightcenter,tile_leftleft,tile_rightright} [--noresize]

My awesome python tiling assistant !

options:
  -h, --help            show this help message and exit
  -m, --mode {
      center,
      tile_left,
      tile_right,
      tile_leftcenter,
      tile_rightcenter,
      tile_leftleft,
      tile_rightright
      }                 Choose how to tile the active window
  --noresize            Center window without resize it

```

### Examples

If you want to put the active window on the left part of the screen, run:

```bash
python main.py -m tile_left
# pytiling -m tile_left if you used the autoinstall script !!
```

## Known Issiues

This is kind a big mess, it looks like the correct alignment depends on multiple things: the terminal you are using, your WM, your theme, ecc.

I tesed this script on a Debian 11 VM with:

- Gnome
- MATE
- Plasma
- Xfce4

And on ArchLinux Xfce4 with Chicago95 theme.

The following are the thing I know:

### On Gnome

_Problems:_

- With the deafult terminal left and right alignment doesn't work correctly (shifted from the screen borders and wrong width)

_Success:_

- Centering works with everything
- Everything seems to work with Konsole

### On MATE

_Problems:_

- With MATE Terminal there are some space between windows but it looks like a feature !!

_Success:_

- With Konsole everything works

### On Plasma

_Problems:_

_Success:_

- With Konsole everything works.
- With MATE Terminal everything works but with some space between windows (its a feature !)

### On Xfce

_Problems:_

- Sometime left/right tiling fail

_Success:_

- Everything works (more or less ...)
