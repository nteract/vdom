class FrozenDict(dict):
    """
    Immutable dictionary subclass

    Once constructed, dictionary can not be mutated without
    internal python hacks. Useful for enforcing invariants,
    but not useful for securing anything!
    """
    def __readonly__(self, *args, **kwargs):
        raise ValueError("Can not modify FrozenDict")

    __setitem__ = __readonly__
    __delitem__ = __readonly__
    pop = __readonly__
    popitem = __readonly__
    clear = __readonly__
    update = __readonly__
    setdefault = __readonly__