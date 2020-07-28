#!/usr/bin/python

# This script requires i3ipc-python package (install it from a system package manager
# or pip).
# It makes inactive windows transparent. Use `transparency_val` variable to control
# transparency strength in range of 0…1 or use the command line argument -o.

import argparse
import i3ipc
import signal
import sys
from functools import partial
from collections import defaultdict
id_to_layout = defaultdict(lambda :0)

def on_window_focus(inactive_opacity, ipc, event):
    global prev_focused
    global prev_workspace

    focused = event.container
    workspace = ipc.get_tree().find_focused().workspace().num
    #import pdb; pdb.set_trace()

    if focused.id != prev_focused.id:  # https://github.com/swaywm/sway/issues/2859
        current_layouts = set(list(map(lambda x:x.xkb_active_layout_index, ipc.get_inputs())))
        current_layouts.remove(None)
        current_layout = current_layouts.pop()
        id_to_layout[prev_focused.id] = current_layout
        if current_layout != id_to_layout[focused.id]:
            ipc = i3ipc.Connection()
            ipc.command(f'input * xkb_switch_layout {id_to_layout[focused.id]}')

        prev_focused = focused
        prev_workspace = workspace




if __name__ == "__main__":
    transparency_val = "0.80"

    parser = argparse.ArgumentParser(
        description="This script allows you to set the transparency of unfocused windows in sway."
    )
    parser.add_argument(
        "--opacity",
        "-o",
        type=str,
        default=transparency_val,
        help="set opacity value in range 0...1",
    )
    args = parser.parse_args()

    ipc = i3ipc.Connection()
    prev_focused = None

    ipc.on("window::focus", partial(on_window_focus, args.opacity))
    ipc.main()
