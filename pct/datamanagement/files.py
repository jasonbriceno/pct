# -*- coding: utf-8 -*-

from os import listdir
from os.path import isfile, join

from ..common.configuration import (
    PCT_COMPOSED_IMAGE_FILENAME,
    PCT_COMPOSED_METADATA_FILENAME,
)

def get_input_image_filenames(directory):
    filenames = []
    for f in listdir(directory):
        full_f = join(directory, f)
        if isfile(full_f):
            filenames.append(full_f)
    return filenames

def get_output_image_filename(directory):
    return join(directory, PCT_COMPOSED_IMAGE_FILENAME)

def get_output_metadata_filename(directory):
    return join(directory, PCT_COMPOSED_METADATA_FILENAME)