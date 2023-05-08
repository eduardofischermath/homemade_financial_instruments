#||
########################################################################
# DOCUMENTATION / README
########################################################################

File belonging to software/library/package "financial_instruments"
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
||#

;; Code in Common Lisp

;; Computes the value of an asset growing at certain interest rate
(defun compute-growth-fixed-interest-rate (spot, other-time, interest-rate)
"Docstring"
(* spot exp (* other-time interest-rate))
)

;; Write function for computing price of a forward contract to buy one unit of an asset in the future at the struck price
(defun price-forward-contract (spot, expiry, interest-rate, struck)
"Docstring"
(- struck (compute-growth-fixed-interest-rate(spot expiry interest-rate)))
)
