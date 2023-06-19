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
    r"""Returns width (or number of columns) of the instance."""
    list_of_lines = self.as_list_of_lines()
    if list_of_lines:
      len(list_of_lines[0])
    else:
      return 0
    
  def get_height(self):
    r"""Returns width (or number of rows) of the instance."""
    list_of_lines = self.as_list_of_lines()
    return len(list_of_lines)
    
  def as_single_string(self):
    r"""Returns single string representing the instance."""
    return '\n'.join(self.list_of_lines)
    
  def as_list_of_lines(self):
    r"""Returns list of lines representing the instance."""
    return self.list_of_lines
  
  @classmethod
  def from_dict(
      cls,
      dictionary,
      keys_to_print = None,
      print_values_only = False,
      force_width_to = None,
      force_height_to = None,
      align_to_center_instead_of_left = False,
      skip_checks = False):
    r"""
    Produces a StringBox from a dict (frozen in time, meaning not updated
    when dictionary is updated).
    
    Will print the key/value information based on keys_to_print. If it
    is set to None, case in which will print in the alphabetical order
    of the string representation of all the keys. If it is a list, will
    produce the list from those keys. If it is a dict, it will produce
    the desired value of that dict in place of the key.
    
    If print_values_only is False, the resulting line (for each key) will be
    'str(key): str(value)', perhaps with a substitution of str(key) by
    another string if keys_to_print is given as a dict. Otherwise, the
    resulting line is simply 'str(value)'.
    
    All other arguments, that is, force_width_to, force_height_to,
    align_to_center_instead_of_left and skip_checks are passed to the
    initialization method of the correct class.
    """
    if isinstance(keys_to_print, dict):
      pass
    else:
      if keys_to_print is None:
        keys_to_print_as_list = list(dictionary)
        keys_to_print_as_list.sort(key = lambda x: str(x))
      elif isinstance(keys_to_print, (list, tuple)):
        keys_to_print_as_list = list(keys_to_print)
      else:
        raise ValueError('Expect keys_to_print to be a list, a dict, or None')
      keys_to_print = {key: key for key in keys_to_print_as_list}
    list_of_lines = []
    for key in keys_to_print:
      if key not in dictionary:
        raise KeyError('Key not in dictionary')
      value = dictionary[key]
      if not print_values_only:
        line = f'{keys_to_print[key]}: {value}'
      else:
        line = f'{value}'
      list_of_lines.append(line)
    new_instance = cls(
        single_string = None,
        list_of_lines = list_of_lines,
        force_width_to = force_width_to,
        force_height_to = force_height_to,
        align_to_center_instead_of_left = align_to_center_instead_of_left,
        skip_checks = skip_checks)
    return new_instance
    
class CharacterCanvas(StringBox):
  pass
