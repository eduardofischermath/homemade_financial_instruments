# For tree structures, focusing on binary (and may complete) trees

########################################################################

from worlds import *
from formulas import *

class FrozenTree():
  """A tree with frozen node structure (the nodes may be mutable)."""
  pass

class FrozenBinaryTree():
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

  def reset_all_nodes_to_value(self, value = None):
    """Changes the values of all nodes to be the specified value."""
    for node in self.list_of_nodes:
      nodes.value = value
      
  def compute_formula_at_nodes(self, formula):
    r"""
    Uses a formula to create a value for a dictionary key which
    will be present in a dictionary in every node of the tree.
    
    A formula is given which computes a dictionary value at a node based
    on other dictionary values at the same node.
    """
    pass

  def propagate_formula_up(self, formula):
    r"""
    Uses a formula to create a value for a dictionary key which
    will be present in a dictionary in every node of the tree.
    
    A formula is given which computes the value of a node based on the
    values of its left and right children. The formula should also
    provide a way to compute the value at the leaves.
    """
    pass
    
  def propagate_formula_down(self, formula):
    r"""
    Uses a formula to create a value for a dictionary key which
    will be present in a dictionary in every node of the tree.
    
    A formula is given which computes the value of a node based on the
    values of its parent (and whether it is the left or right child node).
    The formula should also a way to compute the value at the root.
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
  
  def __init__(self, value, parent = None, left = None, right = None):
    # By definition left and right must be both None or both non-None
    # (Currently the requirement is not enforced)
    self.value = value
    self.parent = parent
    self.left = left
    self.right = right
