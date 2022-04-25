"""This file contain methods used to streamline blender addon creation workflow
"""

import os
import shutil
import subprocess
import pathlib
import psutil

def kill_processes(process_name: str):
    """
    Kills all processes with given name
    """
    for proc in psutil.process_iter():
        # Check whether the process name matches
        if proc.name() == process_name:
            print(f"Killing process:{proc.name()}")
            proc.kill()


def run_blender_side_script(addons_data: dict):
    """
    Runs blender as subprocess from location saved in JSON file
    and run a script for blender-side operations
    """
    blender_path = os.path.join(addons_data["blender_exe_loc"], "blender.exe")
    # Setting up args to run blender with
    args =[
        blender_path,
        "-P",
        "-b",
        os.path.join(pathlib.Path(__file__).parents[0].resolve(),"addons_enable.py")
    ]

    # Running blender as subprocess, with blender-side script
    try:
        print("Starting Blender and running blender-side script")
        subprocess.run(args)
        print("Successfully reimported addons!")
    except OSError as error:
        print(f"Error occured while starting blender:\n{error}")


def zip_new_addons(addons_data: dict):
    """
    Creates zip files from exsisting WIP addons in
    directory provided in JSON file
    """

    directories_to_zip = []
    addons_dir = addons_data["addons_dir_path"]

    # Creates a list of addons to zip, matching dir names with JSON file
    for addon in addons_data["addons"]:
        for folder in os.listdir(addons_dir):
            if addon["addon_name"] == folder:
                directories_to_zip.append(folder)

    # Lists directories to zip
    print(f"Those folders will be zipped: {directories_to_zip}")
    
    # Creating .zip files
    print("Zipping...")
    os.chdir(addons_dir)
    for z_folder in directories_to_zip:
        shutil.make_archive(str(z_folder), "zip", os.path.join(addons_dir, z_folder,))
    
    print("Zipping Done!")


def clean_old_addon_version(addon_name: str, blender_version: str):
    """
    Clears old addon version files from %APPDATA% 
    """
    # Gets application data path from system env
    appdata_path = os.getenv('APPDATA')

    # Deletes entire directory trees associated with addon in it current version
    try:
        add_path = (os.path.join(appdata_path, "Blender Foundation", "Blender", blender_version, "scripts", "addons", addon_name))
        shutil.rmtree(add_path)
        print(f"Old {addon_name} directory removed successfully")
    except OSError as error:
        print(f"Error while removing old addon version:\n{error}")


def copy_and_unzip_new_addons (addon_name: str, blender_version: str, addons_dir_path: dict):
    """
    Copies zip files from WIP addons directory into 
    blender addons directory and unpacks them
    """
    # Sets needed paths
    appdata_path = os.getenv('APPDATA')
    add_path = os.path.join(appdata_path, "Blender Foundation", "Blender", blender_version, "scripts", "addons")
    zips_path = os.path.abspath(addons_dir_path)

    try:
        # Copies .zip files
        shutil.copy(os.path.join(zips_path,addon_name+'.zip'), add_path)
        print(f"New {addon_name} zip copied successfully")
        try:
            # Unpacks .zip files
            shutil.unpack_archive(os.path.join(add_path,addon_name+".zip"),os.path.join(add_path,addon_name))
            print(f"New {addon_name} zip unpacked successfully")
        except OSError as error2:
            print(f"Error while unpacking zip:\n{addon_name}:{error2}")

    except OSError as error:
        print(f"Error while copying new zipped addon version:\n{error}")
