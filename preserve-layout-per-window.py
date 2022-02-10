#!/usr/bin/python

# This script requires i3ipc-python package (install it from a system package manager
# or pip).
# It makes inactive windows transparent. Use `transparency_val` variable to control
# transparency strength in range of 0…1 or use the command line argument -o.

import argparse
import i3ipc
from functools import partial
from collections import defaultdict
id_to_layouts = defaultdict(lambda :defaultdict(lambda :0))

def on_window_focus(ipc, event):
    global prev_focused
    print("Got event")

    focused = event.container
    #if prev_focused and (True or prev_focused.app_id == 'termite'):
    #    prev_focused.command('opacity 0.8')

    if True or focused.app_id == 'termite':
        tree = ipc.get_tree()
        focused = tree.find_by_id(focused.id)
        if focused:
            curent_workspace = focused.workspace()
            #from ipdb import set_trace; set_trace()
            for node in curent_workspace.descendants():
                node.command('opacity 0.8')
            focused.command('opacity 1')


    print(f"last_focused: {prev_focused}, new: {focused}")
    if prev_focused and focused.id != prev_focused.id: 
        current_layouts = {i.identifier: i.xkb_active_layout_index for i in  ipc.get_inputs()}
        id_to_layouts[prev_focused.id] = current_layouts
        ipc = i3ipc.Connection()
        for l in current_layouts:
            try:
                ipc.command(f'input {l} xkb_switch_layout {id_to_layouts[focused.id][l]}')
            except KeyError:
                pass

    prev_focused = focused




if __name__ == "__main__":
    transparency_val = "0.80"

    parser = argparse.ArgumentParser(
        description="This script tracks keyboard layouts of different windows and preserves them"
    )
    args = parser.parse_args()
    ipc = None
    while not ipc:
        try:
            ipc = i3ipc.Connection()
            prev_focused = None
        except Exception:
            print("failed creating IPC. retrying...")
            exit(2)

    print("Created IPC")
    ipc.on("window::focus", partial(on_window_focus))
    ipc.main()
    exit(1)
