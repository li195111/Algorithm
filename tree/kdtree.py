from models import SVG, Point

def distance_squared(point1, point2):
    return (point1[0]-point2[0])**2+(point1[1]-point2[1])**2

def closest_point(all_points, new_point):
    '''Time: O(n)
    '''
    best_point = None
    best_dist = None
    for cur_point in all_points:
        cur_dist = distance_squared(new_point, cur_point)
        if best_dist is None or cur_dist < best_dist:
            best_dist = cur_dist
            best_point = cur_point
    return best_point

class KDNode:
    def __init__(self, point:Point, left=None, right=None) -> None:
        self.point:Point = point
        self.left = left
        self.right = right
        
    def __repr__(self) -> str:
        lines, *_ = self._display_aux()
        return '\n'+'\n'.join(lines)+'\n'
    
    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.point.astype(int)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.point.astype(int)
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.point.astype(int)
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.point.astype(int)
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

def build_kdtree(points, k=2, depth=0):
    n = len(points)
    if n <= 0:return None
    axis = depth % k
    sorted_points = sorted(points, key=lambda point: point[axis])
    return KDNode(sorted_points[n//2],
                  build_kdtree(sorted_points[:n//2], depth=depth+1),
                  build_kdtree(sorted_points[n//2+1:], depth=depth+1))
    
def kdtree_naive_closest_point(root:KDNode, point, k=2, depth=0, best=None):
    '''Without consider the closer point of node.'''
    if root is None: return best
    axis = depth % k
    if best is None or distance_squared(point, best) > distance_squared(point, root.point): best = root.point
    if point[axis] < root.point[axis]: return kdtree_naive_closest_point(root.left, point, k, depth+1, best)
    else: return kdtree_naive_closest_point(root.right, point, k, depth+1, best)
    
def closer_distance(pivot, p1, p2):
    if p1 is None: return p2
    if p2 is None: return p1
    if distance_squared(pivot,p1) < distance_squared(pivot,p2): return p1
    else: return p2
    
def kdtree_closest_point(root:KDNode, point, k=2, depth=0):
    '''consider the closer point of node.'''
    if root is None: return None
    axis = depth % k
    next_branch = None
    opposite_branch = None
    if point[axis] < root.point[axis]:
        next_branch = root.left
        opposite_branch = root.right
    else:
        next_branch = root.right
        opposite_branch = root.left
    best = closer_distance(point,kdtree_closest_point(next_branch,point,k,depth+1),root.point)
    if distance_squared(point, best) > abs(point[axis] - root.point[axis]):
        best = closer_distance(point,kdtree_closest_point(opposite_branch,point,k,depth+1),best)
    return best

if __name__ == "__main__":
    import time
    svg_path = 'draw.svg'
    svg = SVG(svg_path)
    [pivot] = svg.get_specific_point('pivot')
    points = svg.get_points_from_group('points')
    
    print (f"Match       : {pivot} from {len(points)} points")
    st = time.time()
    method1 = closest_point(points, pivot)
    et = time.time()
    print (f"Loop        : {method1} Time cost: {et-st:.3f} sec")
    k = 2
    root = build_kdtree(points, k=k)
    # print (root)
    st = time.time()
    best = kdtree_naive_closest_point(root, pivot)
    et = time.time()
    print (f"KDTree naive: {best} Time cost: {et-st:.3f} sec")
    st = time.time()
    best = kdtree_closest_point(root, pivot)
    et = time.time()
    print (f"KDTree      : {best} Time cost: {et-st:.3f} sec")
    
    [ans] = svg.get_specific_point('closest')
    print (f"Ans         : {ans}")