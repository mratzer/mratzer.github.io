#!/usr/bin/env python3

import os
import yaml

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

def to_absolute_file(directory, file_name):
    return os.path.join(directory, os.fsencode(file_name))

def to_absolute_path(directory, file_name):
    return os.fsdecode(to_absolute_file(directory, file_name))

def to_relative_path(directory, file_path):
    return os.fsdecode(os.path.relpath(file_path, directory))
