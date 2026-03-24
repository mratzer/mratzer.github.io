#!/usr/bin/env python3

import os
import yaml

WORKING_DIR=os.path.abspath(os.fsencode('./'))
YAML_FILE=os.path.join(WORKING_DIR, os.fsencode('photos.yaml'))
TEMPLATE_DIR=os.path.join(WORKING_DIR, os.fsencode('templates/'))
INDEX_TEMPLATE_FILE=os.path.join(TEMPLATE_DIR, os.fsencode('index.html.template'))
PHOTO_TEMPLATE_FILE=os.path.join(TEMPLATE_DIR, os.fsencode('photo.html.template'))
INDEX_FILE=os.path.join(WORKING_DIR, os.fsencode('_site/index.html'))


def read_from_yaml(source):
    try:
        with open(source, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

            return yaml_data['photos']
    except:
        return []

def read_file(source):
    with open(source, 'r') as file:
        content = file.read()
        file.close()
        return content

def write_file(target, content):
    with open(target, 'w') as file:
        file.write(content)
        file.close()


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
            else:
                rendered = rendered.replace(f"${actual_key}", " + " + " + ".join(value))
        elif isinstance(value, dict):
            rendered = render_photo_template(rendered, value, actual_key)
        elif isinstance(value, int):
            rendered = rendered.replace(f"${actual_key}", str(value))
        else:
            rendered = rendered.replace(f"${actual_key}", value)

    return rendered


def main():
    photo_data_list = read_from_yaml(YAML_FILE)
    index_template = read_file(INDEX_TEMPLATE_FILE)
    photo_template = read_file(PHOTO_TEMPLATE_FILE)

    rendered_photos = []

    for photo_data in photo_data_list:
        rendered_photo = render_photo_template(photo_template, photo_data)
        rendered_photo = rendered_photo.replace('$additional_gear', '')
        rendered_photos.append(rendered_photo)

    index = index_template.replace("$photos", "".join(rendered_photos))

#   print(index)

    write_file(INDEX_FILE, index)



if __name__=="__main__":
    main()
