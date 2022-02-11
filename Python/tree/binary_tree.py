class BTreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
    def __repr__(self) -> str:
        lines, *_ = self._display_aux()
        return '\n'+'\n'.join(lines)+'\n'
        
    def display(self):
        lines, *_ = self._display_aux()
        print('\n'+'\n'.join(lines)+'\n')
            
    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.val
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.val
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.val
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

class BTree:
    def __init__(self) -> None:
        self.root = None
    
    def __repr__(self) -> str:
        return self.root.__repr__()
        
    @classmethod
    def from_root(cls, root):
        tree = cls()
        tree.create(root)
        return tree
        
    def create(self, values):
        if values:
            l = 1
            self.root = BTreeNode(values[0])
            args = [self._insert_]
            for v in values[1:]:
                _, l, self.root = self.insert(v, self.root, l, args)
            
    def insert(self, value, node:BTreeNode, l=None, args=[]):
        if not l:
            l = 1
        if not args:
            args = [self._insert_]
        r = args[0](value, node, *args[1:])
        while not r:
            args = [self._insert] + args
            r = args[0](value, node, *args)
            l += 1
        return r, l, node

    def _insert(self, v, node:BTreeNode, fn, *args):
        if not node is None and not node.val is None:
            r = fn(v, node, *args if args else [])
            if not r:
                r = fn(v, node.left, *args if args else [])
            if not r:
                r = fn(v, node.right, *args if args else [])
            return r

    def _insert_(self, value, node:BTreeNode):
        if not node is None and not node.val is None:
            if node.left is None:
                node.left = BTreeNode(value)
                return node
            if node.right is None:
                node.right = BTreeNode(value)
                return node
    
    @property
    def diameter(self):
        self.ans = 0
        self.diameters = {}
        self._diameter(self.root)
        return self.ans
            
    def _diameter(self,node:BTreeNode):
        if (not node is None) and (not node.val is None):
            l = self._diameter(node.left)
            r = self._diameter(node.right)
            if (not node.left is None) and (not node.left.val is None):
                l = self.diameters[node.left] + 1
            if (not node.right is None) and (not node.right.val is None):
                r = self.diameters[node.right] + 1
            self.diameters[node] = max([l,r])
            ans = sum([l,r])
            self.ans = max([self.ans,ans])
            return ans
        return 0

    @property
    def preorder(self):
        out = []
        self._preorder_traverse(self.root, lambda v:out.append(v))
        return out
    
    @property
    def inorder(self):
        out = []
        self._inorder_traverse(self.root, lambda v:out.append(v))
        return out
    
    @property
    def postorder(self):
        out = []
        self._postorder_traverse(self.root, lambda v:out.append(v))
        return out

    def _preorder_traverse(self,node:BTreeNode,callback):
        if node is None:
            return
        callback(node.val)
        self._preorder_traverse(node.left,callback)
        self._preorder_traverse(node.right,callback)

    def _inorder_traverse(self,node:BTreeNode,callback):
        if node is None:
            return
        self._inorder_traverse(node.left,callback)
        callback(node.val)
        self._inorder_traverse(node.right,callback)
        
    def _postorder_traverse(self,node:BTreeNode,callback):
        if node is None:
            return
        self._postorder_traverse(node.left,callback)
        self._postorder_traverse(node.right,callback)
        callback(node.val)
