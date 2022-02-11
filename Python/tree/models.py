class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.map = {0:self.x,1:self.y}

    def __repr__(self) -> str:
        return f"[{self.x} {self.y}]"

    def __len__(self):
        return 2

    def __getitem__(self, i):
        if i < self.__len__():
            return self.map[i]
        raise StopIteration

    def __add__(self,p2):
        return Point((self.x+p2.x),(self.y+p2.y))

    def __sub__(self,p2):
        return Point((self.x-p2.x),(self.y-p2.y))

    def __size__(self):
        return (self.x**2+self.y**2)**0.5

    def __mul__(self, n):
        if isinstance(n,int) or isinstance(n,float):
            return Point(self.x*n,self.y*n)
        elif isinstance(n,Point):
            return Point(self.x*n.x,self.y*n.y)
        else:
            raise ValueError(f"Unsupport __mul__ input type {type(n)}")

    def astype(self, type):
        return Point(type(self.x),type(self.y))

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, v):
        if isinstance(v, float) or isinstance(v,int):
            self._x = v
        else:
            self._x = float(v)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, v):
        if isinstance(v,float) or isinstance(v,int):
            self._y = v
        else:
            self._y = float(v)

import xml.etree.ElementTree as ET

CIRCLE_TAG_NAME = '{http://www.w3.org/2000/svg}circle'
GROUP_TAG_NAME = '{http://www.w3.org/2000/svg}g'

class SVG:
    def __init__(self, svg_path) -> None:
        self.path = svg_path
        self.tree = self.read_svg(self.path)
    
    def read_svg(self, svg_path):
        return ET.parse(svg_path)
    
    def circle2point(self, circle:ET.Element):
        return Point(circle.attrib['cx'], circle.attrib['cy'])

    def get_points_from_group(self, group_id):
        return [c 
                for g in self.tree.iter(GROUP_TAG_NAME) if 'id' in g.attrib and g.attrib['id'] == group_id 
                for c in self.get_points(g)[0]]

    def get_specific_point(self, point_id):
        return [self.circle2point(c) for c in self.tree.iter(CIRCLE_TAG_NAME) if 'id' in c.attrib and c.attrib['id'] == point_id]

    def get_points(self, tree:ET.ElementTree):
        pts_map = {}
        pts = []
        for c in tree.iter(CIRCLE_TAG_NAME):
            pt = self.circle2point(c)
            if 'id' in c.attrib:
                pts_map[c.attrib['id']] = pt
            pts.append(pt)
        return pts, pts_map