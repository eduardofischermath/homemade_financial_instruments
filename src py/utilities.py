########################################################################
# DOCUMENTATION / README
########################################################################

# File belonging to software/library/package "financial_instruments"
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
  """
  
  def center_string(self, string, length, allow_longer = False):
    r"""
    Centers a string into a specific length.
    
    If allow_longer is True, this acts exactly as str.center, so if the
    string is longer then it will return unaltered. Otherwise, it will
    preserve only the initial characters.
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
