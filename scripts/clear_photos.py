#!/usr/bin/env python3

import os
import yaml

PHOTO_SUFFIX='.jpg'
WORKING_DIR=os.path.abspath(os.fsencode('./'))
DEPLOYMENT_DIR=os.path.join(WORKING_DIR, os.fsencode('_site'))
ASSET_DIR=os.path.join(DEPLOYMENT_DIR, os.fsencode('assets'))
YAML_FILE=os.path.join(WORKING_DIR, os.fsencode('photos.yaml'))

PHOTOS_TO_PRESERVE=['preview.jpg']

def clear_photos(directory, used_file_paths):
    all_file_paths = []
    

    for file in os.listdir(directory):
        file_name = os.fsdecode(file)

        if file_name.endswith(PHOTO_SUFFIX):
            all_file_paths.append(to_absolute_path(directory, file))

#   print(used_file_paths)
#   print(all_file_paths)
    
    for photo_to_preserve in PHOTOS_TO_PRESERVE:
        used_file_paths.append(to_absolute_path(ASSET_DIR, photo_to_preserve))
    
    for file_to_delete in (x for x in all_file_paths if x not in used_file_paths):
        print('delete ' + file_to_delete)
        os.remove(file_to_delete)


def get_used_file_paths(directory, photo_data_list):
    used_file_paths = []

    for photo_data in photo_data_list:
        used_file_paths.append(to_absolute_path(directory, photo_data['file_path']))

    return used_file_paths

def to_absolute_path(directory, filename):
    return os.fsdecode(os.path.join(directory, os.fsencode(filename)))

def read_from_yaml(source):
    try:
        with open(source, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

            return yaml_data['photos']
    except:
        return []


def main():
    used_file_paths = get_used_file_paths(DEPLOYMENT_DIR, read_from_yaml(YAML_FILE))
    clear_photos(ASSET_DIR, used_file_paths)


if __name__=="__main__":
    main()
