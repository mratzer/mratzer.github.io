#!/usr/bin/env python3

import datetime
import hashlib
import os
import re
import subprocess
import shutil
import sys
import utils
import yaml
import zoneinfo


PHOTO_PREFIX='DSCF'
PHOTO_SUFFIX='.jpg'
ARTIST='marrat.eu'
WORKING_DIR=os.path.abspath(os.fsencode('./'))
DEPLOYMENT_DIR=os.path.join(WORKING_DIR, os.fsencode('_site'))
ASSET_DIR=os.path.join(DEPLOYMENT_DIR, os.fsencode('assets'))
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
        self.focallength =  values[3] if self.aperture != 'f/?' else '? mm'
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
    def __init__(self, input_file, input_filename, output_file, output_filename, exif_data):
        self.input_file = input_file
        self.input_filename = input_filename
        self.output_file = output_file
        self.output_filename = output_filename
        self.alt = None
        self.exif_data = exif_data
        self.additional_gear = []


def prepare_photos(directory_name):
    directory = os.path.abspath(os.fsencode(directory_name))

    new_photo_data_list = []
    old_photo_data_list = utils.read_from_yaml(YAML_FILE)

    for input_file in os.listdir(directory):
        input_filename = os.fsdecode(input_file)

        if input_filename.startswith(PHOTO_PREFIX) and input_filename.endswith(PHOTO_SUFFIX):
            input_file = os.path.join(directory, input_file)

            new_photo_data = prepare_photo(input_file)
            old_photo_data = get_old_photo_data(old_photo_data_list, new_photo_data.output_file)

            if old_photo_data:
                new_photo_data.alt = old_photo_data['alt']
                new_photo_data.additional_gear = old_photo_data.get('additional_gear', [])

                if not new_photo_data.exif_data.lens_make and old_photo_data['exif_data'].get('lens_make', None):
                    new_photo_data.exif_data.lens_make = old_photo_data['exif_data']['lens_make']
                if not new_photo_data.exif_data.lens_info and old_photo_data['exif_data'].get('lens_info', None):
                    new_photo_data.exif_data.lens_info = old_photo_data['exif_data']['lens_info']

            new_photo_data_list.append(new_photo_data)

    new_photo_data_list.sort(key = lambda pd: pd.exif_data.timestamp, reverse = True)

    return new_photo_data_list


def get_old_photo_data(old_photo_data_list, output_file):
    wanted_file_path = utils.to_relative_path(DEPLOYMENT_DIR, output_file)

    for photo_data in old_photo_data_list:
        if photo_data['file_path'] == wanted_file_path:
            return photo_data

    return None


def prepare_photo(input_file):
    input_filename = os.fsdecode(input_file)

    tmp_file_path = utils.to_absolute_path(WORKING_DIR, f"tmp{PHOTO_SUFFIX}")

    print(f"\tPreparing photo {input_filename}")

    os.system(f"jpegtran -copy all -progressive -perfect -optimize {input_filename} > {tmp_file_path}")
    os.system(f"exiftool -q -q -overwrite_original -all= -tagsFromFile @ -artist={ARTIST} -copyright={ARTIST} -make -model -lensinfo -lensmake -lensmodel -orientation -exposuretime -fnumber -iso -focallength -colorspace {tmp_file_path}")

    output_file = utils.to_absolute_file(ASSET_DIR, f"{sha1sum(tmp_file_path)}{PHOTO_SUFFIX}")
    output_filename = os.fsdecode(output_file)

    os.system(f"mv {tmp_file_path} {output_filename}")

    new_photo_data = PhotoData(
        input_file,
        input_filename,
        output_file,
        output_filename,
        ExifData(input_file))

    print(f"\tPrepared photo {input_filename} -> {utils.to_relative_path(WORKING_DIR, output_file)}")

    return new_photo_data


def sha1sum(file_path):
    # Our photos are small enough to read them as a whole
    with open(file_path, 'rb') as file:
        return hashlib.sha1(file.read()).hexdigest()


def write_to_yaml(photo_data_list, target):
    yaml_data = {
        'photos': []
    }

    for photo_data in photo_data_list:
        exif_data = photo_data.exif_data.__dict__
        filtered_exif_data = { k: v for k, v in exif_data.items() if v and k not in SENSITIVE_EXIF_ATTRIBUTES }

        yaml_data['photos'].append({
            'file_path': utils.to_relative_path(DEPLOYMENT_DIR, photo_data.output_file),
            'alt': photo_data.alt,
            'additional_gear': photo_data.additional_gear,
            'exif_data': filtered_exif_data
        })

#   print(yaml_data)

    if (os.path.isfile(target)):
        shutil.copyfile(target, os.fsdecode(target) + ".bak")

    with open(target, 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False, sort_keys=False)



def main():
    # print(WORKING_DIR)
    # print(ASSET_DIR)
    # print(YAML_FILE)

    print("Preparing photos ...")

    try:
        directory_name=sys.argv[1]
    except:
        print('Please pass a directory as 1st parameter')
        sys.exit()

    photo_data_list = prepare_photos(directory_name)

    for photo_data in photo_data_list:
        if not photo_data.alt:
            photo_data.alt = input(f"Enter ALT text for {photo_data.input_file}: ")

    write_to_yaml(photo_data_list, YAML_FILE)

    print("Prepared photos")



if __name__=="__main__":
    main()
