from typing import (Callable, List)

# %%
class Callb_store: # TODO find some more efficient way to store callbacks, FIXME run callback one time, instead of multiple times
    """ Class for storing callbacks for specyfied addresses """
    
    def __init__(self):
        self._callbs: dict = {}
    
    def add_callb(self, addr: int, callb: Callable[[int, List[int]], None], count: int = 1) -> None: 
        """ Callback = func(addr: int, vals: list) -> None """
        
        for a in range(addr, addr + count):
            x = self._callbs.get(a)
            if (x != None):
                x.append((1, callb))
            else: 
                self._callbs[a] = [(1, callb)]
            
    def run_callbs(self, addr: int, vals: List[int]):
        for i, a in enumerate(range(addr, addr + len(vals))):
            x = self._callbs.get(a)
            if (x != None):
                for count, callb in x:
                    callb(a, [vals[i]]) # FIXME
                    
    def extend(self, cs):
        for a, v in cs._callbs:
            x = self._callbs.get(a)
            if (x != None):
                x.update(v)
            else: 
                self._callbs[a] = v
