#!/usr/bin/env python3

import argparse
from contextlib import contextmanager
from typing import Any, Dict, Optional, Tuple, Union, Callable  # noqa

import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

# display/monitor/screens
d = Gdk.Display.get_default().get_primary_monitor()
ss = Gdk.get_default_root_window()
s = Gdk.get_default_root_window().get_screen()

# dims
wa = d.get_workarea()
w = wa.width
h = wa.height

def main():
    # get active window
    window = Gdk.get_default_root_window().get_screen().get_active_window()

    # execute user selected tiling operation
    options[args.mode](window)



    w.move(int(wid / 2), 0)

    w.move(0, 0)

    w.resize(int(wid / 2), hei)

    Gdk.flush()


"""
Align left and right 





print(w)
print(s)
print(ss.get_width(), ss.get_height())


#wid = ss.get_width()
#hei = ss.get_height()

print(wid, hei)

tt = 1

w.set_decorations(0) #use 1 to turn on decorations

if tt:
	w.move(int(wid/2),0)
else:
	w.move(0,0)

w.resize(int(wid/2), hei)

Gdk.flush()

#w.set_decorations(Gdk.WMDecoration.ALL) #use 1 to turn on decorations
#Gdk.flush()

"""

def __edit_window(window, x=None, y=None, w=None, h=None, nodecorators=True):
    window.set_decorations(0)  # disable window decorators

    if x is not None and y is not None:
        window.move(x, y)

    if w is not None and h is not None:
        window.resize(w, h)

    Gdk.flush()     # apply mods

    # redraw decorators
    if not nodecorators :
        window.set_decorations(Gdk.WMDecoration.ALL)
        Gdk.flush()


def tile_left(window):
    """
        Tile window to the left part of the screen.

        -m tile_left
    """

    print(f"Left Tiling Window {window}")

    """
    x = 0
    y = 0
    w = int(w/2)
    h = h
    print(f"New Window pos: ({_x}, {_y}), New Window size: ({_w}, {_h})")
    """

    __edit_window(
        window,
        x=0,
        y=0,
        w=int(w/2),
        h=h
    )


def tile_right(window):
    """
        Tile window to the right part of the screen.

        -m tile_right
    """

    print(f"Tiling Right Window {window}")

    """
    _x = int(width/2)
    _y = 0
    _w = int(width / 2) - 10    # 10 = border width
    _h = usable_height

    print(f"New Window pos: ({_x}, {_y}), New Window size: ({_w}, {_h})")
    """
    __edit_window(
        window,
        x=int(w/2),
        y=0,
        w=int(w / 2),
        h=h
    )


def centering_window(window):
    """
        Centers the active window.

        -m center

        Used with --noresize the active window is not resized when centered
    """

    print(f"Centering Window {window}")

    __edit_window(
        window,
        x=50,
        y=50,
        w=w-100,
        h=h-100
    )

    """
    if args.noresize:
        # centering windows without resize dims
        print('\t with NoResize mode')

        _x = int((width - win_size.width) / 2)
        _y = int((height - win_size.height) / 2)
        _w = win_size.width
        _h = win_size.height

    else:
        # centering windows and resize dims
        print('\t with Resize mode')

        _x = x
        _y = y
        _w = width - (x * 2)
        _h = height - (y * 2)

    print(f"New Window pos: ({_x}, {_y}), New Window size: ({_w}, {_h})")
    """

if __name__ == '__main__':
    # define selectable options
    # type: Dict[str, Callable[[Window], None]]
    options = {
        'center': centering_window,  # center window
        'tile_left': tile_left,  # tiling window to the left
        'tile_right': tile_right,  # tiling window to the right
    }

    # init argument parser
    parser = argparse.ArgumentParser(description='My awesome python tiling assistant !')

    # arguments
    parser.add_argument(
        '-m',
        '--mode',
        type=str,
        choices=options.keys(),
        required=True,
        help='Choose how to tile the active window'
    )
    parser.add_argument(
        '--noresize',
        action='store_true',
        help='Center window without resize it'
    )

    args = parser.parse_args()

    main()
