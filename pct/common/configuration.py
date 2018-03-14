# -*- coding: utf-8 -*-

"""
A global configuration file for the library.
"""

# Debugging and testing
PCT_DEFAULT_DEBUG = True
PCT_TEST_DIR = '/Users/jasonbriceno/Pictures/Edited/Pictionary Telephone/Game Night 2018/cheating'

# Image Files
PCT_IMAGE_EXTENSIONS = ['jpg', 'png']

# Preview Settings
PCT_PREVIEW_START_X = 1500
PCT_PREVIEW_START_Y = -200
PCT_PREVIEW_MARGIN = 5
PCT_PREVIEW_WIDTH = 337
PCT_PREVIEW_HEIGHT = 253

# Edit Settings
PCT_DEFAULT_AUTOMAGIC = True
PCT_DEFAULT_ROTATION = 5
PCT_DEFAULT_FIT = 25
PCT_FIT_BUFFER = 25

# Composition Settings
PCT_COMPOSITION_START_X = 1500
PCT_COMPOSITION_START_Y = 300
PCT_COMPOSITION_WIDTH = 1800
PCT_BORDER_PIXELS = 50

PCT_HACK_WINDOW_DELAY = 10

# Composition files
PCT_PREFIX = '_pct_'
PCT_EDITED_IMAGE_PREFIX = PCT_PREFIX + 'edit_'
PCT_COMPOSED_IMAGE_FILENAME = PCT_PREFIX + 'composed.jpg'
PCT_COMPOSED_METADATA_FILENAME = PCT_PREFIX + 'metadata.txt'