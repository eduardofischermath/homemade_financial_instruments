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

# For implementation of formulas/ an universal formula handler

########################################################################

class Formula():
  r"""
  Object which implements a rule in which objects given as values
  of a dictionary with predetermined keys produce a new object.
  
  The rule is supplied by a built-in python function (or another callable
  which acts similarly), stored as `inner_function` attribute.
  
  The class allows for additional handling operations specified in
  instantiation, via the attribute `argument_handler`. In their absence,
  is not very much different from its inner function.
  """
  
  def __init__(self, inner_function, argument_handler = None):
    self.func = inner_function
    self.argument_handler = argument_handler
  
  def call(self, *posargs, **kwargs):
    """Executes the formula on given arguments, allowing argument handling."""
    if self.argument_handler:
      posargs, kwargs = self.argument_handler(*posargs, **kwargs)
    return self.inner_function(*posargs, **kwargs) # That is, __call__ of it
    
class FormulaOnDicts():
  r"""
  An object implementing a kind of formula/function whose action is based
  on values stored on dicts.
  
  It is done by wrapping over a regular Formula so that, when the
  instance's `call` method is executed, it will be called after the
  correct variables/arguments are extracted using a DictArgumentProcessor
  from the dicts given as positional or keyword arguments.
  
  This Formula (or alternatively its instantiation arguments) and the
  dictionary for correct extraction (or alternatively the appropriate
  argument transforming/processing object) are given at instantiation.
  """
  
  def __init__(self, dict_for_argument_processing, inner_formula = None,
      inner_function = None, argument_handler = None):
    # Formula inside the FormulaOnDicts may be given explicitly
    #or implicitly, in which case it is formed by the given inner_function
    #and argument_handler
    if inner_formula is None:
      inner_formula = Formula(inner_function, argument_handler)
    self.inner_formula = inner_formula # This might even be None
    # Can give either a DictArgumentProcessor instance, or a dict
    #which conforms to the requirements of DictArgumentProcessor
    if isinstance(dict_for_argument_processing, DictArgumentProcessor):
      self.dict_processor = dict_for_argument_processing
    elif isinstance(dict_for_argument_processing, dict):
      # It is fundamental, for the objectives of this class, to set
      #`raise_error_if_not_all_input_items_are_dicts` to True
      self.dict_processor = DictArgumentProcessor(
          dict_for_argument_processing = dict_for_argument_processing,
          raise_error_if_not_all_input_items_are_dicts = True)
    else:
      raise TypeError('dict_for_argument_processing must be either a dict'\
          'or a DictArgumentProcessor')

  def call(self, *posargs, **kwargs):
    """Executes the inner formula and therefore the inner function"""
    new_posargs, new_kwargs = self.dict_processor.process(posargs, kwargs)
    return self.inner_formula.call(*new_posargs, **new_kwargs)

class DictArgumentProcessor():
  r"""
  An instance with a method which transforms a tuple and a dict into a
  new tuple and a new dict using rules from a specific dictionary,
  given at its initiation.
  
  The tuple and the dict can optionally be interpreted as positional and
  keyword arguments of a function or method call. This interpretation
  motivates the names of the variables: names such as `posargs`, `kwargs`,
  `new_posargs`, `new_kwargs` are used for the new and old tuple and dict
  in some methods and on some specification strings, as well as the
  very class name which bears the substring `Argument`.
  
  Very often the items of `posargs` and `kwargs` are dicts. In this case,
  they are expected to be dicts whose keys are nonempty strings. The
  options `raise_error_if_not_all_input_items_are_dicts` and
  `raise_error_if_any_input_items_is_dict` are used to make all or none
  to be treated as dicts.
  
  When the items are dicts, the corresponding keys are read from the
  third item of the corresponding value of `dict_for_argument_processing`.
  When not dicts, that third item should be None.
  
  In more detail, the attribute `dict_for_argument_processing` is a dict
  whose keys are either nonnegative integers (giving rise to an item in a tuple,
  typically interpreted as a positional argument) or strings (giving rise to
  items in a dict, typically interpreted as keyword argument) and whose values
  are length three tuples. The first of these items is either `posarg` or `kwarg`
  (or any other strings whose first letter is, after lowcasing, `p` or `k`).
  The second is a nonnegative integer if the first item is `posarg`,
  and a string otherwise. The third is either a nonempty string or None.
  
  This is done so that the `transform()` method, which receives a tuple
  named `posargs` and a dict named `kwargs`, produces a tuple named
  `new_posargs` and a dictionary named `new_kwargs`. A numerical key in
  `dict_for_argument_processing` determines the item in the corresponding
  position in a tuple `new_posargs`, while a string key determines the
  corresponding key in the dict `new_kwargs`. The value (in the key-value
  pairs in `dict_for_argument_processing`) determines the value of that
  item of `new_posargs` or `new_kwargs`: if value[2] is a nonempty string,
  either posargs[value[1]][value[2]] if value[0] is `posarg` (or simply `p`)
  or kwargs[value[1]][value[2]] if value[0] is `kwarg` (or simply `k`).
  If value[2] is simply None, then the extracted object is instead either
  posargs[value[1]] or kwargs[value[1]] (depending on value[0]).
  
  The behavior of the formation of `new_posargs` is determined by the Boolean
  attribute `complete_new_posargs_with_nones`. In True, if the numerical keys used
  to derive the items of `new_posargs` don't complete a Python range from 0
  to their maximum, then the remaining positions will be filled with None.
  If False, and the numerical keys don't complete a range, an error will
  be raised.
  
  There are options (`raise_error_if_posargs_and_kwargs_coexist` for the
  input of `transform` and `raise_error_if_new_posargs_and_new_kwargs_coexist`
  for its output) to not accept mixed positional and keyword arguments
  (i. e. tuple or dict should be empty).
  
  Another option `raise_error_if_influence_crosses_sides` makes so the
  input dict doesn't interfere with the output tuple and the input tuple
  doesn't interfere with the output dict.
  
  Another option, `raise_error_if_not_all_input_items_are_dicts`, makes
  all items of `posargs` and `kwargs` to be dicts, and thus forces
  `value[2]` in each `(key, value)` of `dict_for_argument_processing`
  to be a nonempty string.
  
  On the other hand, the option `raise_error_if_any_input_items_is_dict`,
  does a similar thing in the opposite direction: `value[2]` should then
  be None, not allowing for direct "read dict key" operations.
  """
  
  def __init__(
      dict_for_argument_processing,
      complete_new_posargs_with_nones = False,
      raise_error_if_posargs_and_kwargs_coexist = False,
      raise_error_if_new_posargs_and_new_kwargs_coexist = False,
      raise_error_if_influence_crosses_sides = False,
      raise_error_if_not_all_input_items_are_dicts = False,
      raise_error_if_any_input_items_is_dict = False):
    # Verify validity of dictionary on initiation, also get error message if any
    is_valid, error_message = self.is_dict_valid_for_processing(
        dict_for_argument_processing,
        complete_new_posargs_with_nones,
        raise_error_if_posargs_and_kwargs_coexist,
        raise_error_if_new_posargs_and_new_kwargs_coexist,
        raise_error_if_influence_crosses_sides,
        raise_error_if_not_all_input_items_are_dicts,
        raise_error_if_any_input_items_is_dict)
    if not is_valid:
      if not error_message:
        error_message = 'Expected a valid dictionary for argument processing.'
      raise ValueError(error_message)
    self.dict_for_argument_processing = dict_for_argument_processing
    self.complete_new_posargs_with_nones = complete_new_posargs_with_nones
    
  def transform(posargs, kwargs):
    r"""
    Tranforms/processes a tuple and a dict into new ones according to
    rules set in the `dict_for_argument_processing` attribute.
    """
    # Note: sometimes what is done is called transformation, sometimes processing
    pre_pre_new_posargs = {} # First do a dictionary, convert to tuple later
    new_kwargs = {}
    for key, value in self.dict_for_argument_processing.items():
      if isinstance(key, int) and key >= 0:
        dict_to_act_on = pre_pre_new_posargs
      elif isinstance(key, str):
        dict_to_act_on = new_kwargs
      else:
        raise TypeError('keys must be either strings or nonnegative integers')
      if value[0].lower().startswith('p'):
        if value[2] is None:
          new_value = posargs[value[1]]
        else:
          new_value = posargs[value[1]][value[2]]
      elif value[0].lower().startswith('k'):
        if value[2] is None:
          new_value = kwargs[value[1]]
        else:
          new_value = kwargs[value[1]][value[2]]
      else:
        raise ValueError('First item of value should start with \'p\' or \'k\'')
      # Raise error if repeated to avoid mysterious behavior
      if key not in dict_to_act_on:
        dict_to_act_on[key] = new_value
      else:
        raise ValueError('Keys cannot be repeated') # Maybe move check to __init__?
    # Make pre_pre_new_posargs into a list then a tuple, potentially adding Nones
    max_index_in_tuple = -1 # Empty tuple
    for key in pre_pre_new_posargs:
      max_index_in_tuple = max(max_index_in_tuple, key)
    if not complete_new_posarg_with_nones:
      if len(pre_pre_new_posargs) != max_index_in_tuple + 1:
        raise ValueError('Integer keys of dict must form a full range.')
    pre_new_posargs = []
    for idx in range(max_index_in_tuple):
      if idx in pre_pre_new_posargs:
        pre_new_posargs.append(pre_pre_new_posargs[idx])
      else:
        pre_new_posargs.append(None)
    new_posargs = tuple(pre_new_posargs)
    return (new_posargs, new_kwargs)
    
  @staticmethod
  def is_dict_valid_for_processing(
      dictionary,
      complete_new_posargs_with_nones,
      raise_error_if_posargs_and_kwargs_coexist,
      raise_error_if_new_posargs_and_new_kwargs_coexist,
      raise_error_if_influence_crosses_sides,
      raise_error_if_not_all_input_items_are_dicts,
      raise_error_if_any_input_items_is_dict):
    """
    Determines whether a given dict is valid for argument processing.
    
    If invalid, returns False and a string giving the error message.
    Otherwise, if valid, returns (True, None).
    
    That is, the items must satisfy the conditions specified in the class
    docstring.
    
    Also, if `complete_new_posargs_with_nones` is False, then the numerical
    keys (if any exist) of `dictionary` must form a complete range
    from 0 to another nonnegative number.
    
    Also, if `raise_error_if_posargs_and_kwargs_coexist`, the input tuple
    and dict (often called `posargs` and `kwargs`) must not be both nonempty.
    And if `raise_error_if_new_posargs_and_new_kwargs_coexist`, the output
    tuple and dict of the `transform` method (often called `new_posargs`
    and `new_kwargs`) must not be both nonempty.
    
    Also, if `raise_error_if_influence_crosses_sides`, then the output
    tuple `new_posargs` depends only on the input tuple `posargs`, while
    the output dict `new_kwargs` depends only on the input dict `kwargs`.
    
    Also, options `raise_error_if_not_all_input_items_are_dicts` and
    `raise_error_if_any_input_items_is_dict` restrict the third items of
    the values of `dictionary` to be, respectively, nonempty strings
    or None.
    """
    was_problem_detected = False
    error_message = None
    if not isinstance(dictionary, dict):
      was_problem_detected = True
      error_message = 'Expected a dictionary'
    else:
      p_and_k = ['p', 'k']
      total_numerical_input_indices_detected = 0
      total_string_input_indices_detected = 0
      max_numerical_output_index_detected = -1 # Works correctly with formula
      total_numerical_output_indices_detected = 0
      total_string_output_indices_detected = 0
      for (key, value) in dictionary.items():
        # First, basic tests
        if not isinstance(key, (str, int)):
          was_problem_detected = True
          error_message = 'Expected key of dict to be a string or an int'
          break
        elif not isinstance(value, tuple) or len(value) != 3:
          was_problem_detected = True
          error_message = 'Expected value of dict to be tuple of length 3'
          break
        elif not isinstance(value[0], str) or (value[0][0].lower() not in p_and_k):
          was_problem_detected = True
          error_message = 'Expected first item of value to start with \'p\' or \'k\''
          break
        elif not isinstance(value[1], (str, int)):
          was_problem_detected = True
          error_message = 'Expected second item of value to be string or an int'
          break
        elif (value[2] is not None) and (not isinstance(value[2], str)):
          was_problem_detected = True
          error_message = 'Expected third item of value to be either a string or None'
          break
        else:
          pass
        # Tests related to key and second item of tuple, also some counting for later
        # The types must match if raise_error_if_influence_crosses_sides
        if isinstance(key, int):
          if key < 0:
            was_problem_detected = True
            error_message = 'Expected key of dict to not be a negative integer'
            break
          elif raise_error_if_influence_crosses_sides and not isinstance(value[1], int):
            was_problem_detected = True
            error_message = 'Expected second item of value to be an int like its key'
            break
          else:
            total_numerical_output_indices_detected += 1
            max_numerical_output_index_detected = max(max_numerical_output_index_detected, value[1])
        else: # Certainly isinstance(key, str) by previous tests
          if not key:
            was_problem_detected = True
            error_message = 'Expected key of dict to not be an empty string'
            break
          elif raise_error_if_influence_crosses_sides and not isinstance(value[1], str):
            was_problem_detected = True
            error_message = 'Expected second item of value to be a string like its key'
            break
          else:
            total_string_output_indices_detected += 1
        # Tests and counting related to second item of tuple
        if isinstance(value[1], int):
          if value[1] < 0:
            was_problem_detected = True
            error_message = 'Expected index to be nonnegative'
            break
          total_numerical_input_indices_detected += 1
        else: # Certainly isinstance(value[1], str) by previous tests
          if not value[1]:
            was_problem_detected = True
            error_message = 'Expected string to be nonempty'
            break
          total_string_input_indices_detected += 1
        # Test related to third item of tuple
        if raise_error_if_not_all_input_items_are_dicts \
            and (not isinstance(value[2], str) or not value[2]):
          was_problem_detected = True
          error_message = 'Expected nonempty string as third item of value'
        elif raise_error_if_any_input_items_is_dict \
            and value[2] is not None:
          was_problem_detected = True
          error_message = 'Expected None as third item of value'
      # Final tests, already out of the loop
      if raise_error_if_posargs_and_kwargs_coexist \
          and total_string_input_indices_detected \
          and total_numerical_input_indices_detected:
        was_problem_detected = True
        error_message = 'Cannot have both nonempty tuple and dict inputs'
      elif raise_error_if_new_posargs_and_new_kwargs_coexist \
          and total_string_output_indices_detected \
          and total_numerical_output_indices_detected:
        was_problem_detected = True
        error_message = 'Cannot have both nonempty tuple and dict outputs' 
      elif not complete_new_posargs_with_nones \
          and max_numerical_output_index_detected + 1 != total_numerical_output_indices_detected:
        was_problem_detected = True
        error_message = 'Expected no gaps in indices for output tuple'
    return (not was_problem_detected, error_message)
