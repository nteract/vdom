#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
vdom.core
~~~~~~~~~

This module provides the core implementation for the VDOM (Virtual DOM).

"""

from jsonschema import validate, Draft4Validator, ValidationError

def toJSON(el, schema=None):
    """Convert an element to JSON

    If you wish to validate the JSON, pass in a schema via the schema keyword argument.
    If a schema is provided, this raises a ValidationError if JSON does not match the schema.
    """
    if(type(el) is str):
        return el
    if(type(el) is list):
        return list(map(toJSON, el))
    elif(type(el) is dict):
        assert 'tagName' in el
        json_el = el.copy()
        if 'attributes' not in el:
            json_el['attributes'] = {}
        if 'children' not in el:
            json_el['children'] = []
    elif(hasattr(el, 'tagName') and hasattr(el, 'attributes')):
        json_el = {
            'tagName': el.tagName,
            'attributes': el.attributes,
            'children': toJSON(el.children)
        }
    else:
        json_el = el

    if schema:
        try:
            validate(instance=json_el, schema=schema, cls=Draft4Validator)
        except ValidationError as e:
            raise ValidationError("Your object didn't match the schema: {}. \n {}".format(schema, e))

    return json_el


class VDOM():
    """A basic virtual DOM class which allows you to write literal VDOM spec
    
    >>> VDOM({ 'tagName': 'h1', 'children': 'Hey', 'attributes': {}})
    
    It's probably better to use `vdom.h` or the helper functions:
    
    >>> from vdom import h
    >>> h('h1', 'Hey')
    <h1 />
    
    >>> from vdom.helpers import h1
    >>> h1('Hey')
    
    """
    def __init__(self, obj):
        self.obj = obj

    def _repr_mimebundle_(self, include, exclude, **kwargs):
        return {
                'application/vdom.v1+json': toJSON(self.obj)
        }

def _flatten_children(*children, **kwargs):
    '''Flattens *args to allow children to be passed as an array or as
    positional arguments.
    
    >>> _flatten_children("a", "b", "c")
    ["a", "b", "c"]
    
    >>> _flatten_children(["a", "b"])
    ["a", "b"]
    
    >>> _flatten_children(children=["c", "d"])
    ["c", "d"]
    
    >>> _flatten_children()
    []
    
    '''
    # children as keyword argument takes precedence
    if('children' in kwargs):
        children = kwargs['children']
    elif children is not None:
        if len(children) == 0:
            children = None
        elif len(children) == 1:
            # Flatten by default
            children = children[0]
        elif isinstance(children[0], list):
            # Only one level of flattening, just to match the old API
            children = children[0]
        else:
            children = list(children)
    else:
        # Empty list of children
        children = []
    return children

def createComponent(tagName):
    """Create a component for an HTML Tag

    Examples:
        >>> marquee = createComponent('marquee')
        >>> marquee('woohoo')
        <marquee>woohoo</marquee>

    """

    class Component():
        """A basic class for a virtual DOM Component"""
        def __init__(self, *children, **kwargs):
            self.children = _flatten_children(*children, **kwargs)
            self.attributes = kwargs
            self.tagName = tagName

        def _repr_mimebundle_(self, include, exclude, **kwargs):
            return {
                'application/vdom.v1+json': toJSON(self),
                'text/plain': '<{tagName} />'.format(tagName=tagName)
            }
            
    Component.__doc__ = """A virtual DOM component for a {tagName} tag
    
    >>> {tagName}()
    <{tagName} />
    """.format(tagName=tagName)
    
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

def h(tagName, *children, **kwargs):
    """Takes an HTML Tag, children (string, array, or another element), and attributes

    Examples:

      >>> h('div', [h('p', 'hey')])
      <div><p>hey</p></div>

    """
    attrs = {}
    if 'attrs' in kwargs:
        attrs = kwargs.pop('attrs')
        
    attrs = attrs.copy()
    attrs.update(kwargs)
    
    el = createComponent(tagName)
    return el(children, **attrs)


# These are left for backwards compatibility, from here on out we should
# define these in vdom.helpers, just like hyperscript-helpers
h1 = createComponent('h1')
p = createComponent('p')
div = createComponent('div')
img = createComponent('img')
b = createComponent('b')
