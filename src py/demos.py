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

def all_demos():
  """Provides envelope for all demonstration functions."""
  should_keep_going = True
  while should_keep_going:
    evaluate_option_using_binary_tree_demo()
    should_keep_going_raw = best_input('Wish to continue? [Y]es or [N]o.\n')
    if should_keep_going_raw[0].lower() == 'y':
      pass
    else:
      should_keep_going = False
    
def evaluate__vanilla_option_using_binary_tree_demo():
  """Computes value of vanilla option with user-provided information"""
  pass


if __name__ == '__main__':
  all_demos()
