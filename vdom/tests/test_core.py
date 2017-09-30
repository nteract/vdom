#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..core import _flatten_children

def test_flatten_children():
    # when the first argument is an array, interpret it as the primary argument
    assert _flatten_children([1,2,3]) == [1,2,3]
    # otherwise positional arguments are fine
    assert _flatten_children(1,2,3) == [1,2,3]
    # keyword argument of children is ok too
    assert _flatten_children(children=[1,2,3]) == [1,2,3]

    # precedence tests
    # kwargs[children] is highest priority
    assert _flatten_children([1],2, children=[3]) == [3]
    # array as first argument second highest priority
    assert _flatten_children([1],2) == [1]
    # otherwise, positional arguments are the default
    assert _flatten_children(2) == [2]

    # with no arguments, we get an empty array
    assert _flatten_children() == []
    # an empty array returns an empty array
    assert _flatten_children([]) == []

    # If the first argument is None, we assume they explicitly wanted a
    # null element for a VDOMEl (this is ok)
    assert _flatten_children(None) == [None]
    assert _flatten_children(None, 1, None) == [None, 1, None]
