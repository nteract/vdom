#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
vdom.core
~~~~~~~~~

This module provides the core implementation for the VDOM (Virtual DOM).

"""

from jsonschema import validate, Draft4Validator, ValidationError

def toJSON(el, schema=None):
    if schema:
        try:
            validate(instance=el, schema=schema, cls=Draft4Validator)
        except ValidationError as e:
            raise ValidationError("Your object didn't match the schema: {}. \n {}".format(schema, e))

    if(type(el) is str):
        return el
    """Convert an element to JSON

    If you wish to validate the JSON, pass in a schema via the schema keyword argument.
    If a schema is provided, this raises a ValidationError if JSON does not match the schema.
    """
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


def createComponent(tagName):
    """Create a component for an HTML Tag

    Examples:
        >>> marquee = createComponent('marquee')
        >>> marquee('woohoo')
        <marquee>woohoo</marquee>

    """

    class Component():
        """A basic class for a virtual DOM Component"""
        def __init__(self, children=None, **kwargs):
            self.children = children
            self.attributes = kwargs
            self.tagName = tagName

        def _repr_mimebundle_(self, include, exclude, **kwargs):
            return {
                'application/vdom.v1+json': toJSON(self)
            }

    return Component

def createElement(tagName):
    """Takes an HTML tag and creates a VDOM Component

    WARNING: This call is deprecated, as the name is the same as React.createElement
    while having an entirely different meaning.

    This is written more like a helper, similar to https://github.com/ohanhi/hyperscript-helpers
    allowing you to create code like

    div([
      p('hey')
    ])

    Instead of writing

    h('div', [
        h('p', 'hey')
    ])

    This should have been written more like React.createClass
    """
    print("Warning: createElement is deprecated in favor of createComponent")
    return createComponent(tagName)

def h(tagName, children=None, attrs=None, **kwargs):
    """Takes an HTML Tag, children (string, array, or another element), and attributes

    Examples:

      >>> h('div', [h('p', 'hey')])
      <div><p>hey</p></div>

    """
    if attrs is None:
        attrs={}
    el = createComponent(tagName)
    return el(children, **attrs, **kwargs)


h1 = createComponent('h1')
p = createComponent('p')
div = createComponent('div')
img = createComponent('img')
b = createComponent('b')
