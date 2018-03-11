# -*- coding: utf-8 -*-

import cv2

from os.path import basename

from ..common.configuration import (
    PCT_WINDOW_HACK,
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
        for image_composer in self._image_composers.values():
            image_composer.prepare(debug)
        self._log_debug('Image preparation complete.')
    
    def compose(self, debug=False):
        self._debug = debug
        self._log_debug('Composing image...')
        self._composition = self._get_image(0)
    
    def refresh_previews(self, width, height, startx=0, starty=0, margin=0,
                         debug=False):
        self._debug = debug
        self._log_debug('Refreshing previews...')
        x = startx
        y = starty
        for image in self._indexed_images.values():
            self._image_composers[image].refresh_preview(x, y, width, height, debug)
            x += width + margin

    def refresh_composition(self, width, startx=0, starty=0, debug=False):
        self._debug = debug
        self._log_debug('Refreshing composition...')
        if self._composition is None:
            self._log_debug('No compotion exists.')
            return False
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

    def _init_window(self, name):
        if self._window is not None:
            cv2.destroyWindow(self._window)
        self._window = name
        cv2.namedWindow(self._window)
        
    def _check_index(self, index):
        if index in self._indexed_images:
            return True
        return False

    def _get_image(self, index):
        return self._image_composers[self._indexed_images[index]].get_image()
    
    def _reindex_image(self, index_in, index_out):
        temp = self._indexed_images[index_in]
        self._indexed_images[index_in] = self._indexed_images[index_out]
        self._indexed_images[index_out] = temp
        return True
    
    def _refresh_composition(self, width, x=0, y=0):
        self._log_debug('Refreshing composition...')
        self._init_window('COMPOSITION')
        cv2.imshow(self._window, self._composition)
        cv2.moveWindow(self._window, x, y)
        cv2.waitKey(PCT_WINDOW_HACK)
        
class ImgComposerError(BaseComposerError):
    pass

class ImgComposer(BaseComposer):
    
    def prepare(self, debug=False):
        self._debug = debug
        self._log('Preparing {}'.format(self._image_file))
        self._prepare_image()
        self._prepare_window()
    
    def refresh_preview(self, x, y, width, height, debug=False):
        self._debug = debug
        self._log_debug(str(self._image.shape))
        self._preview = cv2.resize(
            self._image,
            (width, height),
            interpolation=cv2.INTER_AREA,
        )
        self._log_debug(str(self._preview.shape))
        self._show_image(self._preview, x, y)
    
    def get_image(self):
        return self._image
    
    def get_window_name(self):
        return self._window
    
    #
    # Private
    #
    
    def __init__(self, image_file, message_writer=None, debug_writer=None):
        super(ImgComposer, self).__init__(message_writer, debug_writer)
        self._image_file = image_file
        self._image = None
        self._window = None
        
    def _prepare_image(self):
        self._log_debug('Preparing image {}'.format(self._image_file))
        self._image = cv2.imread(self._image_file, cv2.IMREAD_GRAYSCALE)
        
    def _prepare_window(self):
        self._log_debug('Preparing window for {}'.format(self._image_file))
        self._window = basename(self._image_file)
        cv2.namedWindow(self._window)
    
    def _show_image(self, image=None, x=0, y=0):
        self._log_debug('Showing image {}'.format(self._image_file))
        if image is None:
            cv2.imshow(self._window, self._image)
        else:
            cv2.imshow(self._window, image)
        cv2.moveWindow(self._window, x, y)
        cv2.waitKey(PCT_WINDOW_HACK)