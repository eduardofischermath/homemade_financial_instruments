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

# In this file we provide classes for classifying entities which could
#be defined in different ways.
# For example, interest rate can be given in many forms, like continuously
#or discretely (typically annually if that is the relevant time unit).
# By using a class we can format the object to know exactly what it consists of

########################################################################

class Uniformization():
  """Registers and controls a multi-faceted entity."""
  pass
  
  def get_preferred_form():
    """Returns the preferred form of presentation of entity."""
    return NotImplementedError('Primitively implemented abstract method')

class InterestRateUniformization():
  pass

  def __init__():
    pass
    
  def get_preferred_form(self):
    return self.continuous_interest_rate
