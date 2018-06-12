from collections import OrderedDict

class FrozenDict(OrderedDict):
    """
    Immutable ordered dictionary subclass

    Once constructed, dictionary can not be mutated without
    internal python hacks. Useful for enforcing invariants,
    but not useful for securing anything!

    Uses an OrderedDict as base, to preserve ordering when
    making outputs.
    """
    def __init__(self, *args, **kwargs):
        self.frozen = False
        super(FrozenDict, self).__init__(*args, **kwargs)
        self.frozen = True

    def __readonly__(self, func, *args, **kwargs):
        if self.frozen:
            raise ValueError("Can not modify FrozenDict")
        else:
            return func(*args, **kwargs)

    def __setitem__(self, *args, **kwargs):
        return self.__readonly__(super().__setitem__, *args, **kwargs)

    def __delitem__(self, *args, **kwargs):
        return self.__readonly__(super().__delitem__, *args, **kwargs)

    def pop(self, *args, **kwargs):
        return self.__readonly__(super().pop, *args, **kwargs)

    def popitem(self, *args, **kwargs):
        return self.__readonly__(super().popitem, *args, **kwargs)

    def clear(self, *args, **kwargs):
        return self.__readonly__(super().clear, *args, **kwargs)

    def update(self, *args, **kwargs):
        return self.__readonly__(super().update, *args, **kwargs)

    def setdefault(self, *args, **kwargs):
        return self.__readonly__(super().setdefault, *args, **kwargs)