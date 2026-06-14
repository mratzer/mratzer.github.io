#!/usr/bin/env python3

import os
import yaml

def read_from_yaml(source):
    try:
        with open(source, mode='r', encoding='utf-8') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)

            return yaml_data['photos']
    except Exception as e:
        print(e)
        return []

def read_file(source):
    with open(source, mode='r', encoding='utf-8') as file:
        content = file.read()
        file.close()
        return content

def write_file(target, content):
    with open(target, mode='w', encoding='utf-8') as file:
        file.write(content)
        file.close()

def to_absolute_file(directory, filename):
    return os.path.join(directory, os.fsencode(filename))

def to_absolute_path(directory, filename):
    return os.fsdecode(to_absolute_file(directory, filename))

def to_relative_path(directory, file):
    return os.fsdecode(os.path.relpath(file, directory))
