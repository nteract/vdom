#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
vdom.core
~~~~~~~~~

This module provides the core implementation for the VDOM (Virtual DOM).

"""
def toJSON(el):
    """Convert an element to JSON"""
    if(type(el) is str):
        return el
    if(type(el) is list):
        return list(map(toJSON, el))
    if(hasattr(el, 'tagName') and hasattr(el, 'attributes')):
        return {
            'tagName': el.tagName,
            'attributes': el.attributes,
            'children': toJSON(el.children)
        }
    return el


class VDOM():
    """A basic virtual DOM class"""
    def __init__(self, obj):
        self.obj = obj

    def _repr_mimebundle_(self, include, exclude, **kwargs):
        return {
                'application/vdom.v1+json': toJSON(self.obj)
        }


def createElement(tagName):
    """Take an HTML tag and create an element"""

    class VDOMEl():
        """A basic class for a virtual DOM element"""
        def __init__(self, children=None, **kwargs):
            self.children = children
            self.attributes = kwargs
            self.tagName = tagName

        def _repr_mimebundle_(self, include, exclude, **kwargs):
            return VDOM(self)

    return VDOMEl


# This deserves some bonafide metaprogramming
# We'll just get started creating some elements for now
h1 = createElement('h1')
p = createElement('p')
div = createElement('div')
img = createElement('img')
b = createElement('b')
