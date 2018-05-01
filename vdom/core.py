"""
vdom.core
~~~~~~~~~

This module provides functions for creating elements and creating objects
that are renderable in jupyter frontends.

"""

from jsonschema import validate, Draft4Validator, ValidationError
import json
import warnings

import os
import io

_vdom_schema_file_path = os.path.join(
    os.path.dirname(__file__), "schemas", "vdom_schema_v1.json")
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
    elif isinstance(el, VDOM):
        json_el = el.to_dict()
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

    >>> VDOM(tag_name='h1', children='Hey', attributes: {}})

    >>> from vdom.helpers import h1
    >>> h1('Hey')
    """
    # This class should only have these 4 attributes
    __slots__ = ['tag_name', 'attributes', 'children', 'key', '_frozen']

    def __init__(self, tag_name, attributes=None, children=None, key=None, schema=None):
        if schema is not None:
            warnings.warn('Passing schema param to VDOM constructor is deprecated')
        if isinstance(tag_name, dict) or isinstance(tag_name, list):
            # Backwards compatible interface
            warnings.warn('Passing dict to VDOM constructor is deprecated')
            value = tag_name
            vdom_obj = VDOM.from_dict(value)
            tag_name = vdom_obj.tag_name
            attributes = vdom_obj.attributes
            children = vdom_obj.children
            key = vdom_obj.key
        self.tag_name = tag_name
        self.attributes = attributes if attributes else {}
        self.children = children if children else []
        self.key = key

        # mark completion of object creation. Object is immutable from now.
        self._frozen = True

    def __setattr__(self, attr, value):
        """
        Make instances immutable after creation
        """
        if hasattr(self, '_frozen') and self._frozen:
            raise ValueError("Cannot change attribute children of immutable object")
        super().__setattr__(attr, value)

    def to_dict(self):
        vdom_dict = {
            'tagName': self.tag_name,
            'attributes': self.attributes
        }
        if self.key:
            vdom_dict['key'] = self.key
        vdom_dict['children'] = [c.to_dict() if isinstance(c, VDOM) else c for c in self.children]
        return vdom_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    def json_contents(self):
        warnings.warn('VDOM.json_contents method is deprecated, use to_json instead')
        return self.to_json()

    def _repr_mimebundle_(self, include, exclude, **kwargs):
        return {
            'application/vdom.v1+json': json.dumps(self.to_dict()),
            'text/plain': '<{tagName} />'.format(tagName=self.tag_name)
        }

    @classmethod
    def from_dict(cls, value):
        try:
            validate(instance=value, schema=VDOM_SCHEMA, cls=Draft4Validator)
        except ValidationError as e:
            raise ValidationError(_validate_err_template.format(VDOM_SCHEMA, e))
        return cls(
            tag_name=value['tagName'],
            attributes=value.get('attributes', {}),
            children=[VDOM.from_dict(c) if isinstance(c, dict) else c for c in value.get('children', [])],
            key=value.get('key')
        )


def create_component(tag_name, allow_children=True):
    """
    Create a component for an HTML Tag

    Examples:
        >>> marquee = create_component('marquee')
        >>> marquee('woohoo')
        <marquee>woohoo</marquee>
    """
    def _component(*children, **kwargs):
        if 'children' in kwargs:
            children = kwargs.pop('children')
        if 'attributes' in kwargs:
            attributes = kwargs['attributes']
        else:
            attributes = dict(**kwargs)
        if tag_name == 'img':
            print(children)
        if not allow_children and children:
            # We don't allow children, but some were passed in
            raise ValueError('<{tag_name} /> cannot have children'.format(tag_name=tag_name))
        v = VDOM(tag_name, attributes, children)
        return v
    return _component


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
    warnings.warn("Warning: createElement is deprecated in favor of createComponent")
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