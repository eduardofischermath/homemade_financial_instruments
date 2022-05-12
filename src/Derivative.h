

#include "pure_objects.h"

#include <string.h>

class Derivative{
  PureDerivative pure_base;
  string name = pure_base::name;
  PureFinancialObject underlying = pure_base::underlying;
  
  price(){
  }
  
  hedge(){
  }
}
