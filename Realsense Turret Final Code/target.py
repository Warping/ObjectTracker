from points import Point, Points
from dataclasses import dataclass, field

@dataclass
class Target:
    _positions: Points
    _uid: int

    def append(self, pos:Point):
        self._positions.append(pos)

    def pop(self, index=None) -> Point:
        return self._positions.pop(index)

    def __len__(self) -> int:
        return len(self._positions)

    def __contains__(self, item:Point) -> bool:
        return item in self._positions

    def __getitem__(self, index) -> Point:
        return self._positions[index]
    
    # And to implement the rest later

    def __delitem__(self, item):
        pass


def mk_targ_list(targs:list) -> dict:
    tl = dict()
    for t in targs:
        tl[t._uid] = t
    return tl

class Targets:
    #_targs: dict = field(default_factory=dict)

    def __init__(self, targs):
        self._targs = targs

    def keys(self):
        return self._targs.keys()
    
    def values(self):
        return self._targs.values()

    def items(self):
        return self._targs.items()
    
    def __getitem__(self, uid) -> Target:
        if uid in self._targs.keys():
            return self._targs[uid]
        else:
            raise KeyError(f'UID {uid} does not exist in _targs')

    def __delitem__(self, uid):
        if uid in self._targs.keys():
            del self._targs[uid]
        else:
            raise KeyError(f'UID {uid} does not exist in _targs')

    def __setitem__(self, uid, targ:Target):
        if uid != targ._uid:
            raise Exception()
        self._targs[uid] = targ

    def __iter__(self):
        return iter(self._targs)


    


