/*
########################################################################
# DOCUMENTATION / README
########################################################################

File belonging to software package "homemade_financial_instruments"
Implements financial instruments and solutions for pricing and hedging.

For more information on functionality, see README.md
For more information on bugs and planned features, see ISSUES.md
For more information on versioning, see RELEASES.md

Copyright (C) 2023 Eduardo Fischer

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License version 3
as published by the Free Software Foundation. See LICENSE.
Alternatively, see https://www.gnu.org/licenses/.

 This program is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
merchantability or fitness for a particular purpose.
*/

#include "pure_objects.h"
#include "Derivative.h"

#include <string.h>



class Option: public std::Derivative{
  PureOption pure_base;
  bool is_call = pure_base.is_call;
  double struck;
  double expiry_time;
  
public:

  Option(){
  }
  
  // Note: need to figure out where to include volatility and value of Stock
  black_scholes_merton_price(){
  }
  
  delta_hedge(){
  }
}
