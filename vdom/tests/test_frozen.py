import pytest

from vdom.frozendict import FrozenDict


def test_ordering():
    """
    FrozenDict should preserve ordering
    """
    f = FrozenDict([('a', 1), ('b', 2)])
    assert list(f.items()) == [('a', 1), ('b', 2)]


def test_frozen():
    """
    FrozenDict is not modifyable
    """
    f = FrozenDict(a=1)
    with pytest.raises(ValueError):
        f['b'] = 5
