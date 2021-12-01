#!/usr/bin/python

import argparse
from contextlib import contextmanager
from typing import Any, Dict, Optional, Tuple, Union, Callable  # noqa

from Xlib import X
from Xlib.display import Display
from Xlib.error import XError
from Xlib.xobject.drawable import Window

# Display Vars
disp = Display()
root = disp.screen().root

# Display settings
x = 50                                  # x position where to puts windows
y = 50                                  # y position where to puts windows
width = root.get_geometry().width       # screen width (eg. 1920)
height = root.get_geometry().height     # screen height (eg. 1080)


def main():
    # get active window
    window = get_active_window()

    # execute user selected tiling operation
    options[args.mode](window)

    # update window
    disp.sync()


def tile_left(window: Window):
    """
        Tile window to the left part of the screen.

        -m tile_left
    """

    print(f"Left Tiling Window {window}")

    # get window size
    win_size = get_window_size(window)

    # tiling left windows
    window.configure(
        # where to put the window
        x=0,
        y=0,
        # new window dims
        width=int(width/2),
        height=height,
        # other stuff
        border_width=0,
        stack_mode=X.Above
    )


def tile_right(window: Window):
    """
        Tile window to the right part of the screen.

        -m tile_right
    """

    print(f"Tiling Right Window {window}")

    # get window size
    win_size = get_window_size(window)

    # tiling left windows
    window.configure(
        # where to put the window
        x=int(width/2),
        y=0,
        # new window dims
        width=int(width/2),
        height=height,
        # other stuff
        border_width=0,
        stack_mode=X.Above
    )


def tile_leftcenter(window: Window):
    """
        Tile window to the left-center (2/3) part of the screen.

        -m tile_leftcenter
    """

    print(f"Tiling LeftCenter Window {window}")

    # get window size
    win_size = get_window_size(window)

    # tiling LeftCenter windows
    window.configure(
        # where to put the window
        x=0,
        y=0,
        # new window dims
        width=int(width / 3)*2,
        height=height,
        # other stuff
        border_width=0,
        stack_mode=X.Above
    )


def tile_rightcenter(window: Window):
    """
        Tile window to the right-center (2/3) part of the screen.

        -m tile_rightcenter
    """

    print(f"Tiling RightCenter Window {window}")

    # get window size
    win_size = get_window_size(window)

    # tiling RightCenter windows
    window.configure(
        # where to put the window
        x=int(width / 3),
        y=0,
        # new window dims
        width=int(width / 3)*2,
        height=height,
        # other stuff
        border_width=0,
        stack_mode=X.Above
    )


def centering_window(window: Window):
    """
        Centers the active window.

        -m center

        Used with --noresize the active window is not resized when centered
    """

    print(f"Centering Window {window}")

    # get window size
    win_size = get_window_size(window)

    if args.noresize:
        # centering windows without resize dims
        print('\t with NoResize mode')
        window.configure(
            # where to put the window
            x=int((width - win_size.width) / 2),
            y=int((height - win_size.height) / 2),
            # new window dims
            width=win_size.width,
            height=win_size.height,
            # other stuff
            border_width=0,
            stack_mode=X.Above
        )
    else:
        # centering windows and resize dims
        print('\t with Resize mode')
        window.configure(
            # where to put the window
            x=x,
            y=y,
            # new window dims
            width=width - (x * 2),
            height=height - (y * 2),
            # other stuff
            border_width=0,
            stack_mode=X.Above
        )


def get_window_size(window: Window):
    """Returns window size object"""
    # get window dims
    win_size = window.get_geometry()
    print(f"Window pos: ({win_size.x}, {win_size.y})  Window size: ({win_size.width}, {win_size.height})")

    return win_size


def get_active_window():
    """Wrapper for getting the active window object. Returns the WindowObject of the active window."""

    # Prepare the property names we use so they can be fed into X11 APIs
    NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
    NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')  # UTF-8
    WM_NAME = disp.intern_atom('WM_NAME')  # Legacy encoding

    last_seen = {'xid': None, 'title': None}  # type: Dict[str, Any]

    @contextmanager
    def window_obj(win_id: Optional[int]) -> Window:
        """Simplify dealing with BadWindow (make it either valid or None)"""
        window_obj = None
        if win_id:
            try:
                window_obj = disp.create_resource_object('window', win_id)
            except XError:
                pass
        yield window_obj

    def _get_active_window() -> Tuple[Optional[int], bool]:
        """Return a (window_id, focus_has_changed) tuple for the active window."""

        response = root.get_full_property(NET_ACTIVE_WINDOW,
                                          X.AnyPropertyType)
        if not response:
            return None, False
        win_id = response.value[0]

        focus_changed = (win_id != last_seen['xid'])
        if focus_changed:
            with window_obj(last_seen['xid']) as old_win:
                if old_win:
                    old_win.change_attributes(event_mask=X.NoEventMask)

            last_seen['xid'] = win_id
            with window_obj(win_id) as new_win:
                if new_win:
                    new_win.change_attributes(event_mask=X.PropertyChangeMask)

        return win_id, focus_changed

    # get active window and return Window Object
    win_id, _ = _get_active_window()
    with window_obj(win_id) as window:
        return window


if __name__ == '__main__':
    # define selectable options
    # type: Dict[str, Callable[[Window], None]]
    options = {
        'center': centering_window,  # center window
        'tile_left': tile_left,  # tiling window to the left
        'tile_right': tile_right,  # tiling window to the right
        'tile_leftcenter': tile_leftcenter,
        'tile_rightcenter': tile_rightcenter,
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
