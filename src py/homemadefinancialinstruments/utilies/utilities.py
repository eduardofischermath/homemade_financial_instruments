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

class StringManagement():
  r"""
  Method related to general management of strings.
  
  For example, centering string within a specific length, or removing
  whitespace characters, or splitting and joining according to line breaks.
  
  This class handles such constructions and also some adjacent concepts.
  """
  
  def split_string_by_line_breaks(self, string,
      also_trim_other_nonspace_whitespace = False):
    r"""
    Given a single string, produces a list of lines (the original string
    is cut at the '\n' characters).
    
    If also_trim_other_nonspace_whitespace is True, it will also remove
    the other non-space non-line break whitespaces, that is, the chars
    among '\t', '\r', '\x0b', '\x0c'.
    """
    list_of_strings = string.split('\n')
    if also_trim_other_nonspace_whitespace:
      # Note '\n' is already excluded from each string
      f = lambda x: self.trim_nonspace_whitespace_of_string(
          string = x,
          removing_instead_of_converting = True)
      list_of_strings = list(map(f, list_of_strings))
    else:
      pass
    return list_of_strings
    
  def join_strings_with_line_breaks(self, list_of_strings,
      also_trim_other_nonspace_whitespace = False):
    r"""
    Given a list of strings without line breaks, joins them into a single
    string using the character '\n'.
    
    It will raise an Error if any string has a '\n' character.
    
    If also_trim_other_nonspace_whitespace is True, it will also remove
    the other non-space non-line break whitespaces, that is, the chars
    among '\t', '\r', '\x0b', '\x0c'.
    """
    for string in list_of_strings:
      if '\n' in string:
        raise ValueError('Strings are assumed to not contain line breaks already')
    if also_trim_other_nonspace_whitespace:
      f = lambda x: self.trim_nonspace_whitespace_of_string(
          string = x,
          removing_instead_of_converting = True)
      list_of_strings = list(map(f, list_of_strings))
    single_string = '\n'.join(list_of_strings)
    return single_string
  
  def center_string(self, string, length, allow_longer = False):
    r"""
    Returns a new string of a specific length where the original given
    string appears in the center (or half character to the right,
    if impossible to subdivide equally).
    
    If allow_longer is True, this acts exactly as str.center, so if the
    string is longer then it will return unaltered. Otherwise, if
    allow_longer is False, it will preserve only the initial characters
    of a longer string.
    """
    if not allow_longer and len(string) > length:
      string = string[0:length]
    return string.center(length)

  def trim_nonspace_whitespace_of_string(self, string,
      removing_instead_of_converting = False):
    r"""
    Returns a new string so that any non-space whitespace (that is, characters
    \t, \n, \r, \x0b, \x0c) of the original string is removed. In particular,
    the output is a string without line breaks.
    
    If removing_instead_of_converting is True, those characters are
    removed. If False, they are converted to a regular ASCII space.
    
    Regular ASCII spaces and other non-whitespace chars are not modified.
    """
    list_for_new_string = []
    for char in string:
      if char in '\t\n\r\x0b\x0c':
        if removing_instead_of_converting:
          char_to_add = '' # Not a char but works in the context
        else:
          char_to_add = ' '
      else:
        char_to_add = char
      list_for_new_string.append(char_to_add)
    return ''.join(list_for_new_string)
    
  def trim_nonspace_whitespace_and_center_string(self, string, length,
      allow_longer = False, removing_instead_of_converting = False):
    r"""
    Trims nonspace whitespace removing nonspaces, including line breaks,
    and then centers it, returning the result in a new string.
    
    Methods trim_nonspace_whitespace_of_string and center_string are
    applied sequentially.
    """
    trimmed_string = self.trim_nonspace_whitespace_of_string(
        string = string,
        removing_instead_of_converting = removing_instead_of_converting)
    centered_trimmed_string = self.center_string(
        string = trimmed_string,
        length = length,
        allow_longer = allow_longer)
    return centered_trimmed_string
    
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
      also_print_keys = False, return_as_string = False):
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

class StringBox():
  r"""
  List of lines of same size to be visualized in a pile.
  
  The only attribute is list_of_lines, a list of strings (sometimes
  called lines) of the same size and without line breaks or other
  non-space whitespace characters.
  
  An empty list (width 0, height 0) is allowed, as well as any nonempty
  list of empty strings (width 0, nonzero height).
  """
  
  def __init__(
      self,
      single_string = None,
      list_of_lines = None,
      force_width_to = None,
      force_height_to = None,
      align_to_center_instead_of_left = False,
      skip_checks = False):
    r"""
    Initializes the instance with either a single string (which will be cut
    through any of their line breaks) or a list of lines.
    
    The length of the resulting lines will be uniformized to the maximum
    of the list, unless if force_width_to is set to a number, case in which
    """
    # Create instance of StringManagement class only if needed
    if align_to_center_instead_of_left:
      string_management = StringManagement()
    # Read init arguments, get candidate_list_of_lines
    if single_string is None:
      if list_of_lines is None:
        candidate_list_of_lines = [] # Default value for initiation, thus
      else:
        candidate_list_of_lines = list_of_lines
    else:
      if single_string == '':
        # The default str.split('\n'), when called on the string '',
        #produces the list [''], and not the empty list
        # This might ou might not be expected but it is what it is,
        #and will be manually set to be the correct behavior
        candidate_list_of_lines = ['']
      else:
        candidate_list_of_lines = single_string.split('\n')
      if list_of_lines is not None:
        candidate_list_of_lines = single_string.split('\n')
        if candidate_list_of_lines != list_of_lines:
          raise ValueError('Init info must be given once not twice')
      else:
        candidate_list_of_lines = list_of_lines
    if not skip_checks:
      self.ensure_consistency_of_list_of_lines(candidate_list_of_lines)
    # Now adjust length, height, and maybe center
    if force_height_to is not None:
      # Eliminate the bottom lines
      if len(candidate_list_of_lines) > force_height_to:
        candidate_list_of_lines = candidate_list_of_lines[:force_height_to]
    if force_width_to is None:
      correct_width = max(0, max(len(line) for line in candidate_list_of_lines))
    else:
      correct_width = force_width_to
    correct_list_of_lines = []
    for line in candidate_list_of_lines:
      if len(line) > correct_width:
        # Possible only if force_width_to is set to a number
        correct_line = line[:correct_width]
      else:
        if align_to_center_instead_of_left:
          correct_line = string_management.center_string(
              string = line,
              length = correct_width,
              allow_longer = False)
        else:
          correct_line = line + ' '*(correct_width - len(line))
      correct_list_of_lines.append(correct_line)
    self.list_of_lines = correct_list_of_lines

  @classmethod
  def ensure_consistency_of_list_of_lines(cls, list_of_lines):
    r"""
    Ensures list of lines is a list made of strings of same size and
    without non-space whitespace (only regular ASCII space is allowed,
    while '\t', '\n', '\r', '\x0b' and '\x0c' are forbidden).
    
    Returns None if everything is okay, and otherwise raises an Error.
    """
    if len(list_of_lines) >= 2:
      length_of_first_line = len(list_of_lines[0])
      for line in list_of_lines[1:]:
        if len(line) != length_of_first_line:
          raise ValueError('Not all lines have the same length')
    for line in lines:
      for symbol in '\t\n\r\x0b\x0c':
        if symbol in line:
          raise ValueError('Found non-space whitespace in one of the lines')
    return None
    
  def get_width(self):
    list_of_lines = self.as_list_of_lines()
    if list_of_lines:
      len(list_of_lines[0])
    else:
      return 0
    
  def get_height(self):
    list_of_lines = self.as_list_of_lines()
    return len(list_of_lines)
    
  def as_single_string(self):
    return '\n'.join(self.list_of_lines)
    
  def as_list_of_lines(self):
    return self.list_of_lines
  
  @staticmethod
  def from_dict(dic):
    # Similar to StringBoxManagement.print_dict_into_string_box
    # Maybe move and adapt code as needed
    pass
    
class CharacterCanvas(StringBox):
  pass
