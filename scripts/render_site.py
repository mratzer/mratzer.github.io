#!/usr/bin/env python3

import os
import utils
from collections import defaultdict

WORKING_DIR=os.path.abspath(os.fsencode('./'))
YAML_FILE=os.path.join(WORKING_DIR, os.fsencode('photos.yaml'))
TEMPLATE_DIR=os.path.join(WORKING_DIR, os.fsencode('templates/'))
INDEX_TEMPLATE_FILE=os.path.join(TEMPLATE_DIR, os.fsencode('index.html.template'))
PHOTO_TEMPLATE_FILE=os.path.join(TEMPLATE_DIR, os.fsencode('photo.html.template'))
ALBUM_TEMPLATE_FILE=os.path.join(TEMPLATE_DIR, os.fsencode('album.html.template'))
INDEX_FILE=os.path.join(WORKING_DIR, os.fsencode('_site/index.html'))

class AlbumData:
    def __init__(self, key, name):
        self.key = key
        self.name = name

def render_photo_template(template, dictionary, prefix=''):
    rendered = template

    for key, value in dictionary.items():
        if not value:
            continue

        if prefix:
            actual_key = f"{prefix}.{key}"
        else:
            actual_key = key

#       print(actual_key)

        if isinstance(value, list):
            if actual_key == 'additional_gear':
                rendered = rendered.replace(f"${actual_key}", "<br>" + " + ".join(value))
            elif actual_key != 'albums':
                rendered = rendered.replace(f"${actual_key}", " + " + " + ".join(value))
        elif isinstance(value, dict):
            rendered = render_photo_template(rendered, value, actual_key)
        elif isinstance(value, int):
            rendered = rendered.replace(f"${actual_key}", str(value))
        else:
            rendered = rendered.replace(f"${actual_key}", value)

    return rendered


def get_album_info(photo_data):
    if (not photo_data['albums']):
        return None

    album_info = []

    for album_data in photo_data['albums']:
        album_key = None
        album_name = None
        if isinstance(album_data, dict):
            album_key = next(iter(album_data))
            album_metadata = album_data[album_key]
            if (album_metadata):
                album_name = album_metadata.get('name', None)
        else:
            album_key = album_data
            album_name = None

        album_info.append(AlbumData(album_key, album_name))

    return album_info


def main():
    print("Rendering site ...")

    photo_data_list = utils.read_from_yaml(YAML_FILE)
    index_template = utils.read_file(INDEX_TEMPLATE_FILE)
    photo_template = utils.read_file(PHOTO_TEMPLATE_FILE)
    album_template = utils.read_file(ALBUM_TEMPLATE_FILE)

    rendered_photos = []
    all_album_data = defaultdict(list)

    for photo_data in photo_data_list:
        albums = get_album_info(photo_data)

        if (albums):
            for album in albums:
                if (not all_album_data[album.key]):
                    album_data = {
                        'name': album.name,
                        'photo_data_list': []
                    }

                    all_album_data[album.key] = album_data

                    rendered_album = render_photo_template(album_template, photo_data | {'album': album.__dict__})
                    rendered_album = rendered_album.replace('$additional_gear', '')
                    rendered_photos.append(rendered_album)

                all_album_data[album.key].get('photo_data_list', []).append(photo_data)
        else:
            rendered_photo = render_photo_template(photo_template, photo_data)
            rendered_photo = rendered_photo.replace('$additional_gear', '')
            rendered_photos.append(rendered_photo)

    index = index_template.replace("$photos", "".join(rendered_photos))
    index = index.replace("$header.left.content", "")

#   print(index)

    utils.write_file(INDEX_FILE, index)
    print("Rendered site")

    for album in all_album_data:
        rendered_album_photos = []

        for photo_data in all_album_data[album].get('photo_data_list', []):
            rendered_photo = render_photo_template(photo_template, photo_data)
            rendered_photo = rendered_photo.replace('$additional_gear', '')
            rendered_album_photos.append(rendered_photo)

        rendered_album = index_template.replace("$photos", "".join(rendered_album_photos))
        rendered_album = rendered_album.replace("$header.left.content", '<a href="/" title="back">&#9664;</a>')
        utils.write_file(os.path.join(WORKING_DIR, os.fsencode(f"_site/{album}.html")), rendered_album)
        print(f"Rendered ablum {album}")



if __name__=="__main__":
    main()
