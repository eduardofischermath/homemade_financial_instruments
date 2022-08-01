
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
