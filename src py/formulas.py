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
  
  The rule is supplied by a built-in python function (or another callable
  which acts similarly).
  
  The class allows for additional handling operations specified in instantiation.
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
  after the correct variables/arguments are extracted from the dicts
  given as non-keyword or keyword arguments during the call method.
  This Formula (or alternatively its instantiation arguments) and the
  dictionary for correct extraction (or alternatively the appropriate
  argument transforming/processing object) for are given at instantiation.
  """
  
  def __init__(self, dict_for_argument_processing, inner_formula = None,
      inner_function = None, argument_handler = None):
    if inner_formula is None:
      inner_formula = Formula(inner_function, argument_handler)
    self.inner_formula = inner_formula # This might even be None
    # Can give either a DictionaryArgumentProcessor, or a dictionary
    #which conforms to the requirements of DictionaryArgumentProcessor
    if isinstance(dict_for_argument_processing, DictionaryArgumentProcessor):
      self.dict_processor = dict_for_argument_processing
    elif isinstance(dict_for_argument_processing, dict):
      # If a dict is given, then complete_new_arg_with_nones will be False
      self.dict_processor = DictionaryArgumentProcessor(
          dict_for_argument_processing = dict_for_argument_processing,
          complete_new_arg_with_nones = False)
    else:
      raise TypeError('dict_for_argument_processing must be either a dict'\
          'or a DictionaryArgumentProcessor')

  def call(self, *args, **kwargs):
    """Executes the inner formula and therefore the inner function"""
    new_args, new_kwargs = self.dict_processor.process(args, kwargs)
    return self.inner_formula.call(*new_args, **new_kwargs)

class DictionaryArgumentProcessor():
  r"""
  An instance transforms a tuple and a dict into a new tuple and a new dict
  using rules from a specific dictionary given at its initiation.
  
  The tuple and the dict can optionally be interpreted as non-keyword and
  keyword arguments of a function or method call. This interpretation
  motivates the names of the variables: args, kwargs, new_args, new_kwargs,
  on some specification strings, as well as the own class name.
  
  In more detail, the attribute dict_for_argument_processing is a dict
  whose keys are either nonnegative integers (giving rise to an item in a tuple,
  typically interpreted as a non-keyword argument) or strings (giving rise to
  items in a dict, typically interpreted as keyword argument) and whose values
  are length three tuples. The first of these items is either 'arg' or 'kwarg'
  (or any other strings whose first letter is, after lowcasing, 'a' or 'k').
  The second is a nonnegative integer if the first item is 'arg',
  and a string otherwise. The third is always a string.
  
  This is done so that the transform() method, which receives a tuple named
  args and a dict named kwargs, produces a tuple named new_args and
  a dictionary named new_kwargs. A numerical key in dict_for_argument_processing
  determines the item in the corresponding position in a tuple new_args,
  while a string key determines the corresponding key in the dict new_kwargs.
  The value (in the key-value pairs in dict_for_argument_processing)
  determines the value of that item of new_args or new_kwargs: it will be
  either args[value[1]][value[2]] if value[0] is 'arg'
  or kwargs[value[1]][value[2]] if value[0] is 'kwarg'.
  
  The behavior of the formation of new_arg is determined by the Boolean
  attribute complete_new_arg_with_nones. In True, if the numerical keys used
  to derive the items of new_args don't complete a Python range from 0
  to their maximum, then the remaining positions will be filled with None.
  If False, and the numerical keys don't complete a range, an error will
  be raised.
  """
  
  def __init__(dict_for_argument_processing, complete_new_arg_with_nones = False):
    self.dict_for_argument_processing = dict_for_argument_processing
    self.complete_new_arg_with_nones = complete_new_arg_with_nones
    
  def transform(args, kwargs):
    r"""
    Tranforms/processes a tuple and a dict into new ones according to
    rules set out in the dictionary for argument processing.
    """
    # Note: sometimes what is done is called transformation, sometimes processing
    pre_pre_new_args = {} # First do a dictionary, convert to tuple later
    new_kwargs = {}
    for key, value in self.dict_for_argument_processing.items():
      if isinstance(key, int) and key >= 0:
        dict_to_act_on = pre_pre_new_args
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
    # Make pre_pre_new_args into a list then a tuple, potentially addind Nones
    max_index_in_tuple = -1 # Empty tuple
    for key in pre_pre_new_args:
      max_index_in_tuple = max(max_index_in_tuple, key)
    if not complete_new_arg_with_nones:
      if len(pre_pre_new_args) != max_index_in_tuple + 1:
        raise ValueError('Integer keys of dict must form a full range.')
    pre_new_args = []
    for idx in range(max_index_in_tuple):
      if idx in pre_pre_new_args:
        pre_new_args.append(pre_pre_new_args[idx])
      else:
        pre_new_args.append(None)
    new_args = tuple(pre_new_args)
    return (new_args, new_kwargs)
