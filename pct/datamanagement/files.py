# -*- coding: utf-8 -*-

from fnmatch import fnmatch

from os import (
    path,
    listdir,
)

from ..common.configuration import (
    PCT_IMAGE_EXTENSIONS,
    PCT_PREFIX,
    PCT_EDITED_IMAGE_PREFIX,
    PCT_COMPOSED_IMAGE_FILENAME,
    PCT_COMPOSED_METADATA_FILENAME,
)

def is_pct(filename):
    return fnmatch(filename, '{}*'.format(PCT_PREFIX))

def is_image(filename):
    for extension in PCT_IMAGE_EXTENSIONS:
        if fnmatch(filename, '*.{}'.format(extension)):
            return True
    return False

def get_input_image_filepaths(directory):
    filepaths = []
    for f in listdir(directory):
        if is_image(f) and not is_pct(f):
            full_f = path.join(directory, f)
            if path.isfile(full_f):
                filepaths.append(full_f)
    return filepaths

def get_output_image_filepath(directory):
    return path.join(directory, PCT_COMPOSED_IMAGE_FILENAME)

def get_output_metadata_filepath(directory):
    return path.join(directory, PCT_COMPOSED_METADATA_FILENAME)

def get_edited_image_filepath(filepath):
    directory, filename = path.split(filepath)
    return path.join(
        directory,
        PCT_EDITED_IMAGE_PREFIX + filename
    )