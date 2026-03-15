#!/usr/bin/env python3

import datetime
import os
import re
import subprocess
import shutil
import sys
import yaml
import zoneinfo


PHOTO_PREFIX='DSCF'
PHOTO_SUFFIX='.jpg'
ARTIST='marrat.eu'
WORKING_DIR=os.path.abspath(os.fsencode('./'))
DEPLOYMENT_DIR=os.path.join(WORKING_DIR, os.fsencode('_site'))
ASSET_DIR=os.path.join(WORKING_DIR, os.fsencode('_site/assets'))
YAML_FILE=os.path.join(WORKING_DIR, os.fsencode('photos.yaml'))
TIMEZONE=zoneinfo.ZoneInfo("Europe/Vienna")
SENSITIVE_EXIF_ATTRIBUTES=['timestamp']


class ExifData:
    def __init__(self, input_file):
        self.artist = ARTIST
        self.copyright = ARTIST

        self._read_exif_data(input_file)

    def _read_exif_data(self, input_file):
        command = [
            'exiftool',
            '-s3',
            '-fnumber',
            '-exposuretime',
            '-iso',
            '-focallength',
            '-colorspace',
            '-make',
            '-model',
            '-lensmake',
            '-lensmodel',
            '-lensinfo',
            '-datetimeoriginal',
            '-offsettimeoriginal',
            os.path.abspath(input_file)
        ]

        result = subprocess.run(command, stdout=subprocess.PIPE)
        values = list(map(self._normalize, result.stdout.decode('utf-8').split('\n')))

        self.aperture = 'f/' + values[0] if values[0] else 'f/?'
        self.exposure = values[1] + 's'
        self.iso = int(values[2])
        self.focallength = values[3]
        self.colorspace = values[4]
        self.camera_make = values[5]
        self.camera_model = values[6]
        self.lens_make = values[7]
        self.lens_model = values[8]
        self.lens_info = values[9]
        self.timestamp = datetime.datetime.strptime(values[10] + values[11], "%Y:%m:%d %H:%M:%S%z")
        self.year_month = self.timestamp.astimezone(TIMEZONE).strftime("%Y-%m")


    def _normalize(self, value):
        stripped = value.strip()

        if not stripped:
            return None
        elif stripped == 'undef':
            return None
        elif stripped == '21mm f/?':
            return None
        else:
            return stripped

class PhotoData:
    def __init__(self, input_file, input_file_name, output_file, output_file_name, exif_data):
        self.input_file = input_file
        self.input_file_name = input_file_name
        self.output_file = output_file
        self.output_file_name = output_file_name
        self.alt = None
        self.exif_data = exif_data
        self.additional_gear = []


def read_photos(directory_name, counter):
    directory = os.path.abspath(os.fsencode(directory_name))

    photo_data_list = []

    for input_file in os.listdir(directory):
        input_file_name = os.fsdecode(input_file)

        if input_file_name.startswith(PHOTO_PREFIX) and input_file_name.endswith(PHOTO_SUFFIX):
            counter = counter + 1

            input_file = os.path.join(directory, input_file)
            input_file_name = os.fsdecode(input_file)
            output_file = os.path.join(os.fsencode(ASSET_DIR), os.fsencode(f"{counter:>03}{PHOTO_SUFFIX}"))
            output_file_name = os.fsdecode(output_file)

            photo_data_list.append(PhotoData(
                input_file,
                input_file_name,
                output_file,
                output_file_name,
                ExifData(input_file)))

    photo_data_list.sort(key = lambda pd: pd.exif_data.timestamp, reverse = True)

    return photo_data_list


def prepare_photo(photo_data):
    os.system(f"jpegtran -copy all -progressive -perfect -optimize {photo_data.input_file_name} > {photo_data.output_file_name}")
    os.system(f"exiftool -overwrite_original -all= -tagsFromFile @ -artist={ARTIST} -copyright={ARTIST} -make -model -lensinfo -lensmake -lensmodel -orientation -exposuretime -fnumber -iso -focallength -colorspace {photo_data.output_file_name}")

def write_to_yaml(photo_data_list, target):
    yaml_data = {
        'photos': []
    }

    for photo_data in photo_data_list:
        exif_data = photo_data.exif_data.__dict__
        filtered_exif_data = { k: v for k, v in exif_data.items() if v and k not in SENSITIVE_EXIF_ATTRIBUTES }

        yaml_data['photos'].append({
            'file_path': os.fsdecode(os.path.relpath(photo_data.output_file, DEPLOYMENT_DIR)),
            'alt': photo_data.alt,
            'exif_data': filtered_exif_data
        })

    # print(yaml_data)

    shutil.copyfile(target, os.fsdecode(target) + ".bak")

    with open(target, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False, sort_keys=False)


def main():
    # print(WORKING_DIR)
    # print(ASSET_DIR)
    # print(YAML_FILE)

    try:
        directory_name=sys.argv[1]
    except:
        print('Please pass a directory as 1st parameter')
        sys.exit()

    try:
        counter=int(sys.argv[2])
    except:
        print('No counter set, continuing with 0')
        counter = 0

    photo_data_list = read_photos(directory_name, counter)

    for photo_data in photo_data_list:
        if not photo_data.alt:
            photo_data.alt = input(f"Enter ALT text for {photo_data.input_file}: ")

        prepare_photo(photo_data)

    write_to_yaml(photo_data_list, YAML_FILE)



if __name__=="__main__":
    main()


# TODOs
# - Read photos.yaml to not override ALT and to determine COUNTER automatically
# - Add possibility to hide fotos
