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
  
  def __init__(self, dict_for_argument_processing, inner_formula = None,
      inner_function = None, argument_handler = None):
    if inner_formula is None:
      inner_formula = Formula(inner_function, argument_handler)
    self.inner_formula = inner_formula
    # Can give either the dictionary or the DictionaryArgumentProcessor
    # If a dict is given, then complete_args_with_nones will be False
    if isinstance(dict_for_argument_processing, DictionaryArgumentProcessor):
      self.dict_processor = dict_for_argument_processing
    elif isinstance(dict_for_argument_processing, dict):
      self.dict_processor = DictionaryArgumentProcessor(
          dict_for_argument_processing = dict_for_argument_processing,
          complete_args_with_nones = False)
    else:
      raise TypeError('dict_for_argument_processing must be either a dict'\
          'or a DictionaryArgumentProcessor')

  def call(self, *args, **kwargs):
    """Executes the inner formula and therefore the inner function"""
    new_args, new_kwargs = self.dict_processor.process(args, kwargs)
    return self.inner_formula.call(*new_args, **new_kwargs)

class DictionaryArgumentProcessor():
  r"""
  Transforms non-keyword and keyword arguments into new non-keyword and
  keyword arguments using a specific dictionary given at its initiation.
  
  The transformation is done on a tuple and a dict which are interpreted
  as non-keyword and keyword arguments of a function or method call.
  This interpretation is optional.
  
  In more detail, the attribute dict_for_argument_processing is a dict
  whose keys are either nonnegative integers (giving rise to non-keyword
  arguments) or strings (giving rise to keyword arguments) and whose values
  are length three tuples. The first of these items is either 'arg' or
  'kwarg'. The second is a nonnegative integer if the first item is 'arg',
  and a string otherwise. The third is always a string.
  
  This is done so that the transform method, which receives a tuple named
  args and a dict named kwargs, produces a tuple named new_args and
  a dictionary named new_kwargs. For each key in dict_for_argument_processing,
  there will be a new_value which will be either (here value is the
  corresponding value) args[value[1]][value[2]] if value[0] is 'arg'
  and kwargs[value[1]][value[2]] if value[0] is 'kwargs', and this new_value
  will either join new_args if the key is an nonnegative integer in which
  case new_value will be new_args[key], or join new_kwargs if key is a string,
  in which case new_value will be new_kwargs[key].
  
  The behavior of the formation of new_tuple is determined by the Boolean
  attribute complete_args_with_nones. In True, if the numerical keys used
  to derive the items of new_args don't complete a Python range from 0
  to their maximum, then the remaining positions will be filled with None.
  If False, an error will be raised.
  """
  
  def __init__(dict_for_argument_processing, complete_args_with_nones = False):
    self.dict_for_argument_processing = dict_for_argument_processing
    self.allow_incomplete_tuple = allow_incomplete_tuple
    
  def transform(args, kwargs):
    r"""
    Tranforms/processes a tuple and a dict into new ones according to
    rules set out in the dictionary for argument processing.
    """
    # Note: sometimes what is done is called transformation, sometimes processing
    pre_new_args = {} # First do a dictionary, convert to tuple later
    new_kwargs = {}
    for key, value in self.dict_for_argument_processing.items():
      if isinstance(key, int) and key >= 0:
        dict_to_act_on = pre_new_args
      elif isinstance(key, str):
        dict_to_act_on = new_kwargs
      else:
        raise TypeError('keys must be either strings nonnegative integers')
      if value[0].lower() == 'a':
        new_value = args[value[1]][value[2]]
      elif value[0].lower() == 'k':
        new_value = kwargs[value[1]][value[2]]
      else:
        raise ValueError('First item of value should start with \'a\' or \'k\'')
      # Raise error if repeated to avoid mysterious behavior
      if key not in dict_to_act_on:
        dict_to_act_on[key] = new_value
      else:
        raise ValueError('Keys cannot be repeated') # Maybe move check to __init__?
    # Make pre_new_args into a tuple
    ### WORK HERE ###
    return (new_args, new_kwargs)
