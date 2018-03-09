# -*- coding: utf-8 -*-

import cmd

from ..common.configuration import PCT_DEBUG

class AnsiColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'    

class PctInteractor(cmd.Cmd):
    
    #
    # Public
    #
    
    prompt = '> '
    doc_header = """Documented commands (type \help <topic>):"""
    
    def precmd(self, line):
        line = line.strip()
        if not line:
            return ''
        if line[0] == '\\':
            return line[1:]
        return 'say ' + line
        
    def do_d(self, line):
        """
        d
        Toggles the debug state.
        """
        return self.do_debug(line)
        
    def do_debug(self, line):
        """
        debug
        Toggles the debug state.
        """
        if self._debug:
            self._debug = False
            self._output_response('Debug disabled.', False)
            return
        self._debug = True
        self._output_response('Debug enabled.', False)
    
    def do_h(self, line):
        """
        h
        List available commands with "h" or detailed help with "h cmd".
        """
        return self.do_help(line)
        
    def do_q(self, line):
        """
        q
        Quits the Interactor.
        """
        return self.do_quit(line)
    
    def do_quit(self, line):
        """
        quit
        Quits the Interactor.
        """
        return True
        
    def preloop(self):
        self._output_response(
            "WELCOME TO THE PICTIONARY TELEPHONE COMPOSER." +
                "\nTYPE '\\h' FOR HELP.\n",
            False,
        )
        
    def postloop(self):
        self._output_response('SEE YA.', False)

    #
    # Private
    #
    
    _debug = PCT_DEBUG
    
    _output_spacer = '    '

    def _output_debug(self, msg):
        if self._debug and msg:
            self._output_response(msg, False, True)

    def _handle_replies(self, replies):
        response = '\n'.join([reply.get_text() for reply in replies])
        return self._output_response(response)
    
    def _output_response(self, response, debug=False):
        output = '{}{}'.format(
            self._output_spacer,
            response.replace('\n', '\n' + self._output_spacer)
        )
        if debug:
            print(self._color_string(output, AnsiColors.OKGREEN))
        else:
            print(output)

    def _color_string(self, string, color):
        return color + string + AnsiColors.ENDC
    
if __name__ == '__main__':
    PctInteractor().cmdloop()