from utils.reimport_addons import *
from utils.addons_enable import get_addons_data


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
        copy_and_unzip_new_addons(addon["addon_name"], addon["blender_version"], addons_data["addons_dir_path"])
  

    # Restarts blender from path taken from JSON
    
    start_blender(addons_data)


    # Instaling addons within blender


if __name__ == '__main__':
    main()
    sys.exit()