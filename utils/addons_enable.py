"""
This is a blender-side script used to enable new addons versions
from unpacked .zip files
"""

try:
    import bpy
except ModuleNotFoundError:
    pass

import json
import os
import sys
import pathlib


# Opening and reading a JSON file
def get_addons_data(filename: str) -> dict:
    """
    Tries to open a json file, checking if it exists and contains correct data
    """

    # Opens JSON file to match its data with addons in WIP addons directory
    try:
        with open(os.path.join(pathlib.Path(__file__).parent.resolve(),filename)) as json_file:
            data = json.load(json_file)
    except FileNotFoundError as error:
        print(f"Error occured while opening JSON file:\n{error}")
        sys.exit()
    except json.decoder.JSONDecodeError:
        print('There is an incorrect value in json file, aborting... ')
        sys.exit()
    else:
        # Returns python dict
        return data


# Gets data from JSON file
addons_data = get_addons_data("addons.json")

# Enables every addon specified in JSON file
for addon in addons_data["addons"]:
    try:
        bpy.ops.preferences.addon_enable(module=addon['addon_name'])
        print(f"{addon['addon_name']} has been enabled")
    except NameError as n_err:
        pass
    except BaseException as err:
        print(f"ERROR: {addon['addon_name']} has NOT been enabled: {err}") 

# Saves user preferences to keep addons enabled after quiting blender
try:
    bpy.ops.wm.save_userpref()
except NameError as n_err:
    pass
except BaseException as err:
    print(f"Error occured while saving blender user preferences:\n{err}")
