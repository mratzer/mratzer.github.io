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

def to_absolute_file(directory, filename):
    return os.path.join(directory, os.fsencode(filename))

def to_absolute_path(directory, filename):
    return os.fsdecode(to_absolute_file(directory, filename))

def to_relative_path(directory, file):
    return os.fsdecode(os.path.relpath(file, directory))
