# -*- coding: utf-8 -*-

import cmd

from sys import stdout

from ..datamanagement.files import get_input_image_filenames

from ..common.configuration import (
    PCT_DEBUG,
    PCT_TEST_DIR,
    
    PCT_PREVIEW_START_X,
    PCT_PREVIEW_START_Y,
    PCT_PREVIEW_MARGIN,
    PCT_PREVIEW_WIDTH,
    PCT_PREVIEW_HEIGHT,
    
    PCT_COMPOSITION_START_X,
    PCT_COMPOSITION_START_Y,
    PCT_COMPOSITION_WIDTH,
)
from ..composer.composer import (
    PctComposer,
    PctComposerError,
)

class AnsiColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'    

class PctInteractorWriter:
    
    def write(self, string):
        if not string:
            return
        
        output = '{}{}'.format(
            self._prefix,
            string.replace('\n', '\n' + self._prefix)
        )
        stdout.write(self._color_string(output))
        stdout.write('\n')
        
    def __init__(self, prefix='', color=None):
        self._prefix = prefix
        self._color = color
    
    def _color_string(self, string):
        if self._color is None:
            return string
        return self._color + string + AnsiColors.ENDC
        
class PctInteractor(cmd.Cmd):
    
    #
    # Public
    #
    
    def precmd(self, line):
        if not line:
            return ''
        return line.strip()
    
    def do_c(self, line):
        return self.do_compose(line)
    
    def do_compose(self, line):
        """
        compose
        Composes the images into a single image.
        """
        self._compose_images()
        self._refresh_composition()
        
    def do_debug(self, line):
        """
        debug
        Toggles the debug state.
        """
        if self._debug:
            self._debug = False
            self._output_response('Debug disabled.')
            return
        self._debug = True
        self._output_response('Debug enabled.')
    
    def do_i(self, line):
        """
        i
        Sets the current working image.
        """
        return self.do_image(line)
    
    def do_image(self, line):
        """
        image
        Sets the current working image.
        """
        if not self._set_working_image(line):
            self._output_response('{}: Invalid image index'.format(line))
    
    def do_index(self, line):
        """
        image
        Sets the current working image.
        """
        if not self._reindex_image(line):
            self._output_response('{}: Invalid image indices'.format(line))
            return
        self._refresh_images()
            
    def do_load(self, line):
        """
        load
        Loads a directory for processing.
        """
        self._output_response('Loading ' + line)
        try:
            filenames = get_input_image_filenames(PCT_TEST_DIR)
        except FileNotFoundError:
            self._output_response('Directory does not exist.')
            return
        
        self._init_composer(sorted(filenames))
        self._refresh_images()
        
    def do_quit(self, line):
        """
        quit
        Quits the Interactor.
        """
        return True
        
    def preloop(self):
        self._output_response('Welcome to the Pictionary Telephone composer.')
        self._output_response("Type 'help' for more info.")
        
        if self._debug:
            self._output_response()
            self._output_response('Debug enabled.')
            
        self._output_response()
        
    def postloop(self):
        self._output_response('See ya.', False)

    #
    # Private
    #

    def __init__(self):
        super(PctInteractor, self).__init__()
        
        self._debug = PCT_DEBUG
        
        self._init_writers('    ')
        self._output_spacer = '    '
        self.doc_header = """Documented commands (type help <topic>):"""
        self._working_image = None
        self._set_prompt()
        
    def _init_writers(self, spacer):
        self._message_writer = PctInteractorWriter(spacer)
        self._debug_writer = PctInteractorWriter(spacer, AnsiColors.OKGREEN)
        
    def _output_debug(self, msg):
        if self._debug and msg:
            self._output_response(msg, False)

    def _handle_replies(self, replies):
        response = '\n'.join([reply.get_text() for reply in replies])
        return self._output_response(response)
    
    def _output_response(self, response='', debug=False):
        if debug:
            self._debug_writer.write(response)
        else:
            self._message_writer.write(response)
   
    def _init_composer(self, filenames):
        self._composer = PctComposer(
            filenames,
            self._message_writer,
            self._debug_writer,
        )
        self._composer.prepare(self._debug)
    
    def _set_prompt(self):
        if self._working_image is None:
            self.prompt = '> '
        else:
            self.prompt = 'image {}> '.format(self._working_image)

    def _refresh_images(self):
        self._composer.refresh_previews(
            PCT_PREVIEW_WIDTH,
            PCT_PREVIEW_HEIGHT,
            PCT_PREVIEW_START_X,
            PCT_PREVIEW_START_Y,
            PCT_PREVIEW_MARGIN,
            self._debug,
        )
    
    def _set_working_image(self, line):
        try:
            index = int(line)
        except Exception:
            return False
        
        if self._composer.check_index(index):
            self._working_image = index
            self._set_prompt()
            return True
        return False
            
    def _reindex_image(self, line):
        tokens = line.split()
        if len(tokens) != 2:
            return False
        
        try:
            index0 = int(tokens[0])
            index1 = int(tokens[1])
        except Exception:
            return False
        
        return self._composer.reindex_image(index0, index1)
    
    def _compose_images(self):
        return self._composer.compose(self._debug)
    
    def _refresh_composition(self):
        self._composer.refresh_composition(
            PCT_COMPOSITION_WIDTH,
            PCT_COMPOSITION_START_X,
            PCT_COMPOSITION_START_Y,
            self._debug,
        )
    
if __name__ == '__main__':
    PctInteractor().cmdloop()