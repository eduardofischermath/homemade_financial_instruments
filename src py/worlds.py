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

# All Worlds in this world

########################################################################

from trees import *

class World():
  """Holds conditions and properties of the world."""
  pass

class NonArbitrageWorld(World):
  """World without arbitrages."""
  pass

class FixedInterestRateWorld(World):
  """World with a fixed interest rate through which bonds are negotiated."""

  def __init__(
      self,
      interest_rate,
      is_rate_discrete_instead_of_continuous = False,
      is_rate_percentage_instead_of_absolute = False):
    self.set_interest_rates(
        self,
        interest_rate,
        is_rate_discrete_instead_of_continuous,
        is_rate_percentage_instead_of_absolute)
  
  def set_interest_rates(
      self,
      interest_rate,
      is_rate_discrete_instead_of_continuous = False,
      is_rate_percentage_instead_of_absolute = False):
    """Set (fixed) discrete and continuous interest rates in the world."""
    if is_rate_percentage_instead_of_absolute:
      interest_rate = interest_rate / 100.0 # Python-agnostic
    # Discrete interest rate is also called annualized on some sources
    # Continuouly compounded rate is also called continous, or short rate
    if is_interest_rate_discrete_instead_of_continuous:
      from math import log1p # More precise than log(1 + _)
      self.continuous_interest_rate = log1p(interest_rate)
      self.discrete_interest_rate = interest_rate
    else:
      from math import expm1 # More precise than exp(_) - 1
      self.continuous_interest_rate = interest_rate
      self.discrete_interest_rate = expm1(interest_rate)

  def get_interest_rate(self, *args, **kwargs):
    """Gets interest rate (the continuously compounded rate, or short rate)"""
    return self.continuous_interest_rate

  def get_or_override_interest_rate(self, overriding_interest_rate):
    r"""
    Gets interest rate, unless a value is given which overrides the request,
    in which case the value is returned without altering self.
    """
    if overriding_interest_rate is not None:
      interest_rate = overriding_interest_rate
    else:
      try:
        interest_rate = self.get_interest_rate()
      except:
        raise ValueError('Interest rate in world could not be determined')
    return interest_rate

  @staticmethod
  def static_produce_world_and_get_or_override_interest_rate(world_or_none,
      overriding_interest_rate = None, overriding_class_for_new_instance = None,
      forbid_overrides = False):
    """Returns tuple with world and an interest rate."""
    if forbid_overrides:
      world = world_or_none
      interest_rate = world.get_interest_rate()
      return (world, interest_rate)
    else:
      # If world_of_none not a proper object, build it with parameters given
      # If overriding class not given, default is FixedInterestRateWorld
      if world_or_none is None:
        if overriding_class_for_new_instance is None:
          overriding_class_for_new_instance = FixedInterestRateWorld
        world = overriding_class_for_new_instance(
            interest_rate = overriding_interest_rate)
      elif isinstance(world_or_none, FixedInterestRateWorld):
        world = world_or_none
      else:
        raise ValueError('Expected FixedInterestRateWorld or None as asset')
      # Extract interest rate, allowing for overrides
      interest_rate = world.get_or_override_interest_rate(world)
      return (world, interest_rate)

  @staticmethod
  def static_dirty_translate_bond_value_between_two_times(world_or_none,
      time_at, value_at_time_at, another_time, overriding_interest_rate = None,
      forbid_overrides = False):
    r"""
    Given bond with specific value at specific time, compute its value at another time.
    Allows for non-specification of world, and also for overriding of interest rate.
    """
    world, interest_rate = FixedInterestRateWorld.static_produce_world_and_get_or_override_interest_rate(
        world_or_none = world_or_none,
        overriding_interest_rate = overriding_interest_rate,
        forbid_overrides = forbid_overrides)
    time_difference = another_time - time_at
    from math import exp
    return value_at_time_at * exp(self.continuous_interest_rate * time_difference)

  def translate_bond_value_between_two_times(self, time_at, value_at_time_at, another_time):
    """Given bond with specific value at specific time, compute its value at another time."""
    return self.static_dirty_translate_bond_value_between_two_times(
        world_or_none = self,
        time_at = time_at,
        value_at_time_at = value_at_time_at,
        another_time = another_time,
        forbid_overrides = True)
  
  @staticmethod
  def static_dirty_compute_current_value_in_bonds_at_another_time(world_or_none,
      current_value_in_bonds, another_time, overriding_interest_rate = None,
      forbid_overrides = False):
    r"""
    Computes value of bonds currently held at another time.
    Allows for non-specification of world, and also for overriding of interest rate.
    """
    return self.static_dirty_translate_bond_value_between_two_times(
        world_or_none = world_or_none,
        time_at = 0,
        value_at_time_at = current_value_in_bonds,
        another_time = another_time,
        overriding_interest_rate = None,
        forbid_overrides = False)

  def compute_current_value_in_bonds_at_another_time(self, current_value_in_bonds, another_time):
    """Computes value of bonds currently held at another time"""
    return self.static_dirty_compute_current_value_in_bonds_at_another_time(
        world_or_none = self,
        current_value_in_bonds = current_value_in_bonds,
        another_time = another_time,
        forbid_overrides = False)

class NonArbitrageFixedInterestRateWorld(NonArbitrageWorld, FixedInterestRateWorld):
  r"""
  World without arbitrage in which there is a fixed interest rate
  which determines the value of bonds through time.
  """
  pass

class RiskNeutralWorld(World):
  """World in which all participants are neutral with respect to risk."""
  pass
  
class RiskNeutralFixedInterestRateWorld(RiskNeutralWorld, FixedInterestRateWorld):
  """World in which the expected value for any asset grow at the interest rate."""
  pass
