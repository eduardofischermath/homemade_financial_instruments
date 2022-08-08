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