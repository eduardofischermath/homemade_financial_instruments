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

# For times and intervals and durations and other time measurements.

########################################################################

from typing import Optional

from ..utilities import *
from ..formulas import *

class TimeInterval():
	"""
	
	Unit is assumed to be always in the singular.
	"""

	def __init__(self, length: float, unit: Optional[str], /, startTime: float = None, endTime: float = None):
		self.length = length
		self.unit = unit
		self.startTime = startTime
		self.endTime = endTime
		if self.startTime is not None or self.endTime is not None:
			raise NotImplementedError()
		
	def setUnit(self, unit: str):
		"""Sets an unit for an unitless time interval."""
		if self.unit is not None:
			raise ValueError("Cannot set the unit. Need to use a conversion.")
		self.unit = unit

	def removeUnit(self):
		"""Renders a non-unitless time interval unitless."""
		if self.unit is not None:
			raise ValueError("Unit already unitless.")
		self.unit = None
		
	def __str__(self):
		if self.unit is None:
			unitString = ""
		else:
			unitString = " " + self.unit
			if self.length != 1:
				unitString += "s"
		return str(self.length) + unitString
		
	def convertToDifferentUnit(self, unit, / , timeUnitsTransformationsContext = None):
		if self.unit is None:
			raise ValueError("Cannot convert already unitless TimeInterval")
		if timeUnitsTransformationsContext is not None:
			raise NotImplementedError()
		if self.startTime is not None or self.endTime is not None:
			raise NotImplementedError()
