########################################################################
# DOCUMENTATION / README
########################################################################

# File belonging to software package "homemade_financial_instruments"
# Implements financial instruments and solutions for pricing and hedging.

# For more information on functionality, see README.md
# For more information on bugs and planned features, see ISSUES.md
# For more information on versioning, see RELEASES.md

# Copyright (C) 2023 Eduardo Fischer

# This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License version 3
#as published by the Free Software Foundation. See LICENSE.
# Alternatively, see https://www.gnu.org/licenses/.

# This program is distributed in the hope that it will be useful,
#but without any warranty; without even the implied warranty of
#merchantability or fitness for a particular purpose.

########################################################################

# For tree structures, focusing on binary (and some perfect) trees

########################################################################

from ..utilities import *
from ..formulas import *

class FrozenTree():
  r"""
  A tree with frozen node structure (the nodes may have mutable data).
  
  There is a specific root, and the nodes can have any number of children.
  
  There should be methods (implemented in subclasses, as abstract methods):
  
  get_root, to obtain the root of the tree
  get_list_of_nodes, to obtain a list of all nodes in the tree
  get_list_of_children_of_node_in_tree, to get a list of children of a given node in tree
  get_parent_of_node_in_tree, to get the parent of a node in the tree (or None)
  """

  def __len__(self):
    """Returns the length or size of the tree, that is, its number of nodes"""
    return len(self.get_list_of_nodes())

  def reset_all_nodes_to_specific_data(self, data = None):
    """Changes the data of all nodes to be the specified data."""
    for node in self.get_list_of_nodes():
      nodes.data = data
    return None
  
  def reset_all_nodes_to_dict_with_given_keys(self, keys):
    """Puts a dictionary with given keys (corresponding values being None) at every node."""
    new_dict = {}
    for key in keys:
      new_dict[key] = None
    self.reset_all_nodes_to_specific_data(new_dict)
    return None
    
  def reset_all_nodes_to_empty_dictionary(self):
    """Puts an empty dictionary as data of every node."""
    self.reset_all_nodes_to_dict_with_given_keys([])
    return None

class FrozenBinaryTree(FrozenTree):
  r"""
  A tree with frozen node structure (the nodes may have mutable data)
  and such that every node has at most 2 child nodes, named left and
  right nodes. In case there is a single one, it is specified whether
  it is a left or right child.
  
  Instance stores a dictionary of left-right addresses of nodes. That is,
  a dictionary whose keys are strings whose only characters are 'l' or 'r'
  (including the empty string), and whose values are the nodes (instances
  of FrozenBinaryTreeNode) which are the destination if one follows the
  instructions contained on the key starting at the root node ('l' for
  taking left child, 'r' for taking right child). 
  """

  def __init__(
      self,
      autodetected_initialization_argument = None,
      left_right_addresses = None,
      root = None,
      list_of_nodes = None,
      skip_checks = False,
      forbid_picking_nodes_from_other_trees = False):
    r"""
    Can be initialized with either (a single one of them):
    a dict of left-right addresses;
    or a single node representing the root;
    or a list of all nodes
    
    Nodes are typically BinaryNode instances which are transformed into
    FrozenBinaryTreeNode instances for storage in the tree.
    
    Some checks might be performed to assure a tree is indeed formed with
    a given list of nodes or of left-right addresses. The variable
    skip_checks can be set to True so the checks are not executed.
    
    forbid_picking_nodes_from_other_trees argument is passed to
    create_frozenbinarytreenode_from_binarynode method which is called
    during initialization
    """
    if auto_detected_initialization_argument:
      if auto_detected_initialization_argument is None:
        pass
      elif isinstance(auto_detected_initialization_argument, (BinaryNode, FrozenBinaryTreeNode)):
        root = autodetected_initialization_argument
      elif isinstance(auto_detected_initialization_argument, dict):
        left_right_addresses = autodetected_initialization_argument
      elif isinstance(auto_detected_initialization_argument, list):
        list_of_nodes = autodetected_initialization_argument
      else:
        raise ValueError('Could not autodetect given initialization argument')
    # If root or left_right_addresses is given it helps the process
    if root or left_right_addresses:
      if left_right_addresses:
        self.left_right_addresses = left_right_addresses
        root_based_on_lra = self.left_right_addresses['']
        if not skip_checks:
          if (root is not None) and (root is not root_based_on_lra):
            raise('Info on given root and left-right addresses does not match')
        root = root_based_on_lra
        if not skip_checks:
          # Need to also ensure FrozenBinaryTreeNodes are produced and correct
          # Also need to take special care about 
          self.ensure_consistency_of_left_right_addresses(
              addresses,
              require_match_of_address_and_path = True,
              forbid_picking_nodes_from_other_trees = False,
              require_perfectness = False,
              require_dicts_as_data_of_nodes = False)
      else:
        # In this case root was given but not left_right_addresses
        self.left_right_addresses = self.obtain_left_right_addresses_from_root(root)
      # All left to do is maybe ensure list_of_nodes, if also given, was correct
      if not skip_checks:
        pass
        ##############
        # WORK HERE
        ##############
    # Harder case below, where no root or left_right_addresses is given
    elif list_of_nodes:
      # Will always check for a single root
      if not skip_checks:
        if not self.check_consistency_of_list_of_nodes(
            list_of_nodes = list_of_nodes,
            require_perfectness = False):
          raise ValueError('Given nodes cannot form a binary tree.')
      self.list_of_nodes = list_of_nodes
      # Shortcut for root insertion
      if skip_checks and root is not None:
        self.root = root
      else:
        computed_root = self.obtain_root_from_node_list(list_of_nodes)
        if root is None:
          self.root = computed_root
        else:
          # In this case root is not None and skip_checks is False
          if root == computed_root:
            self.root = computed_root
          else:
            raise ValueError('Given root is not root of given list of nodes')
    else:
      raise ValueError('Needs left-right addresses, root or list of nodes to build instance')

  @classmethod
  def create_node_with_path_information(
      cls,
      node,
      path,
      skip_checks = False,
      forbid_picking_nodes_from_other_trees = False,
      produce_loose_nodes_instead = False):
    r"""
    Creates a FrozenBinaryTreeNode using data, left and right attributes
    from given node, and adds correct path information (in the context
    of a nonspecified binary tree) to the new node.
    
    The tree is not specified because this is typically called during
    the initialization, while its methods and attributes are not fully
    functional.
    
    If forbid_picking_nodes_from_other_trees is True, then nodes must be
    given as BinaryNode instances. If False, it can accept nodes as
    FrozenBinaryTreeNodes from other trees (erasing and ignoring the
    previous path attribute).
    
    Unless skip_checks is True, will ensure only the correct characters
    appear in the path.
    
    Setting produce_loose_nodes_instead to True will create a new BinaryNode
    instance, which does not have path/address information and clearly
    is not a FrozenBinaryTreeNode. It might be a little contradictory
    with the name of the method but it is allowed and can be useful for
    some purposes.
    """
    if forbid_picking_nodes_from_other_trees:
      if isinstance(node, FrozenBinaryTreeNode):
        raise TypeError('Want loose binary node (not in another tree)')
    if not skip_checks:
      if path.count('l') + path.count('r') != len(path):
        raise ValueError('Given path has characters other than \'l\' and \'r\'')
    if produce_loose_nodes_instead:
      node_in_tree = BinaryNode(
          data = node.data,
          left = node.left,
          right = node.right)
    else:
      node_in_tree = FrozenBinaryTreeNode(
          data = node.data,
          left = node.left,
          right = node.right,
          path = path)
    return node_in_tree

  @classmethod
  def check_consistency_of_anything_class_version(cls, method_name, *args, **kwargs):
    """
    Returns a Boolean for whether arguments pass the method (without errors).
    
    Method can be a class or static method.
    """
    try:
      method = getattr(cls, method_name)
      method(*args, **kwargs)
    except TypeError, ValueError: # Possible errors for use cases
      return False
    return True

  def check_consistency_of_anything_instance_version(self, method_name, *args, **kwargs):
    """
    Returns a Boolean for whether arguments pass the method (without errors).
    
    Method can be an instance, class or static method of self.
    """
    try:
      method = getattr(self, method_name)
      method(*args, **kwargs)
    except TypeError, ValueError: # Possible errors for use cases
      return False
    return True

  @classmethod
  def check_consistency_of_left_right_addresses(cls, *args, **kwargs):
    r"""
    Returns a Boolean for whether arguments pass (without errors)
    ensure_consistency_of_left_right_addresses.
    """
    return cls.check_consistency_of_anything_class_version(
        'ensure_consistency_of_left_right_addresses', *args, **kwargs)
    
  @classmethod
  def ensure_consistency_of_left_right_addresses(
      cls,
      addresses,
      require_match_of_address_and_path = False,
      forbid_picking_nodes_from_other_trees = False,
      require_perfectness = False,
      require_dicts_as_data_of_nodes = False):
    r"""
    Ensures nodes form a binary tree.
    
    Returns None if everything is okay, or otherwise raise an Error.
    
    Works like ensure_consistency_of_list_of_nodes, but on a dict of
    left-right addresses.
    
    Has an option require_match_of_address_and_path, which if True, will
    require the correct path/address information (called address, a key
    of the dict) is already stored in the path attribute of the node.
    """
    # First ensure the correctness of the keys
    for key in addresses:
      if not isinstance(key, str) or key.count('l') + key.count('r') != len(key):
        raise ValueError('Keys can only have \'l\' and \'r\' characters')
    if require_perfectness:
      # There is an easy way based on the length of the addresses
      max_key_length = max(len(key) for key in addresses)
      if len(addresses) != 2**(max_key_length + 1) - 1:
        raise ValueError('Nodes do not form a perfect binary tree')
    if forbid_picking_nodes_from_other_trees:
      # Note: have no way to detecting what it means to be "other" tree
      #if the paths are correctly given for each node object
      # And so, the check is whether the nodes are indeed loose, that is,
      #BinaryNodes, or whether they are FrozenBinaryTreeNodes but every
      #single path information matches with the dict key
      for key, node in addresses.items():
        if isinstance(node, FrozenBinaryTreeNode) and (not hasattr(node, 'path') or node.path != key):
          raise ValueError('Nodes appear to have path information about from another tree')
    if require_match_of_address_and_path:
      # In this case require a FrozenBinaryTreeNode with matching path
      for key, node in addresses.items():
        if not hasattr(node, 'path') or node.path != key:
          raise ValueError('Nodes\' path information doesn\'t match address in dict key')
    if require_dicts_as_data_of_nodes:
      for node in addresses.values():
        if not isinstance(node.data, dict):
          raise ValueError('Nodes are expected to have dicts for their data')
    # Easiest way to check if there is a single parentless node:
    # In a tree of n nodes there are n-1 parent-child relationships
    # Absent circularity (which is impossible with the addresses dict due
    #to how the addresses increase as one moves away from the root), this
    #is enough to ensure tree-ness (provided the addresses of parent and
    #child have the correct relationship)
    number_parent_child_relationships = 0
    for key, node in addresses.items():
      if node.left is not None:
        number_parent_child_relationships += 1
        should_be_address_of_child = key + 'l'
        if not addresses[should_be_address_of_child] == node.left:
          raise ValueError('Incorrect parent-left child relationship in dict')
      if node.right is not None:
        number_parent_child_relationships += 1
        should_be_address_of_child = key + 'r'
        if not addresses[should_be_address_of_child] == node.right:
          raise ValueError('Incorrect parent-right child relationship in dict')
    if number_parent_child_relationships != len(addresses) - 1:
      if return_boolean_instead_of_potentially_raising_error:
        return False
      else:
        raise ValueError('Cannot form a unified tree with nodes in dict')
    else:
      return None

  @classmethod
  def check_consistency_of_list_of_nodes(cls, *args, **kwargs):
    r"""
    Returns a Boolean for whether arguments pass (without errors)
    ensure_consistency_of_list_of_nodes.
    """
    return cls.check_consistency_of_anything_class_version(
        'ensure_consistency_of_list_of_nodes', *args, **kwargs)

  @classmethod
  def ensure_consistency_of_list_of_nodes(
      cls,
      list_of_nodes,
      forbid_picking_nodes_from_other_trees = False,
      require_perfectness = False,
      require_dicts_as_data_of_nodes = False,
      return_boolean_instead_of_potentially_raising_error = False):
    r"""
    Ensures nodes form a binary tree.
    
    Returns None if everything is okay, otherwise raises an Error.
    
    That is, there should be a single root, and the tree should be closed
    for the operations of taking the left or the right child.
    
    If forbid_picking_nodes_from_other_trees is True, requires all nodes
    to be "loose", that is, BinaryNode instances.
    
    If require_perfectness is True, will also check if nodes form a perfect
    binary tree.
    
    If require_dicts_as_data_of_nodes is True, will also check if the
    data in all nodes is a dict.
    """
    # Checks if there is are n-1 parent-child relationships for n nodes
    # Does not check absence of circularity (equivalent to connectedness
    #if number of parent-child relationships is right), and thus is not
    #a complete check
    relationships = 0
    for node in list_of_nodes:
      if node.left is not None:
        relationships += 1
      if node.right is not None:
        relationships += 1
    if relationships != len(list_of_nodes) - 1:
      if return_boolean_instead_of_potentially_raising_error:
        return False
      else:
        raise ValueError('List of nodes has the wrong number of parent-child relationships')
    if return_boolean_instead_of_potentially_raising_error:
      return True
    else:
      return None

  @classmethod
  def check_consistency_of_list_of_nodes_against_addresses(cls, *args, **kwargs):
    r"""
    Returns a Boolean for whether arguments pass (without errors)
    ensure_consistency_of_list_of_nodes_against_addresses.
    """
    return cls.check_consistency_of_anything_class_version(
        'ensure_consistency_of_list_of_nodes_against_addresses', *args, **kwargs)

  @classmethod
  def ensure_consistency_of_list_of_nodes_against_addresses(
      cls, list_of_nodes, addresses):
    r"""
    Ensures a list of nodes have equivalent information to a dict of
    left-right addresses.
    
    Returns None if everything is okay, otherwise raises an Error.
    
    The dict of left-right addresses is assumed consistent.
    """
    # Given that there is no hashing, there is no other way than simply
    #matching the objects one-by-one, starting by the length to simplify
    # Work is O(n^2)
    if len(list_of_nodes) != len(addresses):
      if return_boolean_instead_of_potentially_raising_error:
        return False
      else:
        raise ValueError('List of nodes and dict of addresses have different lengths')
    for node in addresses.values():
      node_found_in_list = False
      for idx, other_node in enumerate(list_of_nodes):
        if node is other_node:
          node_found_in_list = True
          if idx == 0:
            list_of_nodes = list_of_nodes[1:]
          elif idx == len(list_of_nodes) - 1:
            list_of_nodes = list_of_nodes[:len(list_of_nodes) - 1]
          else:
            list_of_nodes = list_of_nodes[:idx-1] + list_of_nodes[idx+1:]
          break
      if not node_found_in_list:
        if return_boolean_instead_of_potentially_raising_error:
          return False
        else:
          raise ValueError('List of nodes and dict of addresses have different nodes')
    # All clear
    if return_boolean_instead_of_potentially_raising_error:
      return True
    else:
      return None

  @classmethod
  def obtain_parentless_nodes_from_node_list(cls, list_of_nodes):
    """Returns list of parentless nodes from a list of loose nodes."""
    # Without hashing to use sets or dicts, not path/address information,
    #this is highly inefficient, O(n^2) time
    nodes_with_parents = []
    for node in list_of_nodes:
      left = node.left
      right = node.right
      if left is not None:
        known_non_roots.append(node.left)
      if right is not None:
        known_non_roots.append(node.right)
    parentless_nodes = []
    for node in list_of_nodes:
      if node not in nodes_with_parents:
        parentless_nodes.append(node)
    return parentless_nodes
    
  @classmethod
  def obtain_root_from_node_list(cls, list_of_nodes, skip_checks = False):
    r"""
    Returns root from list of nodes.
    
    Raises error if more than one root (that is, more than one parentless
    node) is found.
    
    Other checks might be run (ensure tree closed under right and left child
    operations), depending on skip_checks variable.
    """
    if not skip_checks:
      cls.ensure_consistency_of_list_of_nodes(
          list_of_nodes,
          forbid_picking_nodes_from_other_trees = False,
          require_perfectness = False,
          require_dicts_as_data_of_nodes = False)
    parentless_nodes = cls.obtain_parentless_nodes_from_node_list(list_of_nodes)
    if len(parentless_nodes) == 1:
      return parentless_nodes[0]
    else:
      raise ValueError('There is no single parentless node in list.')

  @classmethod
  def obtain_left_right_addresses_from_root(cls, root,
      skip_checks = False, produce_loose_nodes_instead = False):
    r"""
    Produces a left-right address dict for descendants of given root.
    
    Produces FrozenBinaryTreeNodes by default, with the root to be made
    parentless and all other parents sets correctly. However, if
    produce_loose_nodes_instead is set to True then it produces BinaryNodes
    (without information of parentage).
    """
    addresses = {}
    def add_node_and_descendants_as_addresses(addesses, current_node, current_path, current_parent):
      # Updates node according to specifications
      current_node = cls.create_node_with_path_information(
          node = current_node,
          path = current_path,
          skip_checks = skip_checks,
          forbid_picking_nodes_from_other_trees = forbid_picking_nodes_from_other_trees,
          produce_loose_nodes_instead = produce_loose_nodes_instead)
      addesses[current_path] = current_node
      left = current_node.left
      right = current_node.right
      if left is not None:
        add_node_and_descendants_as_addresses(
            addresses = addresses,
            current_node = left,
            current_path = current_path + 'l',
            current_parent = current_node)
      if right is not None:
        add_node_and_descendants_as_addresses(
            addresses = addresses,
            current_node = right,
            current_path = current_path + 'r',
            current_parent = current_node)
    # A single call and addresses will be recursively updated
    add_node_and_descendants_as_addresses(
        addresses = addresses,
        current_node = root,
        current_path = '',
        current_parent = None)
    return addresses

  @classmethod
  def recreate_left_right_addresses_with_addressed_nodes(cls, addresses,
      skip_checks = False, forbid_picking_nodes_from_other_trees = False):
    r"""
    Given dict of left-right addresses with loose nodes, will recreate
    the same dict but with FrozenBinaryTreeNodes with correct paths.
    
    The tree is not specified because this is typically called during
    the initialization, while its methods and attributes are not fully
    functional.
    
    Depending on skip_checks, may raise error if dict is inconsistent
    (i. e. information does not allow for constructing a tree).
    
    Passes forbid_picking_nodes_from_other_trees argument to submethod.
    """
    if not skip_checks:
      cls.ensure_consistency_of_left_right_addresses(
          addresses = addresses,
          require_match_of_address_and_path = False,
          forbid_picking_nodes_from_other_trees = forbid_picking_nodes_from_other_trees,
          require_perfectness = False,
          require_dicts_as_data_of_nodes = False)
    new_addresses = {}
    for address, node in addresses.items():
      new_node = cls.create_node_with_path_information(
          node = node,
          path = address,
          skip_checks = skip_checks,
          forbid_picking_nodes_from_other_trees = forbid_picking_nodes_from_other_trees,
          produce_loose_nodes_instead = False)
      new_addresses[address] = new_node
    return new_addresses
  
  def get_lra(self):
    """Alias for get_left_right_addresses."""
    return self.get_left_right_addresses()
    
  def get_left_right_addresses(self):
    """Returns left-right addresses dict of the tree."""
    return self.left_right_addresses
  
  def get_root(self):
    """Returns root of tree."""
    return self.get_lra()['']
    
  def get_parent_of_node_in_tree(self, node):
    """Returns parent of node in tree, or None if node is the root of the tree."""
    path_of_node = node.path
    if path_of_node == '':
      return None
    else:
      path_of_parent = path_of_node[:-1]
      return self.get_lra()[path_of_parent]
    
  def get_left_child_of_node_in_tree(self, node):
    """Returns left child of node, or None if it does not exist."""
    return node.left
    
  def get_right_child_of_node_in_tree(self, node):
    """Returns right child of node, or None if it does not exist."""
    return node.right
  
  def get_list_of_children_of_node_in_tree(self, node):
    """Returns a list with left and right child of node respectively."""
    # Done this way to be consistent with non-binary trees in case they
    #are implemented in the future
    return [
        self.get_left_child_of_node_in_tree(),
        self.get_right_child_of_node_in_tree()]
    
  def navigate_tree_by_string(self, node, string, ignore_error_if_string_has_invalid_chars = False,
      ignore_error_if_navigation_leads_to_none = False):
    r"""
    Given an initial node and a string made with the characters 'p', 'l' and 'r'
    will produce the node obtaining from the operations of successfuly
    taking parent (for 'p') or left child (for 'l') or right child (for 'r')
    starting from the initial given node.
    
    Will ignore capitalization.
    
    Has option to allow for staying in place if a 'p', 'l' or 'r' instruction
    is provided which would lead to no node. This is potentially dangerous
    and lead to unexpected results but is left as an option.
    
    Also allow for deciding on whether to raise an error or ignore when
    there are characters which are not 'p', 'l' or 'r'.
    """
    string = string.lower()
    current_node = node
    for char in string:
      if char == 'p':
        putative_next_node = self.get_parent_of_node_in_tree(current_node)
      elif char == 'l':
        putative_next_node = self.get_left_child_of_node_in_tree(current_node)
      elif char == 'r':
        putative_next_node = self.get_right_child_of_node_in_tree(current_node)
      else:
        if not ignore_error_if_string_has_invalid_chars:
          raise ValueError('String should contain only \'p\', \'l\' and \'r\'.')
        else:
          pass
      # Every new potential node needs to be checked if it is a node in tree
      if putative_next_node is not None:
        current_node = putative_next_node
      else:
        if not ignore_error_if_navigation_leads_to_none:
          raise ValueError('Cannot follow path for navigation inside tree.')
        else:
          # current_node stays as it is for this loop iteration,
          #exactly as if that char instruction has been simply ignored
          pass
    return current_node
    
  def print_tree_in_lines(self, box_length, box_heigh, horizontal_space,
      vertical_space):
    r"""
    Prints the binary tree in lines, such that the root is at the top,
    and each left and right child of a node are positioned below that
    node (at the left and at the right, respectively).
    
    Each node will be printed to a "box of characters", taking
    box_length and box_height as arguments for length and height, with
    an appropriate whitespace.
    
    The space between two neighbor leaf nodes (i. e. left and right
    child of a certain node) is specified by an argument,
    horizontal_space. It must be a positive integer.
    
    The distance between two lines is also controlled by an argument,
    vertical_space. It must be a positive integer.
    
    The box length is always an integer. If it is a positive value,
    the box of characters will have that length horizontally.
    If it is 0, it will find the maximum length among all possible boxes.
    A negative value raises an error.
    
    The box height may be given as a positive integer, case in which
    the data in the node will be printed in that number of lines (with
    appropriate whitespace of course). It can also be given as a list,
    case in which the height is the length of the list, and the value
    for each item as key in that node's data will be printed. That is,
    each item is looked up using "node.data[item]", what is specially
    fitting for a FrozenBinaryTreeOfDicts. Any other value raises an error.
    """
    #############
    # WORK HERE
    #############
    pass
    

class FrozenBinaryTreeOfDicts(FrozenBinaryTree):
  """A frozen binary tree having dictionaries as data in all nodes."""

  def compute_formula_at_nodes(self, output_key, formula_on_dicts, all_other_args,
      restrict_computation_to_root = False, restrict_computation_to_leaves = False):
    r"""
    Uses a formula to create or update a value for a dictionary key which
    will be present in a dictionary in every node of the tree.
    
    A formula is given which computes a dictionary value at a node based
    on other dictionary values at the same node.
    
    More specifically, it uses a FormulaOnDicts with named keyword dict
    arguments called `very_node_dict` (which receives the `data` attribute of
    the node being altered, necessarily a dict) and `all_other_args`.
    
    Has an option to only work at the root of the tree, or alternatively
    work only at the leaves, leaving the rest of the tree intact.
    """
    if restrict_computation_to_root and restrict_computation_to_leaves:
      raise ValueError('Cannot restrict simultaneously to root and to leaves')
    elif restrict_computation_to_root:
      nodes_to_act_on = [self.get_root()]
    elif restrict_computation_to_leaves:
      is_leaf = lambda x: x.left is None and x.right is None
      nodes_to_act_on = filter(is_leaf, self.list_of_nodes)
    else:
      nodes_to_act = self.list_of_nodes
    for node in nodes_to_act_on:
      kwargs = {
          'very_node_dict': node.data,
          'all_other_args': all_other_args}
      new_value_for_output_key = formula_on_dicts.call(**kwargs)
      node.data[output_key] = new_value_for_output_key

  def propagate_formula_up(self, output_key, formula_on_dicts, all_other_args):
    r"""
    Uses a formula to create or update a value for a dictionary key at
    each node. It changes the instance itself, returning None.
    
    A formula is given which computes the value of that dict key at that node
    based on the data of its left and right children.
    
    The formula does not need to provide a way to compute the value at
    the leaves, but it is assumed they are computed in another way.
    
    More specifically, it uses a FormulaOnDicts with named
    keyword dict arguments called `very_node_dict`, `left_child_dict`,
    `right_child_dict` and `all_other_args`. The result of the formula
    will alter the output key of the very node.
    """
    pass
    
  def propagate_formula_down(self, output_key, formula_on_dicts, almost_all_other_args):
    r"""
    Uses a formula to create or update a value for a dictionary key at
    each node. It changes the instance itself, returning None.
    
    A formula is given which computes the value of that dict key at that node
    based on the data of its parent (and whether it is the left or right
    child node).
    
    The formula does not need to provide a way to compute the value at
    the root, but it is assumed it is already computed in another way.
    
    More specifically, it uses a FormulaOnDicts with named keyword dict
    arguments called `parent_dict`, `relevant_child_dict`, and `all_other_args`.
    
    The dict `all_other_args` must have an added keys compared to
    `almost_all_other_args` named 'is_it_left_instead_of_right', which
    tells whether the node in question, whose `output_key` value is being
    created or altered, is the left or the right child of its parent,
    as well as an added key `is_it_root` which is true only on the root.
    """
    if 'is_it_left_instead_of_right' in almost_all_other_args:
      raise ValueError('Left and right info cannot be given early')
    def depth_first_search(
        self,
        current_node,
        formula_on_dicts,
        almost_all_other_args):
      # Each iteration produces the correct `output_key` corresponding
      #value for left and right node of `current_node`
      list_of_children_and_boolean = [
          (current_node.left, True),
          (current_node.right, False)]
      for child_node, is_it_left_instead_of_right in list_of_children_and_boolean:
        if child_node is not None:
          all_other_args = {'is_it_left_instead_of_right': is_it_left_instead_of_right}
          all_other_args.update(almost_all_other_args)
          new_output_value = formula_on_dicts(
              parent_dict = current_node.data,
              relevant_child_dict = child_node.data,
              all_other_args = all_other_args)
          child_node[output_key] = new_output_value
          depth_first_search(
              self,
              child_node,
              formula_on_dicts,
              almost_all_other_args)
      return None # Alters each node, returning None
    current_node = self.get_root()
    depth_first_search(
        self,
        current_node,
        formula_on_dicts,
        almost_all_other_args)

class FrozenPerfectBinaryTree(FrozenBinaryTree):
  """A FrozenBinaryTree of constant height [distance from leafs to root]."""

  def __init__(self, list_of_nodes = None, root = None, skip_checks = False):
    if not skip_checks:
      if not self.check_consistency_of_list_of_nodes(
          list_of_nodes = list_of_nodes,
          require_perfectness = True):
        raise ValueError('Given nodes cannot form a perfect binary tree.')
    super().__init__(list_of_nodes = list_of_nodes, root = root, skip_checks = True)
    
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

class BinaryNode():
  r"""
  A classical binary node, with data, left and right attributes.
  
  Following the typical convention for trees and nodes, there is no
  parentage/path/address information stored with the object itself.
  This is consistent with the fact that a BinaryNode can be the root of
  a tree of itself with its children, and can also be a non-root node
  in a larger tree (if any other node has the instance as left or right
  child), and so there is no intrinsic parent information for a loose node.
  
  When used as a node in the context of a specific FrozenBinaryTree,
  the information of the instance will be passed (along with correct
  parentage information as determined by the path attribute) to a new
  FrozenBinaryTreeNode instance.
  """
  
  def __init__(self, data, left = None, right = None):
    self.data = data
    self.left = left
    self.right = right
    # Note: typically there is no information about the parent of a node
    #in the node itself. This convention is maintained here
    # When within a FrozenBinaryTree, should be transformed into a
    #FrozenBinaryTreeNode to include parent information

class FrozenBinaryTreeNode():
  r"""
  A node in a FrozenBinaryTree, which is the typical context where an
  instance is expected to be created.
  
  Has information on its position/place/path/address within the tree
  (stored as path attribute), plus its left child and its right child,
  (None if any of those doesn't exist) stored in attributes. Also
  contains data in an attribute.
  """
  
  def __init__(self, data, left = None, right = None, parent = None):
    self.data = data
    self.left = left
    self.right = right
    self.path = path
    
  def produce_equivalent_loose_binary_node(self):
    r"""
    Produces the corresponding loose node, that is, the BinaryNode with
    same data, left and right attributes (with path forgotten).
    """
    return BinaryNode(self.data, self.left, self.right)

    
