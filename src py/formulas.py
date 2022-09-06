########################################################################
# DOCUMENTATION / README
########################################################################

# File belonging to software/library/package "financial_instruments"
# Implements financial instruments and solutions for pricing and hedging.

# For more information on functionality, see README.md
# For more information on bugs and planned features, see ISSUES.md
# For more information on versioning, see RELEASES.md

# Copyright (C) 2022 Eduardo Fischer

# This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License version 3
#as published by the Free Software Foundation. See LICENSE.
# Alternatively, see https://www.gnu.org/licenses/.

# This program is distributed in the hope that it will be useful,
#but without any warranty; without even the implied warranty of
#merchantability or fitness for a particular purpose.

########################################################################

# For implementation of formulas/ an universal formula handler

########################################################################

class Formula():
  r"""
  Object which implements a rule in which objects given as values
  of a dictionary with predetermined keys produce a new object.
  
  The rule is supplied by a built-in python function.
  
  The class allows for other handling operations specified in instantiation.
  """
  
  def __init__(self, inner_function, argument_handler = None):
    self.func = inner_function
    self.argument_handler = argument_handler
  
  def call(self, *args, **kwargs):
    """Executes the formula on given arguments, allowing argument handling."""
    if self.argument_handler:
      args, kwargs = self.argument_handler(*args, **kwargs)
    return self.inner_function(*args, **kwargs) # That is, __call__ of it
    
class FormulaOnDictionaries():
  r"""
  An object implementing a kind of formula/function whose action is based
  on values of dictionaries passed as their variables/arguments.
  
  It is done by wrapping over a regular Formula so that it will be called
  after the correct variables/arguments are extracted from the given dicts.
  This Formula (or alternatively its instantiation arguments) and the
  dictionary for correct extraction for are given at instantiation.
  """
  
  def __init__(self, dict_for_argument_extraction, inner_formula = None,
      inner_function = None, argument_handler = None):
    if inner_formula is None:
      inner_formula = Formula(inner_function, argument_handler)
    self.inner_formula = inner_formula
    self.dict_for_argument_extraction = dict_for_argument_extraction

  def call(self, *args, **kwargs):
    ### WORK HERE
    return self.inner_formula.call(**computed_kwargs)
