# For varied utilities, currently tree structures

class FrozenTree():
  """A tree with frozen node structure (the nodes may be mutable)."""
  pass

class FrozenBinaryTree():
  r"""
  A tree with frozen node structure (the nodes may be mutable) and such that
  every node has at most 2 child nodes.
  """

  def __init__(self, list_of_nodes, root = None, skip_checks = False):
    # Currently assumes list of nodes is correct for a binary tree
    if not skip_checks:
      if not self.check_consistency_of_list_of_nodes(list_of_nodes)
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
    for node in list_of_nodes:
      if node.parent == None:
        root = node
        break
    return root
  
  def get_root(self):
    """Returns root of tree."""
    return self.root
  
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
