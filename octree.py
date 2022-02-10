from typing import Union
import numpy as np

class OctreePoint:
    def __init__(self, min_xyz, max_xyz) -> None:        
        self.min_xyz = min_xyz
        self.max_xyz = max_xyz

        self.dxyz = self.max_xyz - self.min_xyz
        self.center = self.min_xyz + self.dxyz // 2
        self.size = abs(np.ceil(self.dxyz.max()))
        self.radius = self.size //2
        
        self.point_I    = self.center + self.radius
        self.point_II   = np.array([self.center[0]+self.radius,self.center[1]-self.radius,self.center[2]+self.radius])
        self.point_III  = np.array(list(self.center[:2] - self.radius) + list(self.center[2: ] + self.radius))
        self.point_IV   = np.array([self.center[0]-self.radius,self.center[1]+self.radius,self.center[2]+self.radius])
        self.point_V    = np.array(list(self.center[:2] + self.radius) + list(self.center[2: ] - self.radius))
        self.point_VI   = np.array([self.center[0]+self.radius,self.center[1]-self.radius,self.center[2]-self.radius])
        self.point_VII  = self.center - self.radius
        self.point_VIII = np.array([self.center[0]-self.radius,self.center[1]+self.radius,self.center[2]-self.radius])
        
        self.ocpoints = np.array([self.point_I,self.point_II,self.point_III,self.point_IV,self.point_V,self.point_VI,self.point_VII,self.point_VIII])

        self.cube_I    = np.stack([self.center,self.point_I],0)
        self.cube_II   = np.stack([self.center,self.point_II],0)
        self.cube_III  = np.stack([self.center,self.point_III],0)
        self.cube_IV   = np.stack([self.center,self.point_IV],0)
        self.cube_V    = np.stack([self.center,self.point_V],0)
        self.cube_VI   = np.stack([self.center,self.point_VI],0)
        self.cube_VII  = np.stack([self.center,self.point_VII],0)
        self.cube_VIII = np.stack([self.center,self.point_VIII],0)

        self.point_I_mask    = None
        self.point_II_mask   = None
        self.point_III_mask  = None
        self.point_IV_mask   = None
        self.point_V_mask    = None
        self.point_VI_mask   = None
        self.point_VII_mask  = None
        self.point_VIII_mask = None
        
        self.points_I    = None
        self.points_II   = None
        self.points_III  = None
        self.points_IV   = None
        self.points_V    = None
        self.points_VI   = None
        self.points_VII  = None
        self.points_VIII = None
        
        self.n_points_I    = 0
        self.n_points_II   = 0
        self.n_points_III  = 0
        self.n_points_IV   = 0
        self.n_points_V    = 0
        self.n_points_VI   = 0
        self.n_points_VII  = 0
        self.n_points_VIII = 0

        self.colors_I    = None
        self.colors_II   = None
        self.colors_III  = None
        self.colors_IV   = None
        self.colors_V    = None
        self.colors_VI   = None
        self.colors_VII  = None
        self.colors_VIII = None
        
    def point_in_cube(self, cube):
        if not self.points is None:
            return np.logical_and(np.logical_and(np.logical_and(cube[:,0].min()<self.points[:,0],self.points[:,0]<cube[:,0].max()),
                                                 np.logical_and(cube[:,1].min()<self.points[:,1],self.points[:,1]<cube[:,1].max())),
                                  np.logical_and(cube[:,2].min()<self.points[:,2],self.points[:,2]<cube[:,2].max()))

    def seperate_points(self, points):
        if not points is None:
            self.points = points
            self.n_points = len(self.points)
        
            self.point_I_mask    = self.point_in_cube(self.cube_I)
            self.point_II_mask   = self.point_in_cube(self.cube_II)
            self.point_III_mask  = self.point_in_cube(self.cube_III)
            self.point_IV_mask   = self.point_in_cube(self.cube_IV)
            self.point_V_mask    = self.point_in_cube(self.cube_V)
            self.point_VI_mask   = self.point_in_cube(self.cube_VI)
            self.point_VII_mask  = self.point_in_cube(self.cube_VII)
            self.point_VIII_mask = self.point_in_cube(self.cube_VIII)
            
            self.points_I = self.points[self.point_I_mask]
            self.points_II = self.points[self.point_II_mask]
            self.points_III = self.points[self.point_III_mask]
            self.points_IV = self.points[self.point_IV_mask]
            self.points_V = self.points[self.point_V_mask]
            self.points_VI = self.points[self.point_VI_mask]
            self.points_VII = self.points[self.point_VII_mask]
            self.points_VIII = self.points[self.point_VIII_mask]
            
            self.n_points_I    = len(self.points_I)
            self.n_points_II   = len(self.points_II)
            self.n_points_III  = len(self.points_III)
            self.n_points_IV   = len(self.points_IV)
            self.n_points_V    = len(self.points_V)
            self.n_points_VI   = len(self.points_VI)
            self.n_points_VII  = len(self.points_VII)
            self.n_points_VIII = len(self.points_VIII)
            
    def seperate_colors(self, colors):
        if not colors is None:
            self.colors = colors

            self.colors_I = self.colors[self.point_I_mask]
            self.colors_II = self.colors[self.point_II_mask]
            self.colors_III = self.colors[self.point_III_mask]
            self.colors_IV = self.colors[self.point_IV_mask]
            self.colors_V = self.colors[self.point_V_mask]
            self.colors_VI = self.colors[self.point_VI_mask]
            self.colors_VII = self.colors[self.point_VII_mask]
            self.colors_VIII = self.colors[self.point_VIII_mask]
            
    def create_cubes(self):
        if not self.points is None and not self.colors is None:
            self.I    = OctreePoint(self.points_I, self.colors_I)
            self.II   = OctreePoint(self.points_II, self.colors_II)
            self.III  = OctreePoint(self.points_III, self.colors_III)
            self.IV   = OctreePoint(self.points_IV, self.colors_IV)
            self.V    = OctreePoint(self.points_V, self.colors_V)
            self.VI   = OctreePoint(self.points_VI, self.colors_VI)
            self.VII  = OctreePoint(self.points_VII, self.colors_VII)
            self.VIII = OctreePoint(self.points_VIII, self.colors_VIII)

class OctreeNode:
    def __init__(self, val:OctreePoint, isLeaf:Union[bool,int], I=None, II=None, III=None, IV=None, V=None, VI=None, VII=None, VIII=None):
        self.val    = val
        self.isLeaf = isLeaf
        self.I      = I    # [+++]
        self.II     = II   # [+-+]
        self.III    = III  # [--+]
        self.IV     = IV   # [-++]
        self.V      = V    # [++-]
        self.VI     = VI   # [+--]
        self.VII    = VII  # [---]
        self.VIII   = VIII # [-+-]
        
    @property
    def cube_points(self):
        return self.val.ocpoints
    
    @property
    def cube_size(self):
        return self.val.size
    
    @property
    def cube_color(self):
        if self.isLeaf and len(self.val.colors) > 0:
            return self.val.colors.mean(0)
    
    @property
    def lines(self):
        return np.array([[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]])
    
    @property
    def line_colors(self):
        if self.isLeaf and len(self.val.colors) > 0:
            return np.tile(self.val.colors.mean(0),(12,1))
        return np.zeros((12,3),dtype=int)
    
    @property
    def cube_triangles(self):
        return np.array([[2,1,3],[3,1,0],# [III, IV, II], [IV,I,II] Forward
                         [3,0,7],[7,0,4],# [IV,VIII,I], [VIII,V,I] Top
                         [0,1,4],[4,1,5],# [I,V,II],[V,VI,II] Right
                         [1,2,5],[5,2,6],# [II,VI,III],[VI,VII,III] Bottom
                         [2,3,6],[6,3,7],# [III,VII,IV],[VII,VIII,IV] Left
                         [4,5,7],[5,6,7]])# [V,VI,VIII],[VI,VII,VIII] Back
        
class Octree:
    def __init__(self, points, colors=None, max_depth=1) -> None:
        min_xyz, max_xyz = points.min(0), points.max(0)
        self.root = self.create(points, min_xyz, max_xyz, colors, max_depth)
            
    def create(self, points, min_xyz, max_xyz, colors=None, depth=1):
        ocPoint = OctreePoint(min_xyz, max_xyz)
        ocPoint.seperate_points(points)
        ocPoint.seperate_colors(colors)
        if depth<1:
            return OctreeNode(ocPoint, 1)
        return OctreeNode(ocPoint,
                          0,
                          self.create(ocPoint.points_I,   ocPoint.center,ocPoint.point_I,   ocPoint.colors_I,   depth-1),
                          self.create(ocPoint.points_II,  ocPoint.center,ocPoint.point_II,  ocPoint.colors_II,  depth-1),
                          self.create(ocPoint.points_III, ocPoint.center,ocPoint.point_III, ocPoint.colors_III, depth-1),
                          self.create(ocPoint.points_IV,  ocPoint.center,ocPoint.point_IV,  ocPoint.colors_IV,  depth-1),
                          self.create(ocPoint.points_V,   ocPoint.center,ocPoint.point_V,   ocPoint.colors_V,   depth-1),
                          self.create(ocPoint.points_VI,  ocPoint.center,ocPoint.point_VI,  ocPoint.colors_VI,  depth-1),
                          self.create(ocPoint.points_VII, ocPoint.center,ocPoint.point_VII, ocPoint.colors_VII, depth-1),
                          self.create(ocPoint.points_VIII,ocPoint.center,ocPoint.point_VIII,ocPoint.colors_VIII,depth-1))

    def cubes(self):
        out = []
        self.traverse(self.root, lambda v: out.append(v) if not v is None else v)
        return out
        
    def traverse(self, node:OctreeNode, callback):
        if node is None:
            return
        if node.isLeaf:
            callback(create_cube(node))
        self.traverse(node.I, callback)
        self.traverse(node.II, callback)
        self.traverse(node.III, callback)
        self.traverse(node.IV, callback)
        self.traverse(node.V, callback)
        self.traverse(node.VI, callback)
        self.traverse(node.VII, callback)
        self.traverse(node.VIII, callback)
        
def create_cube(node:OctreeNode):
    mesh = o3d.geometry.TriangleMesh()
    if not node is None and node.isLeaf:
        if not node.cube_color is None:
            mesh.vertices = o3d.utility.Vector3dVector(node.cube_points)
            mesh.triangles = o3d.utility.Vector3iVector(node.cube_triangles)
            mesh.paint_uniform_color(node.cube_color)
            return mesh