import numpy as np
from dataclasses import dataclass, field

# FRAME_RATE = 30
# TIME_DELTA = float(1/FRAME_RATE)

@dataclass(frozen=True)
class Point:
    _coordinates: None
    _dimension: int = field(init=False) # This is the amount of dimensions in the Point

    def __post_init__(self):
        pos = self._coordinates
        object.__setattr__(self, '_coordinates', dict())
        if type(pos) == tuple or type(pos) == list:
            for n,p in enumerate(pos):
                self._coordinates['a'+str(n)] = p
            object.__setattr__(self, '_dimension', len(self._coordinates))
        elif type(pos) == dict:
            for label,value in pos.items():
                self._coordinates[label] = value
            object.__setattr__(self, '_dimension', len(self._coordinates))
        else:
            raise TypeError('Invalid object type for Point.coordinates. Must be of tuple, list, or dict.').with_traceback()

    def __add__(self, other):
        """
        Returns a Point which is a vector representation of addition between the two points
        """
        if type(other) != Point:
            raise TypeError("Invalid type. Both objects must be of Point.")
        if self._dimension != other._dimension:
            raise Exception(f"Incorrect dimensions.")
        if self._coordinates.keys() != other._coordinates.keys():
            raise Exception(f"Differing dimension labels.")
        coords = dict()
        for j,k in zip(self._coordinates.keys(), other._coordinates.keys()):
            coords[j] = (self._coordinates[j] + other._coordinates[k])
        return Point(coords)

    def __sub__(self, other):
        """
        Returns a Point which is a vector representation of difference between the two points
        """
        if type(other) != Point:
            raise TypeError("Invalid type. Both objects must be of Point.")
        if self._dimension != other._dimension:
            raise Exception(f"Incorrect dimensions.")
        if self._coordinates.keys() != other._coordinates.keys():
            raise Exception(f"Differing dimension labels.")
        coords = dict()
        for j,k in zip(self._coordinates.keys(), other._coordinates.keys()):
            coords[j] = (self._coordinates[j] - other._coordinates[k])
        return Point(coords)

    def __mul__(self, other) -> float:
        """
        This gets the dot product of two points/vectors and returns a float
        """
        if type(other) != Point:
            raise TypeError("Invalid type. Both objects must be of Point.")
        if self._dimension != other._dimension:
            raise Exception(f"Incorrect dimensions.")
        if self._coordinates.keys() != other._coordinates.keys():
            raise Exception(f"Differing dimension labels.")
        d_prod = 0.0
        for j,k in zip(self._coordinates.keys(), other._coordinates.keys()):
            d_prod += (self._coordinates[j] * other._coordinates[k])
        return d_prod

    def __eq__(self, other) -> bool:
        if self._dimension != other._dimension:
            return False
        if self._coordinates.keys() != other._coordinates.keys():
            raise Exception(f"Differing dimension labels")
        for key in self._coordinates.keys():
            if self._coordinates[key] != other._coordinates[key]:
                return False
        return True





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
    def __init__(self, p_set=None):
        if p_set != None:
            try:
                self.__p_set = list(p_set)
                self.__len = len(p_set)
            except TypeError:
                print("Incorrect type for p_set in __init__(self, p_set)")
        else:
            self.__p_set = list()
        self.__labels = []
        for p in self.__p_set:
            for key in p._coordinates.keys():
                if key not in self.__labels:
                    self.__labels.append(key)

    def __getitem__(self, index) -> Point:
       """
        This part of __getitem__ should be enough to deprecate the line method since this may
        be much easier and simpler to use rather than using line to get all the values on
        a specific dimension. Here, assume p1 is some points containing (x, y) = (1,2).
        You can just do p1['x'] and returns [1] or list(p1['x'], p1['y']) => [1, 2]!
        """
       if type(index) == int:
           try:
               return self.__p_set[index]
           except IndexError:
               raise IndexError(f'Not subscriptable to index \'{index}\' - Out of range')

       elif type(index) == str:
           if index not in self.__labels:
               raise IndexError(f'No key \'{index}\' exists to subscript a numerical line')
           _line = []
           for pt in self.__p_set:
               _line.append(pt._coordinates[index])
           return _line

       else:
           raise TypeError(f'Incorrect indexing with type {type(index)} - Must be of type \'int\' or \'str\'')

    def __len__(self) -> int:
       return self.__len

    def __contains__(self, item) -> bool:
       for p in self.__p_set:
           if p == item:
               return True
       return False




    def line(self, label:str) -> list:
        """
        Gets all the points in the line labeled with "label".
        ex. line('x') gives a list of all the points on the x line
        """

        if label not in self.__labels:
            return False
        _line = []
        for p in self.__p_set:
            _line.append(p._coordinates[label])
        return _line


    def append(self, pt):
        self.__p_set.append(pt)
        self.__len = len(self.__p_set)

        #This could lead to trouble
        #Adding another dimension while the others don't contain
        #the new dimension could lead to some issues!
        for label in pt._coordinates.keys():
            if label not in self.__labels:
                self.__labels.append(label)

    def pop(self, i=None) -> Point:
        if i == None:
            pop_point = self.__p_set.pop()
        else:
            pop_point = self.__p_set.pop(i)
        self.len = len(self.__p_set)
        return pop_point

    def rm_point(self, pt):
        if type(pt) != Point and (type(pt) == list or type(pt) == tuple):
            pt1 = Point(pt) 
        elif type(pt) == Point:
            pt1 = pt


        for idx,p in enumerate(self.p_set):
            if p == pt1:
                del self.p_set[idx]
                self.len = len(self.p_set)
                return True

        return False








