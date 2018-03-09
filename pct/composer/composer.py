# -*- coding: utf-8 -*-

import cv2

class PctComposerError(Exception):
    pass

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

class PctComposer:
    
    def prepare(self):
        messages = []
        warnings = []
        
        response = self._prepare_images()
        messages.extend(response.get_messages())
        warnings.extend(response.get_warnings())
        if not response.get_response():
            return PctComposerResponse(False, messages, warnings)
        
        return PctComposerResponse(True, messages, warnings)
            
    #
    # Private
    #
    
    def __init__(self, images, debug=False):
        self._debug = debug
        self._init_images(images)

    def _init_images(self, images):
        self._images = images