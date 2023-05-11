########################################################################
# DOCUMENTATION / README
########################################################################

# File belonging to software package "homemade_financial_instruments"
# Implements financial instruments and solutions for pricing and hedging.

# For more information on functionality, see README.md
# For more information on bugs and planned features, see ISSUES.md
# For more information on versioning, see RELEASES.md

# Copyright (C) 2023 Eduardo Fischer

# This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License version 3
#as published by the Free Software Foundation. See LICENSE.
# Alternatively, see https://www.gnu.org/licenses/.

# This program is distributed in the hope that it will be useful,
#but without any warranty; without even the implied warranty of
#merchantability or fitness for a particular purpose.

########################################################################

# In this file we define generic utilities: classes, methods and functions
#which don't fit any particular category

########################################################################

class StringBoxManagement():
  r"""
  Method related to general management of string boxes.
  
  A string box, or character box, is understood as a rectangle of chars,
  typically written as a list of lines of chars with same length, or
  the same chars but with the newline character.
  
  This class handles such constructions and also some adjacent concepts.
  """
  
  def center_string(self, string, length, allow_longer = False):
    r"""
    Centers a string into a specific length.
    
    If allow_longer is True, this acts exactly as str.center, so if the
    string is longer then it will return unaltered. Otherwise, if
    allow_longer is Falsen, it will preserve only the initial characters
    of a longer string.
    """
    if not allow_longer and len(string) > length:
      string = string[0:length]
    return string.center()

  def trim_to_single_line_string(self, string):
    r"""
    Modifies a string to that any non-space whitespace (that is, characters
    \t, \n, \r, \x0b, \x0c) is converted to an ASCII space.
    """
    list_for_new_string = []
    for char in string:
      if char in '\t\n\r\x0b\x0c':
        char_to_add = ' '
      else:
        char_to_add = char
      list_for_new_string.append(char_to_add)
    return ''.join(list_for_new_string)
    
  def trim_to_single_line_and_center_string(self, string, length,
      allow_longer = False):
    r"""
    Trims string to single line, then centers it.
    
    Methods trim_to_single_line_string and center_string are applied
    sequentially.
    """
    trimmed_string = self.trim_to_single_line_string(string)
    return self.center_string(trimmed_string, length, allow_longer)
    
  def print_dict_into_lines(self, dictionary, keys_to_print = None,
      also_print_keys = False, return_as_string = False):
    r"""
    Given a dictionary an a list of keys_to_print, produces a list of
    strings for the values corresponding to the keys. (It is returned,
    not printed, despite the method's name.)

    If keys_to_print is None, it will take all dict keys in alphabetical
    order.
    
    If also_print_keys is True, the resulting string will be
    'str(key):str(value)'. Otherwise, it is simply 'str(value)'
    
    If return_as_string is True, it instead performs a joint of the lines
    into a single string with separator '\n'.
    """
    if keys_to_print is None:
      keys_to_print = list(dictionary)
      keys_to_print.sort(key = lambda x: str(x))
    list_of_lines = []
    for key in keys_to_print:
      if key not in dictionary:
        raise KeyError('Key not in dictionary')
      value = dictionary[key]
      if also_print_keys:
        line = f'{key}:{value}'
      else:
        line = f'{value}'
      list_of_lines.append(line)
    if return_as_string:
      return '\n'.join(list_of_lines)
    else:
      return list_of_lines

  def print_dict_into_lines_then_trim_and_center(self, dictionary, 
      length, keys_to_print = None, also_print_keys = False,
      return_as_string = False, allow_longer = False):
    r"""
    Obtains lines from values from a dict, then trims and centers.
    
    Methods print_dict_into_lines, trim_to_single_line_string and
    center_string are applied sequentially using the given arguments.
    """
    lines = self.print_dict_into_lines(
        dictionary = dictionary,
        keys_to_print = keys_to_print,
        also_print_keys = also_print_keys,
        return_as_string = False)
    trimmed_lines = []
    for line in lines:
      trimmed_and_centered_line = self.trim_to_single_line_and_center_string(
          line, length, allow_longer)
      trimmed_and_centered_lines.append(trimmed_line)
    if return_as_string:
      return '\n'.join(trimmed_lines)
    else:
      return trimmed_lines
      
  def print_dict_into_string_box(self, dictionary, keys_to_print = None,
      also_print_keys = False, return_as_string = False)
    r"""
    Produces smallest string box fitting values from a dict.
    
    This is equivalent to calling print_dict_into_lines_then_trim_and_center
    with the maximum length.
    """
    lines = self.print_dict_into_lines(
        dictionary = dictionary,
        keys_to_print = keys_to_print,
        also_print_keys = also_print_keys,
        return_as_string = False)
    max_length = max(len(line) for line in lines)
    return self.print_dict_into_lines_then_trim_and_center(
        dictionary = dictionary,
        length = max_length,
        keys_to_print = keys_to_print,
        also_print_keys = also_print_keys,
        return_as_string = return_as_string,
        allow_longer = False)
        
