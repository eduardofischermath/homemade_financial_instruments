# In this file we provide classes for classifying entities which could
#be defined in different ways.
# For example, interest rate can be given in many forms, like continuously
#or discretely (typically annually if that is the relevant time unit).
# By using a class we can format the object to know exactly what it consists of

class Uniformization():
  """Register and controls a multi-faceted entity."""
  pass
  
  def get_preferred_form():
    """Returns the preferred form of presentation of entity."""
    return NotImplementedError('Primitively implemented abstract method')

class InterestRateUniformization():
  pass

