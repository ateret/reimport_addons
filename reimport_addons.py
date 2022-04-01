"""
Deletes existing addon folder from specified blender version.
Uses JSON file to specify addons and versions
"""

from asyncio import subprocess
import json
import os
import sys
import psutil
import shutil
import subprocess
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
    except BaseException as error:
        print(f"Error while removing old addon version {error}")

def copy_and_unzip_new_addons (addon_name: str, blender_version: str):
    # Gets application data path from system env
    appdata_path = os.getenv('APPDATA')
    add_path = os.path.join(appdata_path, "Blender Foundation", "Blender", blender_version, "scripts", "addons")
    zips_path = pathlib.Path(__file__).parents[1].resolve()

    try:
        shutil.copy(os.path.join(zips_path,addon_name+'.zip'), add_path)
        try:
            shutil.unpack_archive(os.path.join(add_path,addon_name+".zip"),os.path.join(add_path,addon_name))
        except BaseException as error2:
            print(f"Error while unpacking zip{addon_name}:{error2}")

    except BaseException as error:
        print(f"Error while copying new zipped addon version {error}")




def main():
    # Gets data from JSON file
    addons_data = get_addons_data("addons.json")

    # Killing Blender
    blender_process = "blender.exe"
    kill_blender(blender_process)

    # Zips new versions of addons
    zip_new_addons(addons_data)

    # Cleans up every addon folder from Appdata and copies new zips
    for addon in addons_data["addons"]:
        clean_old_addon_version(addon["addon_name"], addon["blender_version"])
        copy_and_unzip_new_addons(addon["addon_name"], addon["blender_version"])
  

    # Restarts blender from path taken from JSON
    
    start_blender(addons_data)


    # Instaling addons within blender


if __name__ == '__main__':
    main()
    sys.exit()
