# ISSUES

Use this file to list and control issues/features/to-dos

(At this moment, this repository is mirrored on GitHub, which has its own project management tools.
At this moment, we prefer to use a ISSUES file.)

Possible values for status: OPEN, COMPLETE, IGNORED, ONGOING.

## ISSUE #0001 ONGOING

Decide versioning/git management/project management structure.

Git versioning is single-branch currently as the current focus is to write
code with a short iteration time. When project grows in complexity
it is likely issues/tickets/todos will be used in project management.

## ISSUE #0002 ONGOING

Define and improve on project structure on all languages.

Currently there are Python, C++ and Common Lisp concurrent code versions,
some more advanced than others, each on their own folders. In the future
there could be ways to install the source code, or to make the different
languages interact.

In Python the code is object-oriented, with abstract (or pseudo-abstract)
classes for Assets, Worlds and Unifications, plus subclasses, always
trying to write functionally. There is a demo file, with interactive prompts,
and unavoidably some is imperative.

## ISSUE #0003 OPEN

For Python, improve package/subpackage/modules structure and importing
to avoid any possible circularities and at the same time don't have names
so long that they hinder development.

## ISSUE #0004 OPEN

Add argument default_if_failed_conversion to input capturing/purifying,
spread it to neighbor functions.

## ISSUE #0005 OPEN

Implement up-propagation (from leaves to root) and down-propagation
(from root to leaves) on binary trees.

## ISSUE #0006 OPEN

Implement formulas for up-propagation  for pricing of vanilla options
for assets behaving in binary trees via replication method (replication
with asset and bond in arbitrage-free world). For example, for a put
European option, if struck is K and fixed short rate is r, if a stands
for value of the underlying asset, pe for pricing of the option, t for
time, and subscripts p, l and r are for parent, left and right nodes in
a three-node three, and T = t_l - t_p = t_r - t_p, then p_p is derived
from p_l and p_r and other variables by:

PE_p = (a_p*(pe_r - pe_l) + exp(-r*T)*(pe_l*a_r - pe_r*a_l))/(a_r - a_l)

and if the put option is American, denoted pa,

pa_p = max(0, K - a_p, (formula above with pa instead of pe))

## ISSUE #0007 OPEN

Implement formulas for up-propagationand via risk-neutral method
(assumption of risk-neutral investors give specific probabilities for the
outcomes and the value of something is "essentially" (need to adjust for
interest rate) equal to its expected value under those probabilities).
