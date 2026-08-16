#!/usr/bin/env python3

import os
import utils

WORKING_DIR=os.path.abspath(os.fsencode('./'))
YAML_FILE=os.path.join(WORKING_DIR, os.fsencode('photos.yaml'))
TEMPLATE_DIR=os.path.join(WORKING_DIR, os.fsencode('templates/'))
INDEX_TEMPLATE_FILE=os.path.join(TEMPLATE_DIR, os.fsencode('index.html.template'))
PHOTO_TEMPLATE_FILE=os.path.join(TEMPLATE_DIR, os.fsencode('photo.html.template'))
ALBUM_TEMPLATE_FILE=os.path.join(TEMPLATE_DIR, os.fsencode('album.html.template'))
INDEX_FILE=os.path.join(WORKING_DIR, os.fsencode('_site/index.html'))

class AlbumData:
    def __init__(self, key, name, order, cover):
        self.key = key
        self.name = name
        self.order = order
        self.cover = cover
        self.photo_data_list = []

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


def main():
    print("Rendering site ...")

    data = utils.read_from_yaml(YAML_FILE)
    index_template = utils.read_file(INDEX_TEMPLATE_FILE)
    photo_template = utils.read_file(PHOTO_TEMPLATE_FILE)
    album_template = utils.read_file(ALBUM_TEMPLATE_FILE)

    rendered_photos = []
    all_album_data = {}

    for album_data in data['albums']:
        all_album_data[album_data['key']] = AlbumData(
            album_data['key'], 
            album_data['name'], 
            album_data['order'],
            album_data['cover'])

    for photo_data in data['photos']:
        album_keys = photo_data['albums']

        if (album_keys):
            for album_key in album_keys:
                album = all_album_data[album_key]

                if photo_data['file_path'] == album.cover:
                    rendered_album = render_photo_template(album_template, photo_data | {'album': {'key': album.key, 'name': album.name}})
                    rendered_album = rendered_album.replace('$additional_gear', '')
                    rendered_photos.append(rendered_album)

                if album.order == 'asc':
                    album.photo_data_list.insert(0, photo_data)
                else:
                    album.photo_data_list.append(photo_data)
        else:
            rendered_photo = render_photo_template(photo_template, photo_data)
            rendered_photo = rendered_photo.replace('$additional_gear', '')
            rendered_photos.append(rendered_photo)

    index = index_template.replace("$photos", "".join(rendered_photos))
    index = index.replace("$header.left.content", "")

#   print(index)

    utils.write_file(INDEX_FILE, index)
    print("Rendered site")

    for album in all_album_data.values():
        rendered_album_photos = []

        for photo_data in album.photo_data_list:
            rendered_photo = render_photo_template(photo_template, photo_data)
            rendered_photo = rendered_photo.replace('$additional_gear', '')
            rendered_album_photos.append(rendered_photo)

        rendered_album = index_template.replace("$photos", "".join(rendered_album_photos))
        rendered_album = rendered_album.replace("$header.left.content", '<a href="/" title="back">&#9664;</a>')
        utils.write_file(os.path.join(WORKING_DIR, os.fsencode(f"_site/{album.key}.html")), rendered_album)
        print(f"Rendered album {album.key}")



if __name__=="__main__":
    main()
