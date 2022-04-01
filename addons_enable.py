import bpy
import os
import pathlib

os.chdir(pathlib.Path(__file__).parents[0].resolve())
print(pathlib.Path(__file__).parents[0].resolve())
from .reimport_addons import get_addons_data 




# Gets data from JSON file
addons_data = reimport_addons.get_addons_data("addons.json")

# bpy.ops.wm.addon_install(filepath='/home/shane/Downloads/testaddon.py')
for addon in addons_data["addons"]:
    bpy.ops.wm.addon_enable(module=addon['addon_name'])

bpy.ops.wm.save_userpref()