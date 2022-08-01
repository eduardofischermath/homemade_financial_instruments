# In this file we define classes of derivatives (for now essentially
#only vanilla call and put options), plus classes for underlyings (Assets)
#and scenarios (Worlds)

# We try to compute their value in a risk-neutral world via binary trees,
#trying to set a good basic machinery which can potentially be reused later

# In future split into different files

########################################################################

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

########################################################################

class Asset():
  r"""
  Has a value every time.
  May have dividends and costs.
  It is often an underlying of a derivative."""
  
  def get_value(self, time):
    """Returns value at specific time."""
    if time == 0:
      if hasattr(self, initial_value):
        return self.initial_value
      else:
        return NotImplementedError('Primitively implemented abstract method')
    else:
      return NotImplementedError('Primitively implemented abstract method')

  def get_initial_value(self):
    """Returns value at time 0."""
    return self.get_value(time = 0)

  def get_or_override_initial_value(self, overriding_initial_value):
    r"""
    Gets initial value, unless a value is given which overrides the request,
    in which case the value is returned without altering self.
    """
    if overriding_initial_value is not None:
      initial_value = overriding_initial_value
    else:
      try:
        initial_value = self.get_initial_value()
      except:
        raise ValueError('Initial value of asset could not be determined')
    return initial_value
    
  def get_dividend_rate(self, time):
    """Returns dividend rate of asset at specific time"""
    return NotImplementedError('Primitively implemented abstract method')
    
  def get_dividends(self, initial_time, final_time):
    """Returns"""
    return NotImplementedError('Primitively implemented abstract method')
    
  def get_costs(self, initial_time, final_time):
    """Return maintenance costs of asset in time interval."""
    return NotImplementedError('Primitively implemented abstract method')

class FixedCostsAsset(Asset):
  """Asset with fixed costs to maintain."""
  
  def __init__(self, fixed_costs, *args, **kwargs):
    self.fixed_costs = fixed_costs
    super(FixedCostsAsset, self).__init__(*args, **kwargs)
    
  def get_costs(self, initial_time, final_time):
    return self.fixed_costs*(final_time - initial_time)

class FixedCostRateAsset(Asset):
  """Asset which fixed cost rate (a fixed fraction of its value over time)"""
  
  def __init__(self, fixed_cost_rate, *args, **kwargs):
    self.fixed_cost_rate = fixed_cost_rate
    super(FixedCostRateAsset, self).__init__(*args, **kwargs)    

class NoCostsAsset(FixedCostsAsset, FixedCostRateAsset):
  """Asset which costs nothing to maintain."""

  def __init__(self):
    super(NoCostsAsset, self).__init__(fixed_costs = 0, fixed_cost_rate = 0)

class FixedDividendsAsset(Asset):
  """Asset with a fixed dividend rate (fixed fraction of value of asset per time)"""
  
  def __init__(self, dividends):
    self.dividends = dividends
    super().__init__()
  
  def get_dividends(self, initial_time, final_time):
    return self.dividends*(final_time - initial_time)

class FixedDividendRateAsset(Asset):
  """Asset with fixed dividends (constant rate over time)"""
  
  def __init__(self, dividend_rate):
    self.dividend_rate = dividend_rate
    super().__init__()
  
  def get_dividend_rate(self, *args, **kwargs):
    return self.dividend_rate
    
  def get_or_override_dividend_rate(self, overriding_dividend_rate):
    r"""
    Gets dividend rate, unless a value is given which overrides the request,
    in which case the value is returned without altering self.
    """
    if overriding_dividend_rate is not None:
      dividend_rate = overriding_dividend_rate
    else:
      try:
        dividend_rate = self.get_dividend_rate()
      except:
        raise ValueError('Dividend rate of asset could not be determined')
    return dividend_rate

class NoDividendsAsset(FixedDividendsAsset, FixedDividendRateAsset):
  """Asset which generates no dividends"""
  
  def __init__(self):
    super(NoDividendsAsset, self).__init__(dividend_rate = 0)

class NoCostsFixedDividendsAsset(NoCostsAsset, FixedDividendsAsset):
  """Asset with no costs and fixed dividends."""
  pass

class NoCostsFixedDividendRateAsset(NoCostsAsset, FixedDividendRateAsset):
  """Asset with no costs and a fixed dividend rate."""
  pass
  
  @staticmethod
  def static_produce_asset_and_get_or_override_initial_value_and_dividend_rate(asset_or_none,
      overriding_initial_value = None, overriding_dividend_rate = None,
      overriding_class_for_new_instance = None, forbid_overrides = False):
    """Returns tuple with asset, an initial value and a dividend rate."""
    if forbid_overrides:
      asset = asset_or_none
      initial_value = asset.get_initial_value()
      dividend_rate = asset.get_dividend_rate()
      return (asset, initial_value, dividend_rate)
    else:  
      # If self_or_none is not a proper object, it is built with the given information
      #necessary parameters are given, which are used to build an Asset
      if asset_or_none is None:
        # Determine the class by overriding_class_for_new_instance
        if overriding_class_for_new_instance is None:
          overriding_class_for_new_instance = NoCostsFixedDividendRateAsset
        asset = overriding_class_for_production(
            initial_value = overriding_initial_value,
            dividend_rate = overriding_dividend_rate)
      elif isinstance(asset_or_none, NoCostsFixedDividendRateAsset):
        asset = asset_or_none
      else:
        raise ValueError('Expected NoCostsFixedDividendRateAsset or None as asset')
      # Even in case self_or_none was an instance to being with, allow for overriding
      initial_value = asset.get_or_override_initial_value(self)
      dividend_rate = asset.get_or_override_dividend_rate(self)
      return (asset, initial_value, dividend_rate)
  
  @staticmethod
  def static_dirty_get_forward_price(asset_or_none, world_or_none, expiry,
      overriding_initial_value = None, overriding_dividend_rate = None,
      overriding_interest_rate = None, overriding_class_for_new_asset_instance = None,
      overriding_class_for_new_world_instance = None, forbid_overrides = False):
    r"""
    Gets forward price of one asset in given world.
    Allows non-specifying of asset or world and overriding of attributes.
    """
    # Clean-up is done in other methods
    # If creating new instance fixed interest rate and non-arbitrage are expected
    #(if nothing stronger is already requested)
    if overriding_class_for_new_world_instance is None:
      overriding_class_for_new_world_instance = NonArbitrageFixedInterestRateWorld
    asset, initial_value, dividend_rate = NoCostsFixedDividendRateAsset.produce_asset_and_get_or_override_initial_value_and_dividend_rate(
        asset_or_none = asset_or_none,
        overriding_initial_value = overriding_initial_value,
        overriding_dividend_rate = overriding_dividend_rate,
        overriding_class_for_new_instance = overriding_class_for_new_asset_instance,
        forbid_overrides = forbid_overrides)
    world, interest_rate = NonArbitrageFixedInterestRateWorld.static_produce_world_and_get_or_override_interest_rate(
        world_or_none = world_or_none,
        overriding_interest_rate = overriding_interest_rate,
        overriding_class_for_new_instance = overriding_class_for_new_world_instance,
        forbid_overrides = forbid_overrides)
    # In a non-arbitrage world:
    from math import exp
    return initial_value*(exp(expiry*(interest_rate - dividend_rate)))

  def get_forward_price(self, world, expiry):
    """Gets forward price of one asset in given world in given future time/expiry."""
    return self.static_dirty_get_forward_price(
        asset_or_none = self,
        world_or_none = world,
        expiry = expiry,
        forbid_overrides = True)

  @staticmethod
  def static_dirty_price_forward_contract_to_buy(asset_or_none, world_or_none, expiry, struck,
      overriding_initial_value = None, overriding_dividend_rate = None,
      overriding_interest_rate = None, overriding_class_for_new_asset_instance = None,
      overriding_class_for_new_world_instance = None, forbid_overrides = False):
    r"""
    Prices a forward contract to buy one asset at given price and struck.
    Allows non-specifying of asset or world and overriding of attributes.
    """
    # Clean-up is done in other methods
    # If creating new instance fixed interest rate and non-arbitrage are expected
    #(if nothing stronger is already requested)
    if overriding_class_for_new_world_instance is None:
      overriding_class_for_new_world_instance = NonArbitrageFixedInterestRateWorld
    asset, initial_value, dividend_rate = NoCostsFixedDividendRateAsset.produce_asset_and_get_or_override_initial_value_and_dividend_rate(
        asset_or_none = asset_or_none,
        overriding_initial_value = overriding_initial_value,
        overriding_dividend_rate = overriding_dividend_rate,
        overriding_class_for_new_instance = overriding_class_for_new_asset_instance,
        forbid_overrides = forbid_overrides)
    world, interest_rate = NonArbitrageFixedInterestRateWorld.static_produce_world_and_get_or_override_interest_rate(
        world_or_none = world_or_none,
        overriding_interest_rate = overriding_interest_rate,
        overriding_class_for_new_instance = overriding_class_for_new_world_instance,
        forbid_overrides = forbid_overrides)
    # In a non-arbitrage world:
    # (Note asset and world are not none, so variables on subclassing are useless)
    forward_price = asset.static_dirty_get_forward_price(
        asset_or_none = asset,
        world_or_none = world,
        expiry = expiry,
        overriding_initial_value = initial_value,
        overriding_dividend_rate = dividend_rate,
        overriding_interest_rate = interest_rate,
        forbid_overrides = forbid_overrides)
    # Price at expiry of contract would be exactly the difference
    price_at_expiry = forward_price - struck
    from math import exp
    # Use the FixedInterestRateWorld method for computing value in bonds
    # Need dirty version because world.get_interest_rate and interest_rate may be different
    price_at_present = world.static_dirty_translate_bond_value_between_two_times(
        world_of_none = world,
        time_at = expiry,
        value_at_time_at = price_at_expiry,
        another_time = 0,
        overriding_interest_rate = interest_rate,
        forbid_overrides = forbid_overrides)
    return price_at_present

  def price_forward_contract_to_buy(self, world, expiry, struck):
    """Prices a forward contract to buy one asset at given price and struck."""
    return self.static_dirty_price_forward_contract_to_buy(
        asset_or_none = self,
        world_or_none = world,
        expiry = expiry,
        struck = struck,
        forbid_overrides = True)

  @staticmethod
  def static_dirty_price_forward_contract_to_sell(asset_or_none, world_or_none, expiry, struck,
      overriding_initial_value = None, overriding_dividend_rate = None,
      overriding_interest_rate = None, overriding_class_for_new_asset_instance = None,
      overriding_class_for_new_world_instance = None, forbid_overrides = False):
    r"""
    Prices a forward contract to sell one asset at given price and struck.
    Allows non-specifying of asset or world and overriding of attributes.
    """
    # Transfer all arguments to static_dirty_price_forward_contract_to_buy
    value_of_contract_to_buy = NoCostsFixedDividendRateAsset.static_dirty_price_forward_contract_to_buy(
        asset_or_none = asset_or_none,
        world_or_none = world_or_none,
        expiry = expiry,
        struck = struck,
        overriding_initial_value = overriding_initial_value,
        overriding_dividend_rate = overriding_dividend_rate,
        overriding_interest_rate = overriding_interest_rate,
        overriding_class_for_new_asset_instance = overriding_class_for_new_asset_instance,
        overriding_class_for_new_world_instance = overriding_class_for_new_world_instance,
        forbid_overrides = forbid_overrides)
    value_of_contract_to_sell = - value_of_contract_to_buy
    return value_of_contract_to_sell
    
  def price_forward_contract_to_sell(self, world, expiry, struck):
    """Prices a forward contract to buy one asset at given price and struck."""
    return self.static_dirty_price_forward_contract_to_sell(
        asset_or_none = self,
        world_or_none = world,
        expiry = expiry,
        struck = struck,
        forbid_overrides = True)

class FixedCostsNoDividendsAsset(FixedCostsAsset, NoDividendsAsset):
  """Asset with fixed costs and which produce no dividends."""
  pass

class NoCostsNoDividendsAsset(NoCostsAsset, NoDividendsAsset):
  """Asset which costs nothing to maintain and which produce no dividends."""
  pass

class DiscreteAsset(Asset):
  """Asset which has value for (finitely many or infinitely many) discrete values."""
  pass
  
class BinaryTreeAsset(DiscreteAsset):
  r"""
  Discrete asset whose behavior is described by a binary tree.
  At every step the value of the asset can assume two values (depending on the previous).
  """
  pass
  
class EqualUpDownBinaryTreeAsset(BinaryTreeAsset):
  r"""
  Asset which behaves as a binary tree. In every step, the value of the asset
  is bumped up or down by a specific value.
  """
  
  def __init__(self, initial_value, jump_amount):
    self.initial_value = initial_value
    self.jump_amount = jump_amount
  
  @staticmethod
  def produce_all_possible_paths_of_signs(length):
    """Produces iterator of all strings of length max_time made of '+' and '-'."""
    from itertools import product
    return product(['+', '-'], length)
    
  def produce_all_possible_paths_of_values(self, max_time):
    r"""
    Produces iterator with the 2**max_time possible paths the asset values
    may take when going from time 0 through max_time.
    """
    possible_paths_of_signs = self.produce_all_possible_paths_of_signs(length = max_time)
    def create_path_of_values_from_signs(path_of_signs):
      """Returns values of the asset given up-or-down jump pattern."""
      path_of_values = [self.initial_value]
      for idx in range(len(path_of_signs)):
        if path_of_signs == '+':
          new_value_in_path = (path_of_values[-1] + self.jump_amount)
        elif path_of_signs == '-':
          new_value_in_path = path_of_values.append(path_of_values[-1] - self.jump_amount)
        else:
          raise ValueError()
        path_of_values.append(new_value_in_path)
        del new_value_in_path
      # Return has length one more than path_of_signs argument
      return path_of_values
    all_paths_of_values = map(create_path_of_values_from_signs, possible_paths_of_signs)
    return all_paths_of_values
    
  def compute_path_probabilities_in_risk_neutral_world(self, world, max_time):
    r"""
    Computes the probability of each possible path the asset might follow.
    Returns list with 2**max_time items, each item a tuple of the possible path
    and its probability"""
    pass
    ### WORK HERE ###

########################################################################

class Derivative(Asset):
  """For any derivative or financial instrument"""
  
  def __init__(self, underlying):
    """Sets the asset which is the underlying of the derivative"""
    # Typically an non-Derivative Asset, but it could be a Derivative Asset
    self.underlying = underlying
  
class VanillaOption(Derivative, NoCostsNoDividendsAsset):
  """For vanilla (European or American) (put or call) options"""
  
  def __init__(self, underlying, expiry, struck):
    self.expiry = expiry
    self.struck = struck
    super(VanillaOption, self).__init__
    
  def set_american_or_european(self, is_american_instead_of_european):
    if is_american_instead_of_european:
      self.is_american = True
      self.is_european = False
    else:
      self.is_american = False
      self.is_european = True

  def set_put_or_call(self, is_put_instead_of_call):
    if is_put_instead_of_call:
      self.is_put = True
      self.is_call = False
    else:
      self.is_put = False
      self.is_call = True
    
  def value_at_expiry_given_asset_value_at_expiry(self, asset_value_at_expiry):
    if self.is_call:
      return max(0, asset_value_at_expiry - struck)
    elif self.is_put:
      return max(0, struck - asset_value_at_expiry)
    else:
      raise ValueError()

  def compute_present_value_in_risk_neutral_world(self, world):
    """Evaluates asset in a risk-neutral world."""
    # Can be computed if the underlying is, for example, an EqualUpDownBinaryTreeAsset
    return NotImplementedError('Primitively implemented abstract method')

class VanillaCallOption(VanillaOption):
  """Vanilla call option"""
  
  def __init__(self, underlying, expiry, struck):
    self.set_put_or_call(is_put_instead_of_call = False)
    super(VanillaCallOption, self).__init__(underlying, expiry, struck)
  
class VanillaPutOption(VanillaOption):
  """Vanilla call option"""

  def __init__(self, underlying, expiry, struck):
    self.set_put_or_call(is_put_instead_of_call = True)
    super(VanillaPutOption, self).__init__(underlying, expiry, struck)
    
class VanillaEuropeanCallOption(VanillaCallOption):
  """Vanilla European call option"""
  
  def __init__(self, underlying, expiry, struck):
    self.set_american_or_european(is_american_instead_of_european = False)
    super(VanillaEuropeanCallOption, self).__init__(underlying, expiry, struck)
  
class VanillaEuropeanPutOption(VanillaPutOption):
  """Vanilla European call option"""
  
  def __init__(self, underlying, expiry, struck):
    self.set_american_or_european(is_american_instead_of_european = False)
    super(VanillaEuropeanPutOption, self).__init__(underlying, expiry, struck)

class VanillaAmericanCallOption(VanillaCallOption):
  """Vanilla American call option"""
  
  def __init__(self, underlying, expiry, struck):
    self.set_american_or_european(is_american_instead_of_european = True)
    super(VanillaAmericanCallOption, self).__init__(underlying, expiry, struck)
  
class VanillaAmericanPutOption(VanillaPutOption):
  """Vanilla American call option"""
  
  def __init__(self, underlying, expiry, struck):
    self.set_american_or_european(is_american_instead_of_european = True)
    super(VanillaAmericanPutOption, self).__init__(underlying, expiry, struck)

########################################################################


