#!/usr/bin/env python3

import argparse
from contextlib import contextmanager
from typing import Any, Dict, Optional, Tuple, Union, Callable  # noqa

from ewmh import EWMH


# wm manager
ewmh = EWMH()

# get desktop size and real desktop sizes
w, h = ewmh.getDesktopGeometry()
xr, yr, wr, hr = ewmh.getWorkArea()[:4]


def main():
    print("Desktop Geometry: ", w, h)
    print("Desktop WorkArea:", xr, yr, wr, hr)

    # execute user selected tiling operation
    options[args.mode]()

    ewmh.display.flush()


def __edit_window(win=None, x=None, y=None, w=None, h=None):
    if win is None:
        win = ewmh.getActiveWindow()

    ewmh.setMoveResizeWindow(
        win,
        x=x,
        y=y,
        w=w,
        h=h
    )

    if h is None:
        ewmh.setWmState(win, 1, '_NET_WM_STATE_MAXIMIZED_VERT')

    print(f"New Window {win} pos: ({x}, {y}), New Window size: ({w}, {h})")


def tile_left():
    """
        Tile window to the left part of the screen.

        -m tile_left
    """

    print(f"Left Tiling Window")

    __edit_window(x=0, y=0, w=int(wr/2)) # w or wr ??


def tile_right():
    """
        Tile window to the right part of the screen.

        -m tile_right
    """

    print(f"Tiling Right Window")

    __edit_window(x=int(wr/2), y=0, w=int(wr / 2)) # w or wr ??


def tile_leftcenter():
    """
        Tile window to the left-center (2/3) part of the screen.

        -m tile_leftcenter
    """

    print(f"Tiling LeftCenter Window")

    __edit_window(x=0, y=0, w=int(wr / 3)*2)  # w or wr ??


def tile_rightcenter():
    """
        Tile window to the right-center (2/3) part of the screen.

        -m tile_rightcenter
    """

    print(f"Tiling RightCenter Window")

    __edit_window(x=int(wr / 3), y=0, w=int(wr / 3)*2)  # w or wr ??


def tile_leftleft():
    """
        Tile window to the left-left (1/3) part of the screen.

        -m tile_leftleft
    """

    print(f"Tiling RightCenter Window")

    __edit_window(x=0, y=0, w=int(wr / 3))  # w or wr ??


def tile_rightright():
    """
        Tile window to the right-right (1/3) part of the screen.

        -m tile_rightright
    """

    print(f"Tiling RightCenter Window")

    __edit_window(x=int(wr / 3) * 2, y=0, w=int(wr / 3))  # w or wr ??


def centering_window():
    """
        Centers the active window.

        -m center

        Used with --noresize the active window is not resized when centered
    """

    print(f"Centering Window")

    win = ewmh.getActiveWindow()
    win_size = get_window_size(win)

    if args.noresize:
        # centering windows without resize dims
        print('\t with NoResize mode')

        __edit_window(win, x=int((wr - win_size.width) / 2), y=int((hr - win_size.height) / 2), w=win_size.width, h=win_size.height)  # w or wr ??

    else:
        # centering windows and resize dims
        print('\t with Resize mode')

        __edit_window(x=(xr + 50), y=(yr + 50), w=(wr - 100), h=(hr - 100))  # w or wr ??


def get_window_size(window):
    """Returns window size object"""
    # get window dims
    win_size = window.get_geometry()
    print(f"Window pos: ({win_size.x}, {win_size.y})  Window size: ({win_size.width}, {win_size.height})")

    return win_size


if __name__ == '__main__':
    # define selectable options
    # type: Dict[str, Callable[[None], None]]
    options = {
        'center': centering_window,  # center window
        'tile_left': tile_left,  # tiling window to the left
        'tile_right': tile_right,  # tiling window to the right
        'tile_leftcenter': tile_leftcenter,
        'tile_rightcenter': tile_rightcenter,
        'tile_leftleft': tile_leftleft,
        'tile_rightright': tile_rightright,
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
