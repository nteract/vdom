"""test_frozen.py"""
import pytest

from vdom.frozendict import FrozenDict

def setup():
    """creates a frozen dict"""
    testdict = FrozenDict([("div", "happy"), ("h", 4), ("meter", "level")])
    return testdict

def test_ordering():
    """FrozenDict should preserve ordering"""
    f = FrozenDict([("a", 1), ("b", 2)])
    assert list(f.items()) == [("a", 1), ("b", 2)]



def test_frozen():
    """FrozenDict is not modifyable"""
    f = FrozenDict(a=1)
    with pytest.raises(ValueError):
        f["b"] = 5

def test_pop():
    testdict = setup()
    with pytest.raises(ValueError):
        testdict.pop()

def test_popitem():
    testdict = setup()
    with pytest.raises(ValueError):
        testdict.popitem("h")

def test_clear():
    testdict = setup()
    with pytest.raises(ValueError):
        testdict.clear("div")

def test_update():
    testdict = setup()
    with pytest.raises(ValueError):
        testdict.update("div", "woo")

def test_setdefault():
    testdict = setup()
    with pytest.raises(ValueError):
        testdict.setdefault("div")
