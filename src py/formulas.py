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
    return self.inner_function(*args, **kwargs)
