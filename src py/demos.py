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
    evaluate_vanilla_option_using_binary_tree_demo
    should_keep_going = capture_purify_ehxibit_input(
        message = 'Wish to continue? [Y]es or [N]o.\n',
        type_to_convert_to = bool,
        pre_conversion_purifying_formula = lambda s: detect_initial(s, 'y'),
        post_conversion_purifying_formula = None,
        public_variable_name = None,
        request_exhibition = False)

def evaluate_vanilla_option_using_binary_tree_demo():
  """Computes value of vanilla option with user-provided information"""
  pass


if __name__ == '__main__':
  all_demos()
