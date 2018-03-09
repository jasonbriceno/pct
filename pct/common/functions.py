# -*- coding: utf-8 -*-

def invert_dictionary(dictionary):
    return {v:k for k, v in dictionary.items()}

def capitalize_first(string):
    return string[:1].upper() + string[1:]