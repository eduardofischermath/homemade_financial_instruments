########################################################################
# DOCUMENTATION / README
########################################################################

# File belonging to software package "homemade_financial_instruments"
# Implements financial instruments and solutions for pricing and hedging.

# For more information on functionality, see README.md
# For more information on bugs and planned features, see ISSUES.md
# For more information on versioning, see RELEASES.md

# Copyright (C) 2025 Eduardo Fischer

# This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License version 3
#as published by the Free Software Foundation. See LICENSE.
# Alternatively, see https://www.gnu.org/licenses/.

# This program is distributed in the hope that it will be useful,
#but without any warranty; without even the implied warranty of
#merchantability or fitness for a particular purpose.

########################################################################

# For rates such as interest rates, or generally numbers over time.

########################################################################

from ..time.timeUnitsContext import *

class Rate():
	"""
	Rates are numbers which normally have as a unit the inverse of
	a time unit.
	
	They can work as simple interest [SimpleRates] or composite interest
	[CompositeRates].
	
	They are treated as real numbers within, but for flexibility, there is
	an option for favoring inputting and outputting them as percentages.
	"""

	def __init__(self, number: float, unit: str: None, asPercentage: bool = False):
		self.asPercentage = asPercentage
		if self.asPercentage:
			self.number = number / 100.0
		else:
			self.number = number
		self.unit = unit
		
	def verificationBeforeConvertionToUnit(self, newUnit: str, /, context: "TimeUnitsContext" = None) -> None:
		"""Verifies"""
		if self.unit is None:
			raise ValueError("Cannot convert to another unit an unitless rate.")
		if context is None:
			context = TimeUnitsContext()
		return None

class CompositeRate(Rate):
	"""
	Rates which work as composite interest: 10% per month at the end of two
	months is more than 21%, and not 20%, for example.
	"""
	
	def convertToUnit(self, newUnit: str, /, context: "TimeUnitsContext" = None) -> "CompositeRate":
		"""Creates new equivalent rate in the unit given."""
		# super() is not strictly necessary here, but we'll use it for future flexibility
		self.super().verificationBeforeConvertionToUnit(context)
		raise NotImplementedError()
		
class SimpleRate(Rate):
	"""
	Rates which are composed simply, purely by addition.
	
	A rate of 20% completion per year is an example of a SimpleRate. It works
	like simple interest: in 5 years it will amount to 100%.
	"""
	
	def convertToUnit(self, newUnit: str, /, context: "TimeUnitsContext" = None) -> "CompositeRate":
		"""Creates new equivalent rate in the unit given."""
		# super() is not strictly necessary here, but we'll use it for future flexibility
		self.super().verificationBeforeConvertionToUnit(context)
		raise NotImplementedError()


