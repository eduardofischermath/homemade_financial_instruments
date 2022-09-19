########################################################################
# DOCUMENTATION / README
########################################################################

# File belonging to software/library/package "financial_instruments"
# Implements financial instruments and solutions for pricing and hedging.

# For more information on functionality, see README.md
# For more information on bugs and planned features, see ISSUES.md
# For more information on versioning, see RELEASES.md

# Copyright (C) 2022 Eduardo Fischer

# This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License version 3
#as published by the Free Software Foundation. See LICENSE.
# Alternatively, see https://www.gnu.org/licenses/.

# This program is distributed in the hope that it will be useful,
#but without any warranty; without even the implied warranty of
#merchantability or fitness for a particular purpose.

########################################################################

# For tree structures, focusing on binary (and may complete) trees

########################################################################

from formulas import *

class FrozenTree():
  """A tree with frozen node structure (the nodes may have mutable data)."""

  def reset_all_nodes_to_specific_data(self, data = None):
    """Changes the data of all nodes to be the specified data."""
    for node in self.list_of_nodes:
      nodes.data = data
  
  def reset_all_nodes_to_dict_with_given_keys(self, keys):
    """Puts a dictionary with given keys (corresponding values being None) at every node."""
    new_dict = {}
    for key in keys:
      new_dict[key] = None
    self.reset_all_nodes_to_specific_data(new_dict)
    
  def reset_all_nodes_to_empty_dictionary(self):
    """Puts an empty dictionary as data of every node."""
    self.reset_all_nodes_to_dict_with_given_keys([])

class FrozenBinaryTree(FrozenTree):
  r"""
  A tree with frozen node structure (the nodes themselves may be mutable)
  and such that every node has at most 2 child nodes.
  """

  def __init__(self, list_of_nodes, root = None, skip_checks = False):
    # Currently assumes list of nodes does form a binary tree
    if not skip_checks:
      if not self.check_consistency_of_list_of_nodes(list_of_nodes):
        raise ValueError('Given nodes cannot form a binary tree.')
    self.list_of_nodes = list_of_nodes
    # Shortcut for root insertion (currently assumes it is indeed the root)
    if root is not None:
      self.root = root
    else:
      self.root = self.static_dirty_get_root_of_node_list(list_of_nodes)

  @staticmethod
  def check_consistency_of_list_of_nodes(list_of_nodes, require_completeness = False):
    """Checks if nodes form a binary tree (or a complete binary tree)"""
    # Currently assumes list of nodes is correct for a (complete) binary tree
    return True

  @staticmethod
  def static_dirty_get_root_of_node_list(list_of_nodes):
    # Currently does not check data is consistent
    root_candidate = list_of_nodes[0]:
    while root_candidate.parent != None:
      root_candidate = root_candidate.parent
    return root_candidate
  
  def get_root(self):
    """Returns root of tree."""
    return self.root

class FrozenBinaryTreeOfDicts(FrozenBinaryTree):
  """A frozen binary tree having dictionaries as data in all nodes."""

  def compute_formula_at_nodes(self, output_key, formula_on_dicts):
    r"""
    Uses a formula to create or update a value for a dictionary key which
    will be present in a dictionary in every node of the tree.
    
    A formula is given which computes a dictionary value at a node based
    on other dictionary values at the same node.
    
    More specifically, it uses a FormulaOnDictionaries with named
    keyword dict arguments called node_dict and all_other_args.
    """
    pass

  def propagate_formula_up(self, output_key, formula_on_dicts):
    r"""
    Uses a formula to create or update a value for a dictionary key at each node.
    
    A formula is given which computes the value of that dict key at that node
    based on the data of its left and right children. The formula should
    also provide a way to compute the value at the leaves.
    
    More specifically, it uses a FormulaOnDictionaries with named
    keyword dict arguments called parent_node_dict, left_child_dict,
    right_child_dict and all_other_args.
    """
    pass
    
  def propagate_formula_down(self, output_key, formula_on_dicts):
    r"""
    Uses a formula to create or update a value for a dictionary key at each node.
    
    A formula is given which computes the value of that dict key at that node
    based on the data of its parent (and whether it is the left or right
    child node). The formula should also a way to compute the value at the root.
    
    More specifically, it uses a FormulaOnDictionaries with named
    keyword dict arguments called parent_node_dict, left_child_dict,
    right_child_dict and all_other_args. The dictionary all_other_args
    must have a key named is_it_left_instead_of_right.
    """
    pass

class FrozenCompleteBinaryTree(FrozenBinaryTree):
  """A FrozenBinaryTree of constant height [distance from leafs to root]."""

  def __init__(self, list_of_nodes, root = None, skip_checks = False):
    if not skip_checks:
      if not self.check_consistency_of_list_of_nodes(list_of_nodes, require_completeness = True):
        raise ValueError('Given nodes cannot form a complete binary tree.')
    super().__init__(list_of_nodes = list_of_nodes, root = root, skip_checks = True)

  def create_from_BinaryTreeAsset(binary_tree_asset):
    pass

class FrozenBinaryTreeNode():
  """A node in a FrozenBinaryTree"""
  
  def __init__(self, data, parent = None, left = None, right = None):
    # By definition left and right must be both None or both non-None
    # (Currently the requirement is not enforced)
    self.data = data
    self.parent = parent
    self.left = left
    self.right = right
