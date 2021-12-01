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
        Centers the active window.

        -m center

        Used with --noresize the active window is not resized when centered
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
        'tile_right': tile_right  # tiling window to the right
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

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
"""
import Xlib.display

WINDOW_NAME = 'some window name'

d = Xlib.display.Display()
r = d.screen().root

x = 0
y = 100
width = r.get_geometry().width
height = r.get_geometry().height - y

window_ids = r.get_full_property(
    d.intern_atom('_NET_CLIENT_LIST'), Xlib.X.AnyPropertyType
).value

for window_id in window_ids:
    window = d.create_resource_object('window', window_id)
    if window.get_wm_name() == WINDOW_NAME:
        print('Moving Window')
        window.configure(
            x=x,
            y=y,
            width=width,
            height=height,
            border_width=0,
            stack_mode=Xlib.X.Above
        )
        d.sync()
"""

'''
ython-xlib example which reacts to changing the active window/title.
Requires:
- Python
- python-xlib
Tested with Python 2.x because my Kubuntu 14.04 doesn't come with python-xlib
for Python 3.x.
Design:
-------
Any modern window manager that isn't horrendously broken maintains an X11
property on the root window named _NET_ACTIVE_WINDOW.
Any modern application toolkit presents the window title via a property
named _NET_WM_NAME.
This listens for changes to both of them and then hides duplicate events
so it only reacts to title changes once.
Known Bugs:
-----------
- Under some circumstances, I observed that the first window creation and last
  window deletion on on an empty desktop (ie. not even a taskbar/panel) would
  go ignored when using this test setup:
      Xephyr :3 &
      DISPLAY=:3 openbox &
      DISPLAY=:3 python3 x11_watch_active_window.py
      # ...and then launch one or more of these in other terminals
      DISPLAY=:3 leafpad


# pylint: disable=unused-import
from contextlib import contextmanager
from typing import Any, Dict, Optional, Tuple, Union  # noqa

from Xlib import X
from Xlib.display import Display
from Xlib.error import XError
from Xlib.xobject.drawable import Window
from Xlib.protocol.rq import Event

# Connect to the X server and get the root window
disp = Display()
root = disp.screen().root

# Prepare the property names we use so they can be fed into X11 APIs
NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')  # UTF-8
WM_NAME = disp.intern_atom('WM_NAME')           # Legacy encoding

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


def get_active_window() -> Tuple[Optional[int], bool]:
    """Return a (window_obj, focus_has_changed) tuple for the active window."""
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


def _get_window_name_inner(win_obj: Window) -> str:
    """Simplify dealing with _NET_WM_NAME (UTF-8) vs. WM_NAME (legacy)"""
    for atom in (NET_WM_NAME, WM_NAME):
        try:
            window_name = win_obj.get_full_property(atom, 0)
        except UnicodeDecodeError:  # Apparently a Debian distro package bug
            title = "<could not decode characters>"
        else:
            if window_name:
                win_name = window_name.value  # type: Union[str, bytes]
                if isinstance(win_name, bytes):
                    # Apparently COMPOUND_TEXT is so arcane that this is how
                    # tools like xprop deal with receiving it these days
                    win_name = win_name.decode('latin1', 'replace')
                return win_name
            else:
                title = "<unnamed window>"

    return "{} (XID: {})".format(title, win_obj.id)


def get_window_name(win_id: Optional[int]) -> Tuple[Optional[str], bool]:
    """Look up the window name for a given X11 window ID"""
    if not win_id:
        last_seen['title'] = None
        return last_seen['title'], True

    title_changed = False
    with window_obj(win_id) as wobj:
        if wobj:
            try:
                win_title = _get_window_name_inner(wobj)
            except XError:
                pass
            else:
                title_changed = (win_title != last_seen['title'])
                last_seen['title'] = win_title

    return last_seen['title'], title_changed


def handle_xevent(event: Event):
    """Handler for X events which ignores anything but focus/title change"""
    if event.type != X.PropertyNotify:
        return

    changed = False
    if event.atom == NET_ACTIVE_WINDOW:
        if get_active_window()[1]:
            get_window_name(last_seen['xid'])  # Rely on the side-effects
            changed = True
    elif event.atom in (NET_WM_NAME, WM_NAME):
        changed = changed or get_window_name(last_seen['xid'])[1]

    if changed:
        handle_change(last_seen)


def handle_change(new_state: dict):
    """Replace this with whatever you want to actually do"""
    print(new_state)

if __name__ == '__main__':
    # Listen for _NET_ACTIVE_WINDOW changes
    root.change_attributes(event_mask=X.PropertyChangeMask)

    # Prime last_seen with whatever window was active when we started this
    get_window_name(get_active_window()[0])
    handle_change(last_seen)

    while True:  # next_event() sleeps until we get an event
        handle_xevent(disp.next_event())
@thor27
thor27 commented on Nov 2, 2017 •
Hi!
Thanks a lot for this gist, I used to create a Steam "window manager", in a working in progress version of the steam-login project (https://github.com/thor27/steam-login/) that is licensed under GPL-v2+.

I still didn't upload it, since I don't know the license for the code on your gist.

Can I use it in my GPL-v2+ project?

thanks!

@ssokolow
Author
ssokolow commented on Nov 2, 2017
I actually posted this as the "full version" of a code snippet I put up on StackOverflow, but you can consider it MIT-licensed if you'd like something more concrete.

Regardless of which terms you use it under, I'd appreciate a shout-out. Nothing fancy... sticking a code comment like this above it will do:

# Based on code by Stephan Sokolow
# Source: https://gist.github.com/ssokolow/e7c9aae63fb7973e4d64cff969a78ae8
@matanster
matanster commented on May 4, 2020 •
Is this code part of any maintained open-source repository right now? didn't realize that getting the active window require so much.

@ssokolow
Author
ssokolow commented on May 4, 2020 •
Is this code part of any maintained open-source repository right now?

I don't go out and try to find any, so I wouldn't know unless somebody tells me.

didn't realize that getting the active window require so much.

It's not so much that "getting the active window requires so much" as "if you need to do something GTK and Qt don't provide a wrapper for, you have to speak raw Xlib... and raw Xlib is verbose even before you check for and deal with the variations in what programs were expected to return across X's three-decade-long lifespan".

Remember, this code:

Watches for changes to the active window ID
Whenever the active window ID changes, unhooks the "watch for changes to the title on this window" code from the old window and hooks it up to the new window.
Whenever the window title changes, deals with how X predates Unicode so there are two different ways to specify the title and some applications never got updated to use the newer one.
Deals with the fact that, because this is inter-process communication we're dealing with, the application on the other end could die in between asking for the active window and asking for its title, or other things like that.
Code written against the raw Win32 API is at least as verbose and ugly. Personally, I think it's worse.

@matanster
matanster commented on May 5, 2020
Thanks so much for comments, this helps motivate and better resonate with the code!

@ehula
ehula commented on May 10, 2020
This works great except it doesn't seem to notice when the active window ID changes if the new window has the same title. Is there a way to get it do that as well?

@ssokolow
Author
ssokolow commented on May 10, 2020 •
@ehula That's a designed behaviour. To disable it, replace line 111

            changed = changed or get_window_name(last_seen['xid'])[1]
...with these lines:

            get_window_name(last_seen['xid'])[1]
            changed = True
@matanster
matanster commented on May 10, 2020
@ehula care to elaborate a scenario or application type where that would happen?

@ehula
ehula commented on May 10, 2020
@ssokolow Worked like a charm! Thanks a bunch! Great script!

@ehula
ehula commented on May 10, 2020
@matanster Sure. The biggest issue for me was having two or more terminals cd'ed to the same directory. They could all be running different programs, but x11 reports them as all having the same title. Also, two or more browser instances showing the same page would do the same thing.

@ehula
ehula commented on May 12, 2020
@ssokolow I just noticed another peculiarity in my particular situation. I am wanting to run your script when I start X, but I found that if there are no windows open when your script is run, it exits. Is there a way to have it run and stay open even if there are no windows currently open. The script continues to run if I close all the open windows, so it seems to only be sensitive to no windows open on launch.

@ssokolow
Author
ssokolow commented on May 12, 2020
get_active_window() was coded with the assumption that there will always exist an active window that the Window Manager has placed in the _NET_ACTIVE_WINDOW property and it crashes if the root.get_full_property call on line 52 returns None.

I've rewritten the code to account for that, added some MyPy type annotations, and fixed a couple of oversights revealed by that as well as a potential bug that showed up during testing. Let me know if you have any further problems.

@ehula
ehula commented on May 12, 2020
So far it's working just great! Thanks a bunch!

@ConnorGutman
ConnorGutman commented on Jul 10, 2020
Wonderful implementation, thank you for the detailed comments!

@veasnama
veasnama commented on Apr 15 •
Does anyone know how to turn code above into rust code ? this is what I did.

use std::collections::HashMap;
use std::error::Error;

use x11rb::connection::Connection;

use x11rb::protocol::xproto::{Atom, AtomEnum, ConnectionExt, GetPropertyReply, Window};

use x11rb::protocol::Event;
use x11rb::x11_utils::TryParse;
use x11rb::xcb_ffi::XCBConnection;

fn find_active_window(
conn: &impl Connection,
root: Window,
net_active_window: Atom,
hash_map: &mut HashMap<&str, Option>,
) -> Result<(Window, bool), Box> {
let window: Window = AtomEnum::ANY.into();
let active_window = conn
.get_property(false, root, net_active_window, window, 0, 1)?
.reply()?;
if active_window.format == 32 && active_window.length == 1 {
// Things will be so much easier with the next release:
let widnow_id = u32::try_parse(&active_window.value)?.0;
let focus_changed = widnow_id != hash_map["xid"].unwrap();
hash_map.insert("xid", Some(widnow_id));
Ok((u32::try_parse(&active_window.value)?.0, focus_changed))
} else {
// Query the input focus
Ok((conn.get_input_focus()?.reply()?.focus, false))
}
}
fn parse_string_property(property: &GetPropertyReply) -> &str {
std::str::from_utf8(&property.value).unwrap_or("Invalid utf8")
}
fn parse_wm_class(property: &GetPropertyReply) -> (&str, &str) {
if property.format != 8 {
return (
"Malformed property: wrong format",
"Malformed property: wrong format",
);
}
let value = &property.value;
// The property should contain two null-terminated strings. Find them.
if let Some(middle) = value.iter().position(|&b| b == 0) {
let (instance, class) = value.split_at(middle);
// Skip the null byte at the beginning
let mut class = &class[1..];
// Remove the last null byte from the class, if it is there.
if class.last() == Some(&0) {
class = &class[..class.len() - 1];
}
let instance = std::str::from_utf8(instance);
let class = std::str::from_utf8(class);
(
instance.unwrap_or("Invalid utf8"),
class.unwrap_or("Invalid utf8"),
)
} else {
("Missing null byte", "Missing null byte")
}
}

pub fn start() -> Result<(), Box> {
let mut last_seen = HashMap::new();
last_seen.insert("xid", Some(10000000));
// Set up our state
let (conn, screen) = XCBConnection::connect(None)?;
let root = conn.setup().roots[screen].root;
let net_activate_win = conn.intern_atom(false, b"_NET_ACTIVE_WINDOW").unwrap();
let net_wm_name = conn.intern_atom(false, b"_NET_WM_NAME").unwrap();
let utf8_string = conn.intern_atom(false, b"UTF8_STRING").unwrap();
let net_activate_win = net_activate_win.reply().unwrap().atom;
let net_wm_name = net_wm_name.reply().unwrap().atom;
let utf8_string = utf8_string.reply().unwrap().atom;
let (focus, _) = find_active_window(&conn, root, net_activate_win, &mut last_seen)?;
println!("XID {:?}", focus);
// Collect the replies to the atoms
let (net_wm_name, utf8_string) = (net_wm_name, utf8_string);
let (wm_class, string): (AtomEnum, AtomEnum) =
(AtomEnum::WM_CLASS.into(), AtomEnum::STRING.into());
// Get the property from the window that we need
let name = conn.get_property(false, focus, net_wm_name, utf8_string, 0, u32::max_value())?;
let class = conn.get_property(false, focus, wm_class, string, 0, u32::max_value())?;
let (name, class) = (name.reply()?, class.reply()?);
println!("Window name: {:?}", parse_string_property(&name));
let (instance, class) = parse_wm_class(&class);
println!("Window instance: {:?}", instance);
println!("Window class: {:?}", class);
// Print out the result

loop {
    conn.flush().unwrap();
    match conn.wait_for_event() {
        Ok(event) => match event {
            Event::PropertyNotify(e) => {
                println!("Event: {:?}", e);
            }
            _ => {}
        },
        Err(e) => println!("Error: {:?}", e),
    }
}
}

@ShayBox
ShayBox commented on May 16
You should package the main into its own function and have a callback so this can be used fully as a lib instead of modifying it, it can be used directly as a submodule/its own dependency

@ssokolow
Author
ssokolow commented on May 24
@ShayBox The problem is that, when you start to think about how to integrate it into programs which may already have an Xlib connection for other purposes, it's not as simple to offer it up structured that way. Unnecessarily pushing a program to open more X sockets is a code smell.

@ncvescera

Leave a comment
No file chosen
Attach files by dragging & dropping, selecting or pasting them.
© 2021 GitHub, Inc.
Terms
Privacy
Security
Status
Docs
Contact GitHub
Pricing
API
Training
Blog
About
'''