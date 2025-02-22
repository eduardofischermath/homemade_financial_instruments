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

from typing import Optional, Union

from ..utilities import *
from ..formulas import *

class TimeUnitsContext():
	"""
	Presents rules for changing time units.
	
	Default is the Brazilian standard, with 252 days per year, but one can
	also call the 30/360 standard using the string "30/360 us" as argument.
	"""
	
	BRAZILIAN_STANDARD_CONVERSION_DICT = {
		"year" : {
			"day": 252,
			"month": 12,
		},
		"month" : {
			"day": 21,
	}
	
	THIRTY_THREE_SIXTY_CONVERSION_DICT = {
		"year" : {
			"day": 360,
			"month": 12,
		},
		"month" : {
			"day": 30,
	}
	
	DIRECT_TO_INVERTED_STANDARD_CONVERSION_DICT = {
		"year" : "annual",
		"month" : "monthly",
		"day": "daily",
	}

	def __init__(
			self,
			directTransformDict: Optional[Union[dict, str]] = None,
			onlyPartial = True,
			directToInvertedDict: Optional[dict] = None,
	):
		if self.directTransformDict is None:
			onlyPartial = True
			self.directTransformDict = dict(self.BRAZILIAN_STANDARD_CONVERSION_DICT)
		elif isinstance(directTransformDict, str):
			onlyPartial = True
			if directTransformDict.lower() == "brazilian":
				self.directTransformDict = dict(self.BRAZILIAN_STANDARD_CONVERSION_DICT)
			elif directTransformDict.lower() == "30/360 us":
				self.directTransformDict = dict(self.THIRTY_THREE_SIXTY_CONVERSION_DICT)
		else:
			self.directTransformDict = dict(directTransformDict)
		if onlyPartial:
			self.directTransformDict = self.completePartialDict(self.directTransformDict)
		if directedToInvertedDict is None:
			self.directToInvertedDict = DIRECT_TO_INVERTED_STANDARD_CONVERSION_DICT
		else:
			self.directToInvertedDict = directToInvertedDict
		self.inverseTransformDict = self.getInverseDict(
				self.directTransformDict,
				self.directToInvertedDict,
		)

	def getInverseDict(self, directDict: dict, directToInverted: dict): dict:
		"""
		Gets dict with reverse relations between time units.
		
		For example, if a year has 12 months, a monthly equivalent rate of an
		annual rate is represented as a number which is 1/12 of the latter.
		"""
		dictWithInverses = {}
		for firstKey, valueDict in dict_.items():
			inverseFirstKey = self.inverseTransformDict[firstKey]
			for secondKey, ratio in valueDict.items():
				inverseSecondKey = self.inverseTransformDict[secondKey]
				if inverseSecondKey not in dictWithInverses.keys():
					newDict[inverseSecondKey] = {}
				dictWithInverses[inverseSecondKey][inverseFirstKey] = ratio
		return dictWithInverses

	def completePartialDict(self, dict_: dict) -> dict:
		"""
		Completes dict including reverse relations such as: if the dictionary
		specifies 12 months in an year, then a month is 1/12 of an year.
		
		Also adds identity rules (e.g one month is one month) for all keys.
		
		It assumes given partial dict is all correct (has a single occurrence
		of each pair). It does not make further assumptions.
		"""
		newDict = dict(dict_)
		for firstKey, valueDict in dict_.items():
			for secondKey, ratio in valueDict.items():
				if secondKey not in newDict.keys():
					newDict[secondKey] = {}
				newDict[secondKey][firstKey] = 1 / ratio
		for key in newDict.keys():
			newDick[key][key] = 1
		return newDict

	def directTransform(self, num: float, unitFrom: str, unitTo: str) -> float:
		"""
		Converts a number from one [direct] time unit to another.
		
		For example, converts 2 years into 24 months.
		"""
		ratio = self.directTransformDict[unitFrom][unitTo]
		return num * ratio
		
	def inverseTransform(self, num: float, unitFrom: str, unitTo: str, compositeNotSimple: bool) -> float:
		"""
		Converts a number from one [inverse] time unit to another.
		
		Option compositeNotSimple decides if it will convert as composite or
		simple interest.
		
		For example, 0.01 monthly is equivalent to 0.12 yearly via simple
		interest, and to (1.01)*12 - 1 via composite interest. 
		"""
		ratio = self.inverseTransformDict[unitFrom][unitTo]
		if compositeNotSimple:
			return (1 + num)**ratio - 1
		else:
			return num * ratio
		
