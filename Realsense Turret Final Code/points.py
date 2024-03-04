import numpy as np
from dataclasses import dataclass, field

# FRAME_RATE = 30
# TIME_DELTA = float(1/FRAME_RATE)

@dataclass(frozen=True)
class Point:
    coordinates: None
    dimension: int = field(init=False)

    def __post_init__(self):
        pos = self.coordinates
        object.__setattr__(self, 'coordinates', dict())
        if type(pos) == tuple or type(pos) == list:
            for n,p in enumerate(pos):
                self.coordinates['a'+str(n)] = p
            object.__setattr__(self, 'dimension', len(self.coordinates))
        elif type(pos) == dict:
            for label,value in pos.items():
                self.coordinates[label] = value
            object.__setattr__(self, 'dimension', len(self.coordinates))
        else:
            raise TypeError('Invalid object type for Point.coordinates. Must be of tuple, list, or dict.').with_traceback()

    def __add__(self, other):
        """
        Returns a Point which is the vector addition between the two points
        """
        if type(other) != Point:
            raise TypeError("Invalid type. Both objects must be of Point.")
        if self.dimension != other.dimension:
            raise Exception(f"Incorrect dimensions.")
        if self.coordinates.keys() != other.coordinates.keys():
            raise Exception(f"Differing dimension labels.")
        coords = dict()
        for j,k in zip(self.coordinates.keys(), other.coordinates.keys()):
            coords[j] = (self.coordinates[j] + other.coordinates[k])
        return Point(coords)
    
    def __sub__(self, other):
        """
        Returns a Point which is the vector difference between the two points
        """
        if type(other) != Point:
            raise TypeError("Invalid type. Both objects must be of Point.")
        if self.dimension != other.dimension:
            raise Exception(f"Incorrect dimensions.")
        if self.coordinates.keys() != other.coordinates.keys():
            raise Exception(f"Differing dimension labels.")
        coords = dict()
        for j,k in zip(self.coordinates.keys(), other.coordinates.keys()):
            coords[j] = (self.coordinates[j] - other.coordinates[k])
        return Point(coords)

    def __mul__(self, other) -> float:
        """
        This gets the dot product of two points/vectors and returns a float
        """
        if type(other) != Point:
            raise TypeError("Invalid type. Both objects must be of Point.")
        if self.dimension != other.dimension:
            raise Exception(f"Incorrect dimensions.")
        if self.coordinates.keys() != other.coordinates.keys():
            raise Exception(f"Differing dimension labels.")
        d_prod = 0.0
        for j,k in zip(self.coordinates.keys(), other.coordinates.keys()):
            d_prod += (self.coordinates[j] * other.coordinates[k])
        return d_prod




"""
TODO:
    Points needs to be updated to reflect these changes to Point.
    This should be very easy to do and currently, Points may not
    behave as it should and frankly shouldn't even be used until this 
    garbage I've wrote is cleaned up.
"""

class Points:
    """
    Points will store a set of the Point object and acts 
    like a container to simplify accessing and storing many Points
    """
    def __init__(self, p_set):
        self.p_set = list(p_set)
        self.len = len(p_set)

        self.labels = []
        for p in self.p_set:
            self.labels = p.coordinates.keys()

        


    
    def all_line(self, label:str) -> list:
        """
        Gets all the points in the line label.
        ex. all_line('x') gives a list of all the points on the x line
        """

        if label not in self.labels:
            return False
        line = []
        for p in self.p_set:
            line.append(p.coordinates[label])
        return line


    def add_point(self, pt):
        self.p_set.append(pt)
        self.len = len(self.p_set)
        for label in pt.coordinates.keys():
            if label not in self.labels:
                self.labels.append(label)

    def pop(self, i=None):
        if i == None:
            pop_point = self.p_set.pop()
        else:
            pop_point = self.p_set.pop(i)
        self.len = len(self.p_set)
        return pop_point
    
    def rm_point(self, pt):
        if type(pt) != Point and (type(pt) == list or type(pt) == tuple):
           pt1 = Point(pt) 
        else:
            pt1 = pt


        for idx,p in enumerate(self.p_set):
            if p == pt1:
                del self.p_set[idx]
                self.len = len(self.p_set)
                return True
        
        return False


    



                          

