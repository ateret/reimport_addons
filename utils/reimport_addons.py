"""
Deletes existing addon folder from specified blender version.
Uses JSON file to specify addons and versions
"""

from asyncio import subprocess
import os
import psutil
import shutil
import subprocess
import pathlib






def kill_blender(process_name: str):
    """
    Kills blender process, so blender doesnt write addon data again
    """
    for proc in psutil.process_iter():
        # Check whether the process name matches
        if proc.name() == process_name:
            print(f"Killing {proc.name()}")
            proc.kill()


def start_blender(addons_data: dict):
    """
    Runs blender from location saved in JSON file
    """
    blender_path = os.path.join(addons_data["blender_exe_loc"], "blender.exe")
    args =[
        blender_path,
        "-P",
        os.path.join(pathlib.Path(__file__).parents[0].resolve(),"addons_enable.py")
    ]
    try:
        subprocess.run(args)
    except BaseException as error:
        print(error)


def zip_new_addons(addons_data: dict):
    folders_to_zip = []
    addons_dir = addons_data["addons_dir_path"]
    for addon in addons_data["addons"]:
        for folder in os.listdir(addons_dir):
            if addon["addon_name"] == folder:
                folders_to_zip.append(folder)

    print(f"Those folders will be zipped: {folders_to_zip}")
    print(f"Zipping....")

    os.chdir(addons_dir)
    for z_folder in folders_to_zip:
        
        shutil.make_archive(str(z_folder), "zip", os.path.join(addons_dir, z_folder,))
    
    print(f"Zipping Done!")


def clean_old_addon_version(addon_name: str, blender_version: str):
    # Gets application data path from system env
    appdata_path = os.getenv('APPDATA')

    # Deletes entire directory trees associated with addon in it current version
    try:
        add_path = (os.path.join(appdata_path, "Blender Foundation", "Blender", blender_version, "scripts", "addons", addon_name))
        shutil.rmtree(add_path)
        print(f"{addon_name} removed successfully")
    except BaseException as error:
        print(f"Error while removing old addon version {error}")


def copy_and_unzip_new_addons (addon_name: str, blender_version: str, addons_dir_path: dict):
    # Gets application data path from system env
    appdata_path = os.getenv('APPDATA')
    add_path = os.path.join(appdata_path, "Blender Foundation", "Blender", blender_version, "scripts", "addons")
    zips_path = os.path.abspath(addons_dir_path)

    try:
        shutil.copy(os.path.join(zips_path,addon_name+'.zip'), add_path)
        print(f"{addon_name} zip copied successfully")
        try:
            shutil.unpack_archive(os.path.join(add_path,addon_name+".zip"),os.path.join(add_path,addon_name))
            print(f"{addon_name} zip unpacked successfully")
        except BaseException as error2:
            print(f"Error while unpacking zip{addon_name}:{error2}")

    except BaseException as error:
        print(f"Error while copying new zipped addon version {error}")

