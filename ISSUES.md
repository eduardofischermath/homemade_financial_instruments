# ISSUES

Use this file to list and control issues/features/to-dos

(At this moment, this repository is mirrored on GitHub, which has its own project management tools.
At this moment, we prefer to use a ISSUES file.)

Possible values for status: OPEN, COMPLETE, IGNORED, ONGOING.

Issues are uniquely numbered from 0001 through 9999. In case an issue is
specific to one or some of the programming languages then it might be added
to the number for quicker identification.

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
trying to write code in a functional and object-oriented paradigm. There
is a demo file, with interactive prompts, and unavoidably some is imperative.

## ISSUE #0003py OPEN

For Python, improve package/subpackage/modules structure and importing
to avoid any possible circularities and at the same time avoid excessively
long names which might hinder development.

## ISSUE #0004py OPEN

Add argument default_if_failed_conversion to input capturing/purifying,
spread it to neighbor functions.

## ISSUE #0005py ONGOING

Implement up-propagation (from leaves to root) and down-propagation
(from root to leaves) on binary trees.

## ISSUE #0006py ONGOING

Implement formulas for up-propagation  for pricing of vanilla options
for assets behaving in binary trees via replication method (replication
with asset and bond in arbitrage-free world). For example, for a put
European option, if struck is K and fixed short rate is r, if a stands
for value of the underlying asset, pe for pricing of the option, t for
time, and subscripts p, l and r are for parent (itself), left and right
nodes in a three-node three, and T = t_l - t_p = t_r - t_p, then p_p is
derived from p_l and p_r and other variables by:

PE_p = (a_p*(pe_r - pe_l) + exp(-r*T)*(pe_l*a_r - pe_r*a_l))/(a_r - a_l)

and if the put option is American, denoted pa,

pa_p = max(0, K - a_p, (formula above with pa instead of pe))

This also includes implementing a formula/function handler. This is doable
as SageMath has some functionality, but currently most of the code is
simply an interface for what is essentially a function. Maybe need to
implement something like symbolic variables (like SageMath or TensorFlow).

Maybe the Formula (including the FormulaOnDicts wrapper) needs to
be made to accept only named arguments?

## ISSUE #0007py OPEN

Implement formulas for up-propagationand via risk-neutral method
(assumption of risk-neutral investors give specific probabilities for the
outcomes and the value of something is "essentially" (need to adjust for
interest rate) equal to its expected value under those probabilities).

## ISSUE #0008 COMPLETE

Add to each file a header related to author, copyright and license.

## ISSUE #0009py COMPLETE

Add methods to navigate through nodes among a tree. For example, in a way that takes
a node and a string such as "plr" and produces the parent node of the given node,
then takes its left child node and then its right child node.

## ISSUE #0010py OPEN

Write code for pricing put American options in Exercise 6 of Chapter 3 of
Mark Joshi's book "The Concepts and Practice of Mathematical Finance"
using the FrozenBinaryTree methods (yet to be coded).

## ISSUE #0011py OPEN

Work on uniformizations (for example, interest rate and dividend rate).
Also, add function outside classes for transformation into and out of
percentage (probably better outside classes than a method of a class
designed specifically for that).

## ISSUE #0012 COMPLETE

Due to the fact that the words "key" and "value" are used in the context
of a Python dictionary, replace the word "value" for "data" in the context
of the content of a node (in a tree).
(For consistency, this should be the default in all languages.)

## ISSUE #0013 OPEN

Consider renaming the project to Homemade Financial Instruments.
(Or something else, or not rename at all.)

## ISSUE #0014py OPEN

Write type hints (introduced in Python 3.5 via PEP 484) for every existing
variable/function/method.
Do the same for variable annotations (PEP 526, Python 3.6)
Also consider the constructions final/Final/@final (PEP 591, Python 3.8)

## ISSUE #0015py COMPLETE

Rename some classes to avoid the full word Dictionary, abbreviating it
to Dict.

Make some effort to restrict the types of argumentos (positional and
keyword) which can appear in a DictArgumentProcessor (previously
DictionaryArgumentProcessor).

Allow for DictArgumentProcessor to explicitly take dict items
(in tuple and dict input) and also to avoid them. This way the purpose
of an instance becomes clearer specially when used with FormulaOnDicts.
