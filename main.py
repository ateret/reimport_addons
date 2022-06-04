"""Simplify blender addons creation pipeline

This script closes all active blender processes, clean old addon files,
zips new one in specified WIP addon directory, copies them into
proper blender version addon directory, unpacks them and then runs
blender script to activate them, and saves user preferences.

This allows to see changes to your addon without having to manually
disable and remove old version, pack, copy and install new one,
streamlining this tedious task to 1 click

Requires "addons.json" within same directory to run. This file is
used to specify WIP addon location, addon versions and
main blender.exe location

Requires: psutil
"""

import sys
from utils.reimport_addons import *
from utils.addons_enable import get_addons_data


def main():
    """
    This is a main function scripts. It uses methods from reimport_addons.py
    """
    # Gets data from JSON file
    addons_data = get_addons_data("addons.json")

    # Killing Blender process
    blender_process = "blender.exe"
    kill_process(blender_process)

    # Zips new versions of addons
    zip_new_addons(addons_data)

    # Cleans up every addon folder from Appdata, copies and unpacks new zips
    for addon in addons_data["addons"]:
        clean_old_addon_version(addon["addon_name"], addon["blender_version"])
        copy_and_unzip_new_addons(addon["addon_name"], addon["blender_version"], addons_data["addons_dir_path"])

    # Restarts blender from path taken from JSON and starts blender-side script
    run_blender_side_script(addons_data)

if __name__ == '__main__':
    main()
    sys.exit()
