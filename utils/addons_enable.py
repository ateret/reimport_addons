try: 
    import bpy
except ModuleNotFoundError:
    pass

import json
from lib2to3.pytree import Base
import os
import sys
import pathlib


# Opening and reading a JSON file
def get_addons_data(filename: str) -> dict:
    """
    Tries to open a json file, checking if it exists and contains correct data
    """
    try:
        with open(os.path.join(pathlib.Path(__file__).parent.resolve(),filename)) as json_file:
            addons_data = json.load(json_file)
    except FileNotFoundError as error:
        print(error)
        sys.exit()
    except json.decoder.JSONDecodeError:
        print('There is an incorrect value in json file, aborting... ')
        sys.exit()
    else:
        # Returns python dict
        return addons_data


# Gets data from JSON file
addons_data = get_addons_data("addons.json")

# bpy.ops.wm.addon_install(filepath='/home/shane/Downloads/testaddon.py')
for addon in addons_data["addons"]:
    try:
        bpy.ops.preferences.addon_enable(module=addon['addon_name'])
        print(f"{addon['addon_name']} has been enabled")
    except BaseException as err: 
        print(f"ERROR: {addon['addon_name']} has NOT been enabled: {err}")
        

try: 
    bpy.ops.wm.save_userpref() 
except:
    pass