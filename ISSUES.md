# ISSUES

Use this file to list and control issues/features/to-dos

(At this moment, this repository is mirrored on GitHub, which has its own
project management tools. At this moment, we prefer to use a ISSUES file.)

Possible values for status: OPEN, COMPLETE, IGNORED, ONGOING.

Issues are uniquely numbered from 0001 through 9999. In case an issue is
specific to one or some of the programming languages then that info might
be added to the number for quicker identification.

## ISSUE #0001 ONGOING

Have versioning/git management/project management structure.

Git versioning is mostly single-branch (named master) as the current focus
is to write code with a short iteration time. Each issue gets a branch for
development, often merged into master branch. As the program develops
further, versioning will likely be on branches named releaseX.Y
containing the vX.Y.Z-tagged commits/versions (X, Y, Z are numbers) which
are the "official releases".

## ISSUE #0002 ONGOING

Define and improve on project structure on all languages.

Currently there are Python, C++, Java and Common Lisp concurrent code
versions, some more advanced than others (in special Python), each on their
own folders. In the future there could be ways to install the source code,
or to make the different languages interact.

In Python the code is object-oriented, with abstract (or pseudo-abstract)
classes for Assets, Worlds and Unifications, plus subclasses, always
trying to write code in a functional and object-oriented paradigm. There
is a demo file, with interactive prompts, and unavoidably some is imperative.

## ISSUE #0003py COMPLETE

For Python, improve package/subpackage/modules/folders structure and importing
to avoid any possible circularities and at the same time avoid excessively
long names which might hinder development.

The way it is done: the large Python project/package has many subpackages.
Each subpackage currently has a single file with multiple classes
(noting that testing is not a subpackage, but outside the large package),
and for each subpackage, the classes within the corresponding files are
brought (via importing) to the top level of the subpackage via:
"from . import * "

The large Python package, on the other hand, will have (via importing) all
subpackages at the top-level by doing relative imports on its init file with:
"from . import subpackage"
If the large package is imported in a module or in interactive session
using a simple "import project" statement, then any Class (except for
testing) is available via project.subpackage.Class, and same for functions

As soon as the project has a more definitive name and preferably procedures
for installing (such pip installation via setuptools) are in place
(after being pip-installed, it can be imported independently of where
a module is being run from or where a interactive session was launched from)
importing within individual files should be done as one of the following:
"from ..subpackage import Class"
"from ..subpackage import * "
(using those relative imports helps keeps the subpackages more or less
independent of the large package)

For an user importing the package in an interactive session or in
a file of another project, a class can be brought to the namespace with:
"from project.subpackage import Class"
and a subpackage (except testing subpackage) can be imported via
"from project import subpackage"

This (importing on init files) might be considered a "hack" or not.
Nonetheless, it is the current way to address importing, subpackaging
and scopes/namespaces.

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

## ISSUE #0011py ONGOING

Work on uniformizations (for example, interest rate and dividend rate, and
also dates), as well as transformations between different frequencies and amounts
(years to days and annual rates to daily rates).

Add percentage functionality for rates and other numbers.

This can be done by having having a class called Rate and at least three attributes:
one numeric for the rate itself, one for whether it prefers to be called as a
percentage, and other for the frequency (per year, per month, per day, et cetera),
which can also be "unspecified"/"unknown"/None if the user doesn't want the depth.

Time can also have many attributes one for the number, and other for the unit. It can
also comport an optional start time and an optional end time.

## ISSUE #0012 COMPLETE

Due to the fact that the words "key" and "value" are used in the context
of a Python dictionary, replace the word "value" for "data" in the context
of the content of a node (in a tree).
(For consistency, this should be the default in all languages.)

## ISSUE #0013 COMPLETE

Rename the project to Homemade Financial Instruments.
It could be called "homemade_financial_instruments" as a project. For
Python's pip it should be "homemadefinancialinstruments" given how
finicky pip is with underlines.

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

## ISSUE #0016 COMPLETE

Update copyright to current year 2023.

## ISSUE #0017py OPEN

Write method check_consistency_of_list_of_nodes for class FrozenBinaryTree
(and possibly also adaptable for other related classes).

## ISSUE #0018py ONGOING

Write method for nicely printing a tree to the screen, so that useful
tests can be written for other tree methods and their correctness can
be verified by a naked human eye.
Alternatively, use a ready-made tree library for printing.

This printing can be done so that the tree goes top-to-bottom when going
root-to-leaves (makes more sense when talking about left and right nodes,
and is prettier but way harder to program) or left-to-right when going
root-to-leaves.

## ISSUE #0019py ONGOING

Create structure for unit testing functionalities of the Python code.
It will be a folder outside the folder of the overall package.

## ISSUE #0020py ONGOING

In support of an in-house solution for ISSUE #0018py, build a class for
dealing with box of characters (currently called string boxes, meaning
a list of strings of same size which are supposed to be displayed in a pile
forming a rectangle of chars).

That class might be called CharacterCanvas or something like that, and
have methods which allow for drawing on the "canvas", which can be finite
or infinite (i. e. supporting arbitrarily long strings even if codified
in lines of finite length) and be stored as a list of same-size strings.
This canvas can support, for example, string boxes (which may or may not
constitute a separate class than the whole canvas), as well as lines
connecting specific points specified as "anchors".

By lines connecting anchors, the idea is: there can be an anchor point
(given by absolute or relative coordinates) of two string boxes. For
example, for a node in a binary tree and a left child, where the levels
of the tree are characterized by their height on the canvas, there can be a
southwest anchor on the parent node and a north anchor on the left child
so that these anchors can be connected via some characters on the canvas
(typically something like '-', '/', '|' or '\') in "ASCII art style".
Although this example was for trees where the root is on the top and it
"grows down", it can also be used for trees where the root is on the left.

There can simply be a method of the canvas: create line between two anchors.
There can also be methods for finding the correct anchor points, and
others for adding a string box to the canvas at a specific coordinate.

An horizontal example with one canvas, two boxes and one line would be:
 -----       -----
|box 1|-----|box 2|
 -----       -----
 
## ISSUE #0021py COMPLETE

Consider descriptions of a binary tree given by a dictionary whose keys
are strings formed by 'l' and 'r' exclusively (including empty string)
and whose values are the nodes one arrives at by following the instructions
(also called path, or address): 'l' for left child, 'r' for right child
starting from the root.

Ensure this is the core of the implementation of the tree (that is,
internal storage).

Do this for FrozenBinaryTree and FrozenPerfectBinaryTree.

(Of course, the nodes themselves have indication of left and right children,
but this would allow for alternative means of navigation, specially for
going up.

This could be a more or less equivalent (in space taken) structure to
store all the nodes of the tree (instead of saving all nodes in a list,
and a variable indicating the root).

## ISSUE #0022py COMPLETE

Split implementation of binary nodes into two different classes (none
should be a subclass of the other):
BinaryNode for "loose" nodes, with data, left and right attributes, exactly
what was FrozenBinaryTreeNode for, and
FrozenBinaryTreeNode for nodes considered inside a FrozenBinaryTree, with
data, left, right and left-right address (name of attribute will be path)
attributes.

This allows a easier way to obtain a parent within a tree, avoiding the
self-referencing, chicken-and-egg problem which would appear if there
was a single mention of the parent in the child node.

This change also has the benefit of forgoing the cumbersome dict_of_parents
attribute in a FrozenBinaryTree, which besides taking up space had the
problem of using nodes as dict keys (they don't have a default hash, and an
implemented hash would likely need to be recomputed every time the content
of the node changes, potentially for many nodes for each change).

## ISSUE #0023py COMPLETE

For methods which check/ensure data quality is the proper one for a method,
allow for two methods (for each possible verification or condition or
set of conditions to be met).

The method whose name starts with the words 'ensure_consistency_of' shall
return None if everything is okay, or raise an Error otherwise. (That is,
they are procedural, non-functional methods.)

The other one should start with 'check_consistency_of', and return a Boolean,
True or False, depending on whether the data is adequate. Of course, errors
outside of the verification process intended by the method can be made
to raise Errors.

At the moment, this applies to the methods for creating a binary tree which
must receive compatible and consistent data, and in the future this
'check'/'ensure' naming convention should apply to other contexts.

## ISSUE #0024py OPEN

Need to design and write the initialization methods for FrozenBinaryTreeNode
so that self-referencing problems do not occur.

Need to streamline options regaring allowing nodes from other trees.
There is confusion because a FrozenBinaryTreeNode has left-right path
information, but it is not possible to access the tree it belongs to
(or even the root, for that matter) only using the node.

Idea: when building nodes from other nodes use:
i) one Boolean option to restrict input to BinaryNodes
ii) another to restrict input to a FrozenBinaryTreeNode already having
the "correct" path/address
iii) a third option to restrict input to a node which fits either of
the previous descriptions (i and ii)

## ISSUE #0025py COMPLETE

The following should be implemented for "StringBox" object. The ideas
here are related to ISSUE #0020py.

The goal is to prepare good (and personalizable) boxes from dicts, and
use them when printing a tree (in particular a FrozenBinaryTreeOfDicts).

Given a dict, can prepare a representation which is a box of strings.
For example (note keys are to be output without single quotes), to produce
a StringBox which looks like:
a: 10
b: 45.25
path: llr

The colons might be forced to be aligned or not. The resulting box has
certain dimensions.

There could be options like for example abbreviating some of the keys
(for example through another dict) or limiting the floats to a specific
number of decimal places.

## ISSUE #0026py OPEN

Consider implementing recombinant trees (as defined on Baxter and Rennie's
book "Financial Calculus"). That is, for any vertex, taking left then right
child yields the same node (or None) than taking right then left child.

Path information can be given as a tuple of length two. The first is the
number of left child operations, the second the number of right child
operations. This also allows to compute the family of parents (in the case
exactly two parents) of a node; this is done by subtracting 1 from either
of the items of the tuple.

## ISSUE #0027py OPEN

Consider creating a class TrioOfNodes, which stores a parent node and
its two children (in the context of a binary tree), possibly as the
values of a dict.

This class can be used to do operations which alter the nodes, such as
propagate_formula_up and propagate_formula_down, without having to verify
the nodes have the correct relationship (because this is would be done
in a previous step than the formula propagation).

(On the other hand, which other information does a TrioOfNodes has which
is not the parent node itself?)

## ISSUE #0028py COMPLETE

An idea for printing a tree, specially good for when the data are dicts
or otherwise good things to represent in boxes of strings, and also
easier to program that the ideas in ISSUE #0018py. Below how a example
with simple/minimal boxes (no decorations around the data) could look like:

a: 1
b: 100
|___L___a: 100
|       b: 10000
|       |___L___a: 300
|               b: 30000
|       |___R___a: 400
|               b: 40000
|___R___c: 2
        |___L___c:20
                |___L___c: 200
                |___R___c: 2000

The top is root, and the children are indicated in a more or less natural
way (L and R indicate left or right). Note the tree does not need to be
perfect.

Note that every single line is dedicated to a single node (and for nodes
whose data is a dict, each line corresponds to a single key).

The "tab" space in the example is 8 but it can be changed according to a
method/function argument in the implementation.

There can also be an option for whether the left or right child comes
on top.

This is more or less (the L and R additions are new flavors specific for
binary trees and necessary for our purposes) how the output of a "tree"
command returns in Bash/Linux/Unix. We shall call this approach the
"indented display", or "indented representation" of the binary tree.

## ISSUE #0029py OPEN

Maybe the Formula (including the FormulaOnDicts wrapper) needs to
be made to either accept only non-keyword/non-made arguments or accept
only keyword/named arguments (in both inputs and outputs).

This can be done by subclassing (leaving the superclass non-initializable).

## ISSUE #0030py OPEN

A possible functionality for the production of a StringBox from a dict:
there could be an option to try to compress the lines and make the best
representation possible conditioned to setting a limit for the number
of columns (i. e. number of chars in each string of the box). For example,
to reduce space, dynamic strategies such as omitting the ASCII spaces
of the string ': ', or rounding to a smaller case of decimal places
could take place.

## ISSUE #0031py OPEN

Consider creating a class called UnevenStringBox. The name is a bit
contradictory name, but it would mean a list of lines but without the
lines being all the same size.

This way, StringBox would be a subclass of UnevenStringBox, and every
StringBox instance would be also an UnevenStringBox instance.

## ISSUE #0032py OPEN

An idea to generate trees in a single line, like a one-line "__repr__".
(Ideas valid also for instantiation of trees.) Can always represent
each node in a binary tree as a triple, the triple being its value/content,
the left and the right node (maybe None). This can be represented like in:
"(10, (20, None, None), None)". With some effort, it might be possible
to even parse a string (but receiving a tuple/list would be way easier).

## ISSUE #0033py OPEN

To increase the modularity of the design, separate the Nodes (the many
types) from the Trees (the many types).

Although in the program they are used in tandem, the nodes are conceptually
more independent. For example, they can be used to form trees (like
in data structures such as heaps/priority queues and binary search trees)
without the overarching of our trees (which don't even have the
self-mutability needed for those data structures).

Thus, in some way, non-frozen trees are implemented in this program -
to do so, use the classes from the nodes package and ignore the trees
package.

## ISSUE #0034py OPEN

Consider renaming the trees package (which contains only frozen trees)
to frozen_trees. First because they are all frozen, the binary ones
even having an argument for the L-R-path/address. Second is that trees
can be formed only with the nodes - even if some operations might be
a little harder to execute.

Other alternative is to keep the same name but also have trees
with mutable node structure (in the future, as they are not needed now).

## ISSUE #0035py OPEN

Consider whether to keep FrozenBinaryTree as a subclass of FrozenTree.

One reason to keep it: all methods of FrozenTree are applicable (with
any possible arguments) to all FrozenBinaryTrees with the understanding
that the left node is the child 0 and the right node is the child 1 of
a node (when considered as FrozenTrees, where the children are given
numbers).

One reason to not: if we want to implement an address/path system for a
FrozenTree, it can be done with a sequence of numbers (instead of
L-R-paths as is the case for FrozenBinaryTrees). But in this case the
addresses would be incompatible for a FrozenBinaryTree when considered
as a FrozenTree: would the path be "lrll" or "0100"?

So if we want to implement paths for FrozenTrees, I believe we are
forced to abandon the subclassing.

## ISSUE #0036py OPEN

Revolutionize the implementation of FrozenBinaryTree and
FrozenBinaryTreeNode.

Make FrozenBinaryTreeNode a nested class inside FrozenBinaryTree.
Also, FrozenBinaryTreeNode should have 5 attributes: value/data/content,
which can be changed more or less freely, and 4 others fundamentally
related to the tree (but crucially don't reference the tree literally,
as that could bring an undesired circularity to the design): left,
right, parent and path/address.

The FrozenBinaryTreeNode should be a dictionary whose keys are paths/
addresses and whose values are the nodes at that position (the nodes
will have their paths/addresses in them too).

In Python, these 4 could be marked as properties, to be read-only, and
to be set only once by the FrozenBinaryTree (in a separate method of
FrozenBinaryTree to be called by FrozenBinaryTree after initiation).

Then methods such as FrozenBinaryTree.get_left_child_of_node_in_tree
(and other navigation methods) can read the correct property in the node.
This would also make dict_of_parents obsolete.

Rationale: since FrozenBinaryTreeNode don't exist without the tree, the
design should indicate that by subclassing. Also, left/right/parent/path
(or address) should never change during the lifetime of a
FrozenBinaryTreeNode.

(Also, note that this could all be created without the nodes themselves,
but it is probably better to have a specific class to encapsulate the
data and the structure and what it means to the whole tree.)

## ISSUE #0037py OPEN

Consider creating a class Node to mean a "blob" with some data. Then it
can have as subclasses (loose) BinaryNode, FrozenBinaryTreeNode (even
being a nested class) and also other non-binary nodes.

Even if the class would be a bit meaningless, it could help from the
point of view of integrating with printing -- for example, methods for
printing a box around the content could be written to Node so they could
be inherited by all its subclasses.

## ISSUE #0038 OPEN

Implement the following idea: a binary tree representing possible
variations of a stock, but at each odd level, it branches off into two
values (up and down), while at the even levels, it branches off into
"stable" or "jump-down" (say a fixed proportion of the asset value).

This could be a tool to model jump-diffusion models while maintaining a 
binary tree (where derivatives can be hedges with asset and bond and
thus can be computed back the tree whatever they payoff is at the leaves).

(Idea was based on Joshi's book, page 86.)

## ISSUE #0039ja COMPLETE

Start project also in Java

## ISSUE #0040 ONGOING

Implement formulas for outstanding balance/balance due.
In particular, for a case of fixed installments, given three among:
outstanding balance, the interest rate (say per month), the number of time
units (say months) and the installment, compute the fourth.

The key formula will be described below. Let P0 be the borrowed principal,
and let P(i) the balance at time i (exaclty after the i-th payment).
Then P(0) = P0. Also, let n be the number of time units for the installments;
then P(n) = 0. The interest rate could be given in multiple ways, but
to ease the formulas we will write as u > 1, meaning u = e^r, for r the
continuously compounded interest rate, or u = 1+s, if s is the interest
rate for the timeunit. Let also a be the value of a single installment.

Observing the effect of a single timeunit, we can write:

$P(i) = P(i-1)*u - a$

Knowing P(0) and P(n), P(i) can be determined as

$P(n-i) = a*(u + u^2 + ... + u^i)$

In particular,

$P = a*(u + u^2 + ... + u^n)$

Or alternatively, since u > 1,

$P = a*u*(u^n - 1)/(u - 1)$

This last formula helps use to easily compute P, n or a from the others.
On the other hand, to compute u from P, n and a, we likely will need to
implement something like the Newton method (or better, import external
libraries for it).

We can potentially write the formulas better, for example in a PDF, to
help the user to the program.

Suggestion of design: use two classes, one outside, which is responsible
for handling requests, and one inside, which is an instance of a
fixed-installment borrowing, with the four numbers above specified and
fixed throughout the existence of the instance.

## ISSUE #0040ja ONGOING

Progress of ISSUE #0040 in Java. 

## ISSUE #0040py ONGOING

Progress of ISSUE #0040 in Python.

## ISSUE #0041py OPEN

Implement ISSUE #0040py using the Formula class formalism. More precisely:
use instances of Formulas to write the formulas used to derive the fourth
variable from the other three. (At least for the ones which have closed
formulas).

## ISSUE #0042 OPEN

Regarding ISSUE #0040: add possibility of down payment

## ISSUE #0043 OPEN

Regarding ISSUE #0040: add another feature in which, for an instance of
a fixed-payment borrowing, provides the outstanding balance at any moment,
and given an outstanding balance, provides the time that balance is the
amount owed.

## ISSUE #0044 OPEN

In addition to ISSUE #0040, add all characteristics available on the HP
12-C financial calculator. That is, functions which relate PV (present
value), FV (future value), n (number of payments, or number of coupons
in some contexts), i/d/y (the discount rate, or interest rate of the
value) and PMT (the value of each payment, or coupon, depending on the
context).

Also adopt the conventions for negative and positive numbers; for example,
that incoming money is positive while outgoing is negative, as is the
convention on the HP 12-C.

## ISSUE #0045 OPEN

Adopt the functions for cash flows as can be done on the HP 12-C (i. e.
the functions corresponding to the buttons CF0, CFij, Nj, NPV, i and IRR
in the calculator).

## ISSUE #0046 OPEN

Since it is usual that some Brazilian instruments pay a percentage of a
certain index (for example, something with a remuneration of a percentage
of the CDI), implement that computation correctly to match the behavior of
the Brazil Central Bank's "Calculadora do cidadão".

This in particular would be very useful for a more user-front-facing demo or
application.

According to "Calculadora do cidadão", the rule is that the percentage would
always affect the exponent, and not the resulting interest rate. For example,
for dates January 2, 2020 and January 2, 2024, 100% of the CDI results in a
correction factor of 1.36324865 (i. e., interest rate of 36.324865%) while
50% of the CDI results in a correction factor of 1.16760108 (i. e., interest
rate of 16.760108%), and the relationship between these numbers is between
the correction factors, which are close to the square of each other (due to
daily compounding and rounding errors, I can only assume), while their
interest rates are not obviously related.

## ISSUE #0047 OPEN

Implement the concept of Macauley duration and of modified duration for
investments.

Also use the idea to implement the idea that the modified duration corresponds
to the negative of the derivative of the present price of the instrument
with regard to the interest rate. Perhaps use the idea to linearly estimate
(and maybe verify with other formulas) the price given the variation
in interest rates.

## ISSUE #0048 OPEN

Since most of Brazilian-based finance is based on an year of 252 business days,
build utility to compute number of business days between any two dates.

## ISSUE #0049py OPEN

One utility for percentages can be: given an object from the user, if it is a
string ending in a "%" char, make it a percentage (Python does not do that
natively). Otherwise treat it approprietly. Such function can be called
something like "readNumberOrPercentage".

## ISSUE #0048 OPEN

Code structure to compute IRRBB as determined by BCB Circular number 3876,
or at least NII and EVE (i. e. without the shocks).
