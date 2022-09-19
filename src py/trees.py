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

# For tree structures, focusing on binary (and may perfect) trees

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

  def __init__(self, list_of_nodes = None, root = None, skip_checks = False):
    # Can be formed by either giving its root or by providing a list of all nodes
    if list_of_nodes != None:
      # Currently assumes list of nodes does form a binary tree
      if not skip_checks:
        if not self.check_consistency_of_list_of_nodes(
            list_of_nodes = list_of_nodes,
            require_perfectness = False,
            return_boolean_instead_of_potentially_raising_error = True):
          raise ValueError('Given nodes cannot form a binary tree.')
      self.list_of_nodes = list_of_nodes
      # Shortcut for root insertion
      if skip_checks and root is not None:
        self.root = root
      else:
        computed_root = self.static_dirty_get_root_of_node_list(list_of_nodes)
        if root is None:
          self.root = computed_root
        else:
          # In this case root is not None and skip_checks is False
          if root == computed_root:
            self.root = computed_root
          else:
            raise ValueError('Given root is not root of given list of nodes')
    elif root != None:
      self.root = root
      self.list_of_nodes = self.static_dirty_get_list_of_nodes_from_root(self.root)
    else:
      raise ValueError('Needs either root or list of nodes to build instance')

  @staticmethod
  def check_consistency_of_list_of_nodes(list_of_nodes, require_perfectness = False,
      return_boolean_instead_of_potentially_raising_error = False):
    r"""
    Checks if nodes form a binary tree (or a perfect binary tree).
    
    It can be set up to return True or False (if it passes or fails the test,
    respectively), or to raise an Error if fails the test and doing nothing
    if it passes."""
    # Currently assumes list of nodes is correct for a (perfect) binary tree
    if return_boolean_instead_of_potentially_raising_error:
      return True
    else:
      return None

  @staticmethod
  def static_dirty_get_root_of_node_list(list_of_nodes, skip_checks = False):
    """Obtains the root from a list of nodes."""
    # Currently does not check nodes consistently form a tree
    root_candidate = list_of_nodes[0]
    while root_candidate.parent != None:
      root_candidate = root_candidate.parent
    return root_candidate
    
  @staticmethod
  def static_dirty_get_list_of_nodes_from_root(root):
    """Produces a list of all nodes which are descendents of a given node."""
    list_of_nodes = []
    def navigate_tree_and_append_node_to_list(node, list_of_nodes):
      list_of_nodes.append(node)
      if node.left != None:
        navigate_breadth_first_and_append_children_to_list(node.left, list_of_nodes)
      if node.right != None:
        navigate_breadth_first_and_append_children_to_list(node.right, list_of_nodes)
    list_of_nodes = navigate_tree_and_append_node_to_list(root, list_of_nodes)
    return list_of_nodes
  
  def get_root(self):
    """Returns root of tree."""
    return self.root
    
  def get_parent_of_node_in_tree(self, node):
    """Returns parent of node, or None if root."""
    if hasattr(self, dict_of_parents):
      return sef.dict_of_parents[node]
    else:
      putative_parent = None
      for other_node in self.list_of_nodes:
        if other_node.left == node or other_node.right == node:
          putative_parent = other_node
          break
      return putative_parent

  def create_dict_of_parents(self, set_as_attribute_instead_of_returning = False,
      ignore_if_already_set = False):
    r"""
    Creates a dictionary associating to each node its parent (or None for the root).
    
    Has the option of either returning the dictionary or setting it as
    an attribute dict_of_parents of the instance (and returning None).
    
    Has the option to consider or ignore a dict_of_parents previously set
    as attribute. If not ignored and the attribute is set, then the method
    simply uses it.
    """
    if ignore_if_already_set and hasattr(self, dict_of_parents):
      dict_of_parents = self.dict_of_parents
    else:
      dict_of_parents = {}
      for node in self.list_of_nodes:
        if node.left != None:
          dict_of_parents[node.left] = node
        if node.right != None:
          dict_of_parents[node.right] = node
    if set_as_attribute_instead_of_returning:
      self.dict_of_parents = dict_of_parents
      return None
    else:
      return dict_of_parents
    
  def navigate_tree_by_string(self, node, string, raise_error_if_string_has_invalid_chars = True,
      raise_error_if_navigation_leads_to_none = True):
    r"""
    Given an initial node and a string made with the characters 'p', 'l' and 'r'
    will produce the node obtaining from the operations of successfuly
    taking parent (for 'p') or left child (for 'l') or right child (for 'r')
    starting from the initial node.
    
    Has option to allow for staying in place if a 'p', 'l' or 'r' instruction
    is provided which would lead to no node.
    """
    # Since this might be called multiple times it might be useful to set
    #all parents at once instead of searching every time
    create_dict_of_parents(self, set_as_attribute_instead_of_returning = True,
        ignore_if_already_set = False)
    current_node = node
    for char in string:
      if char.lower() == 'p':
        putative_next_node = self.dict_of_parents[current_node]
      elif char.lower() == 'l':
        putative_next_node = current_node.left
      elif char.lower() == 'r':
        putative_next_node = current_node.right
      else:
        if raise_error_if_string_has_invalid_chars:
          raise ValueError('String should contain only \'p\', \'l\' and \'r\'.')
        else:
          pass
      # Every new potential node needs to be checked if it is a node in tree
      if putative_next_node is not None:
        current_node = putative_next_node
      else:
        if raise_error_if_navigation_leads_to_none:
          raise ValueError('Cannot follow path for navigation inside tree.')
        else:
          pass # current_node stays as it is for this loop iteration
    return current_node

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

class FrozenPerfectBinaryTree(FrozenBinaryTree):
  """A FrozenBinaryTree of constant height [distance from leafs to root]."""

  def __init__(self, list_of_nodes = None, root = None, skip_checks = False):
    if not skip_checks:
      if not self.check_consistency_of_list_of_nodes(
          list_of_nodes = list_of_nodes,
          require_perfectness = True,
          return_boolean_instead_of_potentially_raising_error = True):
        raise ValueError('Given nodes cannot form a perfect binary tree.')
    super().__init__(list_of_nodes = list_of_nodes, root = root, skip_checks = True)

  def __len__(self):
    """Returns the length or size of the tree, that is, its number of nodes"""
    return len(list_of_nodes)
    
  def get_height(self):
    """Returns the height, that is, the distance from root to every leaf node"""
    # A perfect tree of height h has n = 2**(h + 1) - 1 nodes
    # So h is obtained as h = log2(n+1) - 1
    # This can be done with either math.log2 or bit_length, which on
    #powers of 2 returns one plus its logarithm in base 2
    return (len(self) + 1).bit_length() - 2

  @classmethod
  def generate_perfect_binary_tree(cls, height, data = None):
    r"""
    Generates an instance (of FrozenPerfectBinaryTree or subclass) of given height
    holding given data at every node.
    """
    # At the moment does not check if height is nonnegative integer
    # Produce a list of nodes such that the node in position 0 is the root
    #and such that the left and right child of the node in position idx
    #are at 2*idx + 1 and 2*idx + 2 respectively
    # Need to start node creation by the leaves and then go up
    number_of_nodes = 2**(height + 1) - 1
    list_of_nodes = [None]*number_of_nodes
    index_of_first_leaf = 2**height - 1
    for idx in reversed(range(number_of_nodes)):
      if idx >= index_of_first_leaf:
        list_of_nodes[idx] = FrozenBinaryTreeNode(data = data, left = None, right = None)
      else:
        left = list_of_nodes[2*idx + 1]
        right = list_of_nodes[2*idx + 2]
        list_of_nodes[idx] = FrozenBinaryTreeNode(data = data, left = left, right = right)
    frozen_perfect_binary_tree = cls(
        list_of_nodes = list_of_nodes,
        root = list_of_nodes[0],
        skip_checks = True)
    return frozen_perfect_binary_tree

  @classmethod
  def generate_perfect_binary_tree_of_empty_dicts(cls, height):
    """Creates a perfect binary tree holding empty dicts in every node."""
    return generate_perfect_binary_tree(cls, height, data = {})

class FrozenPerfectBinaryTreeOfDicts(FrozenPerfectBinaryTree, FrozenBinaryTreeOfDicts):
  """A frozen perfect binary tree having dictionaries as data in every node."""
  
  pass
  
class FrozenBinaryTreeNode():
  """A node in a FrozenBinaryTree"""
  
  def __init__(self, data, left = None, right = None):
    self.data = data
    self.left = left
    self.right = right
