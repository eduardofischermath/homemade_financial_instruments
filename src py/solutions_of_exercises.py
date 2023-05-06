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

# This file is for small functions which solve exercises in the book
#"The Concepts and Practice of Mathematical Finance", 2nd edition, by
#Mark Joshi, thereon referred to only as Joshi's book or Joshi's.

########################################################################

from math import exp

# For problem 6 in chapter 3: we evaluate the European put option
# (Note the process prices an European call option instead of the
#European put option. We do put-call parity at the end.)
# Time is always 4 months. Variables:
# Annual continuous interest rate in problem is r = 0.05 annual continuous
# Start at S0 = 100
# Jumps by +A or -A each month (in problem A = 10)
# We assume the final position is S0 + 2A or S0 + 4A
# We assume the option was struck at S0 + A
def solution_03_06(S0 = 100, A = 10, r = 0.05, use_sanity_checks = False):
  # We first write the possible lists. 1st through 4th is preparation
  #for S0 + 2A, the last being for S0 + 4A
  pre_lists = []
  pre_lists.append(['-', '+', '+', '+'])
  pre_lists.append(['+', '-', '+', '+'])
  pre_lists.append(['+', '+', '-', '+'])
  pre_lists.append(['+', '+', '+', '-'])
  pre_lists.append(['+', '+', '+', '+'])
  historic_lists = []
  for pre_list in pre_lists:
    new_list = [S0]
    for plus_or_minus in pre_list:
      if plus_or_minus == '+':
        new_list.append(new_list[-1] + A)
      else:
        new_list.append(new_list[-1] - A)
    historic_lists.append(new_list)
  if use_sanity_checks:
    print(historic_lists)
  # Useful value which will be used many times:
  epsilon = (exp(r/12) - 1) / (2*A)
  if use_sanity_checks:
    print(f'{epsilon=}')
  # Now we compute expected value. Note the value of the European call option
  #at expiry is exactly A if S4 = S0+2A and exactly 3A if S4 = S0+4A,
  #or simply taking the last element and subtracting S0 + A
  call_option_expected_future_value = 0
  for (history_in_numbers, history_in_signs) in zip(historic_lists, pre_lists):
    value_of_history = (history_in_numbers[-1] - S0 - A)
    for index in range(0, 4):
      if history_in_signs[index] == '+':
        value_of_history *= 0.5 + history_in_numbers[index]*epsilon
      else: 
        value_of_history *= 0.5 - history_in_numbers[index]*epsilon
    call_option_expected_future_value += value_of_history
  if use_sanity_checks:
    print(f'{call_option_expected_future_value=}')
  # To compute value at present, at time 0
  call_option_present_value = call_option_expected_future_value * exp(-4*r/12)
  # Using put-call parity for a contract to buy with struck S0 + A
  present_value_of_forward_contract = exp(-4*r/12)*(S0*exp(4*r/12) - (S0 + A))
  if use_sanity_checks:
    print(f'{present_value_of_forward_contract=}')
  put_option_present_value = call_option_present_value - present_value_of_forward_contract
  if use_sanity_checks:
    print(f'{put_option_present_value=}')
  return put_option_present_value

