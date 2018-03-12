# -*- coding: utf-8 -*-

import numpy
import cv2

from os.path import basename

from ..common.configuration import (
    PCT_BORDER_PIXELS,
    PCT_HACK_WINDOW_DELAY,
)
from ..datamanagement.files import (
    get_edited_image_filepath,
)

class PctComposerResponse:

    def get_response(self):
        return self._response
    
    def get_messages(self):
        return self._messages
    
    def get_warnings(self):
        return self._warnings
    
    #
    # Private
    #
    
    def __init__(self, response, messages=[], warnings=[]):
        self._response = response
        self._messages = messages
        self._warnings = warnings

class BaseComposerError(Exception):
    pass

class BaseComposer:
    def __init__(self, message_writer=None, debug_writer=None):
        self._debug = False
        self._message_writer = message_writer
        self._debug_writer = debug_writer
    
    def _log(self, msg):
        if self._message_writer:
            self._message_writer.write(msg)
        
    def _log_debug(self, msg):
        if self._debug_writer and self._debug:
            self._debug_writer.write(msg)

class PctComposerError(BaseComposerError):
    pass

class PctComposer(BaseComposer):
    
    def prepare(self, debug=False):
        self._debug = debug
        self._log_debug('Preparing images...')
        for image_composer in self._get_composers():
            image_composer.prepare(debug)
        self._log_debug('Image preparation complete.')
    
    def compose(self, debug=False):
        self._debug = debug
        self._log_debug('Composing image...')
        if not self._create_composition():
            self._log('No composition could be created.')
            return False
        return True
    
    def refresh_previews(self, width, startx=0, starty=0, margin=0,
                         debug=False):
        self._debug = debug
        self._log_debug('Refreshing previews...')
        x = startx
        y = starty
        for composer in self._get_composers():
            composer.refresh_preview(x, y, width, debug)
            x += width + margin

    def refresh_composition(self, width, startx=0, starty=0, debug=False):
        self._debug = debug
        self._log_debug('Refreshing composition...')
        return self._refresh_composition(width, startx, starty)

    def reindex_image(self, index_in, index_out, debug=False):
        self._debug = debug
        self._log_debug('Swapping images {} and {}'.format(index_in, index_out))
        if self._check_index(index_in) and self._check_index(index_out):
            return self._reindex_image(index_in, index_out)
        return False
    
    def check_index(self, index, debug=False):
        self._debug = debug
        self._log_debug('Checking index {}'.format(index))
        return self._check_index(index)
    
    def rotate(self, index, angle, debug=False):
        self._debug = debug
        self._log_debug('Rotating {} by {}'.format(index, angle))
        if not self._check_index(index):
            self._log('Invalid index.')
            return False
        return self._get_composer(index).rotate(angle, debug)
        
            
    def save(self, filepath, metafile=None, debug=False):
        self._debug = debug
        self._log_debug('Saving {}'.format(filepath))
        
        # Composed
        if not self._save_composed(filepath):
            self._log('Unable to save {}'.format(filepath))
            return False
        
        # Edited
        image_files = self._save_changed_images()
        if not image_files:
            self._log('Unable to save edited image files')
            return False
        
        # Metadata
        if metafile is not None:
            if not self._save_metadata(metafile, image_files, filepath):
                self._log('Unable to save {}'.format(metafile))
                return False
            
        return True
            
    #
    # Private
    #
    
    def __init__(self, image_files, message_writer=None, debug_writer=None):
        super(PctComposer, self).__init__(message_writer, debug_writer)
        self._init_image_composers(image_files)
        
        self._composition = None
        self._window = None

    def _init_image_composers(self, image_files):
        self._indexed_images = {}
        self._image_composers = {}
        for index, image in enumerate(image_files):
            self._indexed_images[index] = image
            self._image_composers[image] =  ImgComposer(
                image,
                self._message_writer,
                self._debug_writer,
            )
        return self._image_composers

    def _init_window(self, name=None):
        if self._window is not None:
            cv2.destroyWindow(self._window)
        if name is not None:
            self._window = name
        else:
            self._window = ' + '.join(
                [c.get_window() for c in self._get_composers()]
            )
        cv2.namedWindow(self._window)
        
    def _check_index(self, index):
        if index in self._indexed_images:
            return True
        return False

    def _get_composer(self, index):
        return self._image_composers[self._indexed_images[index]]
        
    def _get_composers(self, ordered=True):
        indices = list(self._indexed_images.keys())
        if ordered:
            indices.sort()
        composers = []
        for index in indices:
            composers.append(
                self._image_composers[self._indexed_images[index]]
            )
        return composers
    
    def _reindex_image(self, index_in, index_out):
        temp = self._indexed_images[index_in]
        self._indexed_images[index_in] = self._indexed_images[index_out]
        self._indexed_images[index_out] = temp
        return True
    
    def _create_composition(self):
        images = [c.get_image() for c in self._get_composers()]
        min_height = min([img.shape[0] for img in images])
        self._composition = compose_images(images, min_height)
        return True
    
    def _refresh_composition(self, width, x=0, y=0):
        self._init_window()
        preview = resize_image_width(self._composition, width)
        self._show_image(preview, x, y)
    
    def _show_image(self, image, x=0, y=0):
        cv2.imshow(self._window, image)
        cv2.moveWindow(self._window, x, y)
        cv2.waitKey(PCT_HACK_WINDOW_DELAY)
    
    def _save_changed_images(self):
        filepaths = []
        for composer in self._get_composers():
            filepaths.append(composer.save(self._debug))
        return filepaths
    
    def _save_composed(self, filepath):
        cv2.imwrite(filepath, self._composition)
        return True
    
    def _save_metadata(self, filepath, image_files, composed_file):
        fp = open(filepath, 'w')
        fp.write(composed_file + '\n')
        for f in image_files:
            fp.write(f + '\n')
        fp.close()
        return True
    
class ImgComposerError(BaseComposerError):
    pass

class ImgComposer(BaseComposer):
    
    def prepare(self, debug=False):
        self._debug = debug
        self._log('Preparing {}'.format(self._image_file))
        self._prepare_image()
        self._prepare_window()
    
    def refresh_preview(self, x, y, width, debug=False):
        self._debug = debug
        preview = resize_image_width(self._current_image(), width)
        self._show_image(preview, x, y)
    
    def get_image(self):
        return self._current_image().copy()
    
    def get_window(self):
        return self._window
    
    def rotate(self, angle, debug=False):
        self._debug = debug
        self._log_debug('Rotating {}'.format(self._image_file))
        self._rotate(angle)
        
    def save(self, debug=False):
        self._debug = debug
        self._log_debug('Saving edited {}'.format(self._image_file))
        filepath = self._get_save_filepath()
        if self._save(filepath):
            return filepath
        return None
    
    #
    # Private
    #
    
    def __init__(self, image_file, message_writer=None, debug_writer=None):
        super(ImgComposer, self).__init__(message_writer, debug_writer)
        self._image_file = image_file
        self._images = []
        self._window = None
    
    def _add_image(self, image):
        self._images.append(image)
    
    def _current_image(self):
        if len(self._images) < 1:
            return None
        return self._images[-1]
    
    def _pop_image(self):
        if len(self._images) < 2:
            return None
        return self._images.pop()
    
    def _prepare_image(self):
        self._log_debug('Preparing image {}'.format(self._image_file))
        self._add_image(cv2.imread(self._image_file))
        
    def _prepare_window(self):
        self._log_debug('Preparing window for {}'.format(self._image_file))
        self._window = basename(self._image_file)
        cv2.namedWindow(self._window)
    
    def _show_image(self, image=None, x=0, y=0):
        self._log_debug('Showing image {}'.format(self._image_file))
        if image is None:
            cv2.imshow(self._window, self._current_image())
        else:
            cv2.imshow(self._window, image)
        cv2.moveWindow(self._window, x, y)
        cv2.waitKey(PCT_HACK_WINDOW_DELAY)

    def _get_save_filepath(self):
        return get_edited_image_filepath(self._image_file)
    
    def _rotate(self, angle):
        rotated = rotate_image(self._current_image(), angle)
        self._add_image(rotated)

    def _save(self, filepath=None):
        cv2.imwrite(filepath, self._current_image())
        return True
    
def resize_image_width(image, width):
    current_width = image.shape[1]
    if width == current_width:
        return image.copy()
    
    current_height = image.shape[0]
    height = (width * current_height) // current_width
    
    if width < current_width:
        interp = cv2.INTER_AREA
    else:
        interp = cv2.INTER_LINEAR
    return cv2.resize(image, (width, height), interpolation=interp)

def resize_image_height(image, height):
    current_height = image.shape[0]
    if height == current_height:
        return image.copy()
    
    current_width = image.shape[1]
    width = (height * current_width) // current_height
    
    if height < current_height:
        interp = cv2.INTER_AREA
    else:
        interp = cv2.INTER_LINEAR
    return cv2.resize(image, (width, height), interpolation=interp)

def rotate_image(image, angle):
    rows, cols, _ = image.shape
    M = cv2.getRotationMatrix2D((cols // 2, rows // 2), -angle, 1)
    return cv2.warpAffine(image, M, (cols,rows))

def add_image_border(image, noleft=False):
    if noleft:
        left_pixels = 0
    else:
        left_pixels = PCT_BORDER_PIXELS
    return cv2.copyMakeBorder(
        image,
        PCT_BORDER_PIXELS,
        PCT_BORDER_PIXELS,
        left_pixels,
        PCT_BORDER_PIXELS,
        cv2.BORDER_CONSTANT,
    )

def compose_images(images, height):
    resized_images = [resize_image_height(img, height) for img in images]
    
    # Image borders are a little hacky
    bordered_images = []
    for index, img in enumerate(resized_images):
        if index == 0:
            bordered_images.append(add_image_border(img))
        else:
            bordered_images.append(add_image_border(img, True))
            
    return numpy.concatenate(bordered_images, axis=1)