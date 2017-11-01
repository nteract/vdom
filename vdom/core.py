"""
vdom.core
~~~~~~~~~

This module provides functions for creating elements and creating objects
that are renderable in jupyter frontends.

"""

from jsonschema import validate, Draft4Validator, ValidationError
import json

import os
import io

_vdom_schema_file_path = os.path.join(
    os.path.dirname(__file__), "schemas", "vdom_schema_v0.json")
with io.open(_vdom_schema_file_path, "r") as f:
    VDOM_SCHEMA = json.load(f)
_validate_err_template = "Your object didn't match the schema: {}. \n {}"


def to_json(el, schema=None):
    """Convert an element to VDOM JSON

    If you wish to validate the JSON, pass in a schema via the schema keyword
    argument. If a schema is provided, this raises a ValidationError if JSON
    does not match the schema.
    """
    if (type(el) is str):
        json_el = el
    elif (type(el) is list):
        json_el = list(map(to_json, el))
    elif (type(el) is dict):
        assert 'tagName' in el
        json_el = el.copy()
        if 'attributes' not in el:
            json_el['attributes'] = {}
        if 'children' not in el:
            json_el['children'] = []
    elif (hasattr(el, 'tagName') and hasattr(el, 'attributes')):
        json_el = {
            'tagName': el.tagName,
            'attributes': el.attributes,
            'children': to_json(el.children)
        }
    else:
        json_el = el

    if schema:
        try:
            validate(instance=json_el, schema=schema, cls=Draft4Validator)
        except ValidationError as e:
            raise ValidationError(_validate_err_template.format(schema, e))

    return json_el


class VDOM(object):
    """A basic virtual DOM class which allows you to write literal VDOM spec

    >>> VDOM({ 'tagName': 'h1', 'children': 'Hey', 'attributes': {}})

    It's probably better to use `vdom.h` or the helper functions:

    >>> from vdom import h
    >>> h('h1', 'Hey')
    <h1 />

    >>> from vdom.helpers import h1
    >>> h1('Hey')

    """
    _schema = VDOM_SCHEMA
    _obj = None

    def __init__(self, obj, schema=None):
        # we need to assign self.schema first,
        # because it is used to validate the object
        if schema is not None:
            self.schema = schema
        self.obj = obj

    def _repr_mimebundle_(self, include, exclude, **kwargs):
        return {'application/vdom.v1+json': self.json_contents}

    @property
    def json_contents(self):
        return to_json(self._obj, schema=self._schema)

    @property
    def obj(self):
        return self._obj

    @obj.setter
    def obj(self, value):
        if to_json(value, schema=self._schema) is not None:
            self._obj = value

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, value):
        Draft4Validator.check_schema(value)
        # if object is present, check if schema works, if not give a log
        if self._obj:
            try:
                to_json(self._obj, schema=value)
            except ValidationError as e:
                # Don't raise error, but give warning that it is no longer valid
                print(_validate_err_template.format(value, e))
                print("VDOM cannot submit a message until this is fixed")
        self._schema = value

    @staticmethod
    def validate(value, schema=_schema):
        to_json(value, schema=schema)


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
    if ('children' in kwargs):
        children = kwargs['children']
    elif children is not None:
        # If children array is empty, might as well pass None (null in JSON)
        if len(children) == 0:
            children = None
        elif len(children) == 1:
            # Flatten by default
            children = children[0]
        elif isinstance(children[0], list):
            # Only one level of flattening, just to match the old API
            children = children[0]
            # Do we care to map across all the children, making sure to
            # flatten them too? Or should we just do the else case that
            # keeps lists of lists of nodes?
        else:
            # children came in as pure args, our primary case
            children = list(children)
    else:
        # Empty list of children
        children = []
    return children


def create_component(tagName, allow_children=True):
    """Create a component for an HTML Tag

    Examples:
        >>> marquee = create_component('marquee')
        >>> marquee('woohoo')
        <marquee>woohoo</marquee>

    """

    class Component():
        """A basic class for a virtual DOM Component"""

        def __init__(self, *children, **kwargs):
            self.children = _flatten_children(*children, **kwargs)
            if not allow_children and self.children:
                raise ValueError('<{tagName} /> cannot have children'.format(
                    tagName=tagName))
            self.attributes = kwargs
            self.tagName = tagName
            self._schema = VDOM_SCHEMA

        def _repr_mimebundle_(self, include, exclude, **kwargs):
            return {
                'application/vdom.v1+json': to_json(self, schema=self._schema),
                'text/plain': '<{tagName} />'.format(tagName=tagName)
            }

        @property
        def schema(self):
            return self._schema

        @schema.setter
        def schema(self, value):
            Draft4Validator.check_schema(value)
            self._schema = value

    Component.__doc__ = """A virtual DOM component for a {tagName} tag

    >>> {tagName}()
    <{tagName} />
    """.format(tagName=tagName)

    return Component


def create_element(tagName):
    """Takes an HTML tag and creates a VDOM Component

    WARNING: This call is deprecated, as the name is the same as
    React.createElement while having an entirely different meaning.

    This is written more like a helper, similar to
    https://github.com/ohanhi/hyperscript-helpers allowing you to create code
    like

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
    return create_component(tagName)


def h(tagName, *children, **kwargs):
    """Takes an HTML Tag, children (string, array, or another element), and
    attributes

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


# backwards compatibility
toJSON = to_json
createElement = create_element
createComponent = create_component
