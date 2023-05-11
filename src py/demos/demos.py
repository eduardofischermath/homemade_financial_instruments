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

# Functions which showcase the capabilities of this program/library
#with interactive user input on flagship functions
# (This should contain the only imperative Python code!!)

########################################################################

# Not the best importing mechanisms but fine for the time being
from sys import version_info as sys_version_info
from trees import *
from worlds import *
from assets import *

# So in this file the input works well from both Python 2 and Python 3
if sys_version_info.major == 2:
  best_input = raw_input
elif sys_version_info.major == 3:
  best_input = input
else:
  raise ValueError('Only works with Python 2 and 3.')

def detect_initial(string, desired_first_letter, be_case_sensitive = False,
    desired_return_if_empty_string = False):
  """Detects whether the first letter of a string is the desired one."""
  if string:
    if be_case_sensitive:
      is_desired = string[0] == desired_first_letter
    else:
      is_desired = string[0].lower() == desired_first_letter.lower()
    return is_desired
  else:
    return desired_return_if_empty_string

def capture_purify_ehxibit_input(message, type_to_convert_to = None,
    pre_conversion_purifying_formula = None, post_conversion_purifying_formula = None,
    public_variable_name = None, request_exhibition = False):
  r"""
  Takes a raw input and makes it into the desirable type, returning it.
  
  Can make it go through formulas ("purification"), can also show it to the user.
  """
  input_string = best_input(message)
  if pre_conversion_purifying_formula:
    input_string = pre_conversion_purifying_formula(input_string)
  if type_to_convert_to:
    input_object = type_to_convert_to(input_string)
  if post_conversion_purifying_formula:
    input_object = post_conversion_purifying_formula(input_object)
  if request_exhibition:
    if public_variable_name is None:
      string_before_object = ''
    else:
      string_before_object = f'{public_variable_name}: '
    print(string_before_object + str(input_object))
  return input_object

def all_demos():
  """Provides envelope for all demonstration functions."""
  should_keep_going = True
  while should_keep_going:
    evaluate_vanilla_option_using_binary_tree_demo()
    should_keep_going = capture_purify_ehxibit_input(
        message = 'Wish to continue? [Y]es or [N]o. (Default: No)\n',
        type_to_convert_to = bool,
        pre_conversion_purifying_formula = lambda s: detect_initial(s, 'y'),
        post_conversion_purifying_formula = None,
        public_variable_name = None,
        request_exhibition = False)

def evaluate_vanilla_option_using_binary_tree_demo():
  """Computes value of vanilla option with user-provided information"""
  print('This evaluates a vanilla option on an asset whose progress is\
      tracked by a binary tree.')
  # First collect all information
  list_of_args = []
  list_of_args.append({
      'message': 'Which kind of option? [C]all or [P]ut option? (Default: Call)\n',
      'type_to_convert_to': bool,
      'pre_conversion_purifying_formula': lambda s: detect_initial(s, 'p'),
      'public_variable_name': 'is_put_instead_of_call',
      'request_exhibition': True})
  list_of_args.append({
      'message': 'Which kind of option? [European] or [A]merican? (Default: European)\n',
      'type_to_convert_to': bool,
      'pre_conversion_purifying_formula': lambda s: detect_initial(s, 'a'),
      'public_variable_name': 'is_american_instead_of_european',
      'request_exhibition': True})
  list_of_args.append({
      'message': 'Enter [annual, continuous] interest rate (as a number). Also known as short rate.\n\
          (Default: 0.05 which is equivalent to 5%)\n',
      'type_to_convert_to': float,
      'pre_conversion_purifying_formula': None,
      'public_variable_name': 'annual_continuous_interest_rate',
      'request_exhibition': True})
  list_of_args.append({
      'message': 'Enter relevant time unit for step of binary tree: [Y]ear, [M]onth or [D]ay. (Default: Month)\n',
      'type_to_convert_to': str,
      'pre_conversion_purifying_formula': lambda s: s[0].lower() if s else 'm',
      'public_variable_name': 'time_unit_for_step',
      'request_exhibition': True})
  list_of_args.append({
      'message': 'Enter duration of a single step in previous time unit. (Default: 1)\n',
      'type_to_convert_to': float,
      'pre_conversion_purifying_formula': None,
      'public_variable_name': 'duration_of_single_step',
      'request_exhibition': True})
  list_of_args.append({
      'message': 'Enter number of steps in binary tree. (Default: 4)\n',
      'type_to_convert_to': int,
      'pre_conversion_purifying_formula': None,
      'public_variable_name': 'number_of_steps',
      'request_exhibition': True})
  list_of_args.append({
      'message': 'Enter initial value of base asset. (Default: 100)\n',
      'type_to_convert_to': float,
      'pre_conversion_purifying_formula': None,
      'public_variable_name': 'initial_value',
      'request_exhibition': True})
  list_of_args.append({
      'message': 'Enter number of steps in binary tree. (Default: 10)\n',
      'type_to_convert_to': float,
      'pre_conversion_purifying_formula': None,
      'public_variable_name': 'number_of_steps',
      'request_exhibition': True})
  # Call relevant function and print it
  print('')
  return None # Imperative

if __name__ == '__main__':
  all_demos()
