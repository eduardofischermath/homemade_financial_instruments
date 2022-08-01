/**
 * All financial objects are structs, PureFinancialObject.
 */

#include <string.h>

struct PureFinancialObject{
  string name;
}

PureFinancialObject PureStock{
  string name;
}

PureFinancialObject PureDerivative{
  string name;
  PureFinancialObject underlying;
}

PureDerivative PureOption{
  string name;
  PureFinancialObject underlying;
  bool is_call;
}
