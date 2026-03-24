#!/usr/bin/env python3

import os
import utils

PHOTO_SUFFIX='.jpg'
WORKING_DIR=os.path.abspath(os.fsencode('./'))
DEPLOYMENT_DIR=os.path.join(WORKING_DIR, os.fsencode('_site'))
ASSET_DIR=os.path.join(DEPLOYMENT_DIR, os.fsencode('assets'))
YAML_FILE=os.path.join(WORKING_DIR, os.fsencode('photos.yaml'))

PHOTOS_TO_PRESERVE=['preview.jpg']

def clear_photos(directory, used_file_paths):
    all_file_paths = []

    for file in os.listdir(directory):
        filename = os.fsdecode(file)

        if filename.endswith(PHOTO_SUFFIX):
            all_file_paths.append(utils.to_absolute_path(directory, file))

#   print(used_file_paths)
#   print(all_file_paths)

    count = 0

    for photo_to_preserve in PHOTOS_TO_PRESERVE:
        used_file_paths.append(utils.to_absolute_path(ASSET_DIR, photo_to_preserve))
    
    for file_to_delete in (x for x in all_file_paths if x not in used_file_paths):
        print('delete ' + file_to_delete)
        os.remove(file_to_delete)
        count+=1

    return count

def get_used_file_paths(directory, photo_data_list):
    used_file_paths = []

    for photo_data in photo_data_list:
        used_file_paths.append(utils.to_absolute_path(directory, photo_data['file_path']))

    return used_file_paths



def main():
    print("Clearing photos ...")
    used_file_paths = get_used_file_paths(DEPLOYMENT_DIR, utils.read_from_yaml(YAML_FILE))
    count = clear_photos(ASSET_DIR, used_file_paths)

    print(f"Cleared {count} photos")



if __name__=="__main__":
    main()
