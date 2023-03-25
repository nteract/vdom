"""
vdom.core
~~~~~~~~~

This module provides functions for creating elements and creating objects
that are renderable in jupyter frontends.

"""
from __future__ import unicode_literals

import io
import json
import os
import re
import warnings
from html import escape

from IPython import get_ipython
from jsonschema import Draft4Validator, ValidationError, validate

from vdom.frozendict import FrozenDict

_vdom_schema_file_path = os.path.join(os.path.dirname(__file__), "schemas", "vdom_schema_v1.json")
with io.open(_vdom_schema_file_path, "r") as f:
    VDOM_SCHEMA = json.load(f)
_validate_err_template = "Your object didn't match the schema: {}. \n {}"


def to_json(el, schema=None):
    """Convert an element to VDOM JSON

    If you wish to validate the JSON, pass in a schema via the schema keyword
    argument. If a schema is provided, this raises a ValidationError if JSON
    does not match the schema.
    """
    if type(el) is str:
        json_el = el
    elif type(el) is list:
        json_el = list(map(to_json, el))
    elif type(el) is dict:
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


def eventHandler(handler=None, preventDefault=False, stopPropagation=False):
    """Create an event handler with special attributes

    Typically when defining event handlers you can simply pass them to a VDOM Component,
    however you can't prevent the event's default behaviors or stop its propagation up
    through the DOM this way.

    Parameters:
        preventDefault: stop the event's default behavior
        stopPropagation: halt the event's propagation up the DOM

    Examples:
        >>> @eventHandler(preventDefault=True, stopPropagation=True)
        ... def on_hover(event):
                pass
        >>> drag_drop_spot = VDOM("div", event_handler={"onDragOver": hover})
    """

    def setup(handler):
        return EventHandler(handler, preventDefault, stopPropagation)

    if handler is not None:
        return setup(handler)
    else:
        return setup


class EventHandler(object):
    def __init__(self, handler, prevent_default=False, stop_propagation=False):
        self._handler = handler
        self._prevent_default = prevent_default
        self._stop_propagation = stop_propagation

        self.comm = None
        # Register a new comm for this event handler
        if get_ipython():
            comm_manager = get_ipython().kernel.comm_manager
            comm_manager.register_target(hash(self), self._on_comm_opened)

    def serialize(self):
        return {
            "hash": hash(self),
            "preventDefault": self._prevent_default,
            "stopPropagation": self._stop_propagation,
        }

    def __call__(self, event):
        return self._handler(event)

    def __hash__(self):
        return hash(self._handler)

    def _on_comm_opened(self, comm, msg):
        self.comm = comm
        comm.on_msg(self._on_comm_msg)
        comm.send('Comm target "{hash}" registered by vdom'.format(hash=hash(self)))

    def _on_comm_msg(self, msg):
        data = msg['content']['data']
        event = json.loads(data)
        return_value = self(event)
        if return_value:
            self.comm.send(return_value)


class VDOM(object):
    """A basic virtual DOM class which allows you to write literal VDOM spec

    >>> VDOM(tag_name='h1', children='Hey', attributes: {}})

    >>> from vdom.helpers import h1
    >>> h1('Hey')
    """

    # This class should only have these 7 attributes
    __slots__ = ['tag_name', 'attributes', 'style', 'children', 'key', 'event_handlers', '_frozen']

    def __init__(
        self,
        tag_name,
        attributes=None,
        style=None,
        children=None,
        key=None,
        event_handlers=None,
        schema=None,
    ):
        if isinstance(tag_name, dict) or isinstance(tag_name, list):
            # Backwards compatible interface
            warnings.warn('Passing dict to VDOM constructor is deprecated')
            value = tag_name
            vdom_obj = VDOM.from_dict(value)
            tag_name = vdom_obj.tag_name
            style = vdom_obj.style
            event_handlers = vdom_obj.event_handlers
            attributes = vdom_obj.attributes
            children = vdom_obj.children
            key = vdom_obj.key
        self.tag_name = tag_name
        # Sort attributes so our outputs are predictable
        self.attributes = FrozenDict(sorted(attributes.items())) if attributes else FrozenDict()
        self.children = tuple(children) if children else tuple()
        self.key = key
        # Sort attributes so our outputs are predictable
        self.style = FrozenDict(sorted(style.items())) if style else FrozenDict()
        self.event_handlers = (
            FrozenDict(sorted(event_handlers.items())) if event_handlers else FrozenDict()
        )

        # Validate that all children are VDOMs or strings
        if not all(isinstance(c, (VDOM, str, bytes)) for c in self.children):
            raise ValueError('Children must be a list of VDOM objects or strings')

        # All style keys & values must be strings
        if not all(
            isinstance(k, (str, bytes)) and isinstance(v, (str, bytes))
            for k, v in self.style.items()
        ):
            raise ValueError('Style must be a dict with string keys & values')

        # mark completion of object creation. Object is immutable from now.
        self._frozen = True

        if schema is not None:
            self.validate(schema)

    def __setattr__(self, attr, value):
        """
        Make instances immutable after creation
        """
        if hasattr(self, '_frozen') and self._frozen:
            raise AttributeError("Cannot change attribute of immutable object")
        super(VDOM, self).__setattr__(attr, value)

    def validate(self, schema):
        """
        Validate VDOM against given JSON Schema

        Raises ValidationError if schema does not match
        """
        try:
            validate(instance=self.to_dict(), schema=schema, cls=Draft4Validator)
        except ValidationError as e:
            raise ValidationError(_validate_err_template.format(VDOM_SCHEMA, e))

    def to_dict(self):
        """Converts VDOM object to a dictionary that passes our schema"""
        attributes = dict(self.attributes.items())
        if self.style:
            attributes.update({"style": dict(self.style.items())})
        vdom_dict = {'tagName': self.tag_name, 'attributes': attributes}
        if self.event_handlers:
            event_handlers = dict(self.event_handlers.items())
            for key, handler in event_handlers.items():
                if not isinstance(handler, EventHandler):
                    handler = EventHandler(handler)
                event_handlers[key] = handler.serialize()
            vdom_dict['eventHandlers'] = event_handlers
        if self.key:
            vdom_dict['key'] = self.key
        vdom_dict['children'] = [c.to_dict() if isinstance(c, VDOM) else c for c in self.children]
        return vdom_dict

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_html(self):
        return self._repr_html_()

    def json_contents(self):
        warnings.warn('VDOM.json_contents method is deprecated, use to_json instead')
        return self.to_json()

    def _to_inline_css(self, style):
        """
        Return inline CSS from CSS key / values
        """
        return "; ".join(['{}: {}'.format(convert_style_key(k), v) for k, v in style.items()])

    def _repr_html_(self):
        """
        Return HTML representation of VDOM object.

        HTML escaping is performed wherever necessary.
        """
        # Use StringIO to avoid a large number of memory allocations with string concat
        with io.StringIO() as out:
            out.write('<{tag}'.format(tag=escape(self.tag_name)))
            if self.style:
                # Important values are in double quotes - cgi.escape only escapes double quotes, not single quotes!
                out.write(' style="{css}"'.format(css=escape(self._to_inline_css(self.style))))

            for k, v in self.attributes.items():
                # Important values are in double quotes - cgi.escape only escapes double quotes, not single quotes!
                if isinstance(v, (str, bytes)):
                    out.write(' {key}="{value}"'.format(key=escape(k), value=escape(v)))
                if isinstance(v, bool) and v:
                    out.write(' {key}'.format(key=escape(k)))
            out.write('>')

            for c in self.children:
                if isinstance(c, (str, bytes)):
                    out.write(escape(str(c)))
                else:
                    out.write(c._repr_html_())

            out.write('</{tag}>'.format(tag=escape(self.tag_name)))

            return out.getvalue()

    def _repr_mimebundle_(self, include=None, exclude=None, **kwargs):
        return {'application/vdom.v1+json': self.to_dict(), 'text/plain': self.to_html()}

    @classmethod
    def from_dict(cls, value):
        try:
            validate(instance=value, schema=VDOM_SCHEMA, cls=Draft4Validator)
        except ValidationError as e:
            raise ValidationError(_validate_err_template.format(VDOM_SCHEMA, e))
        attributes = value.get('attributes', {})
        style = None
        event_handlers = None
        if 'style' in attributes:
            # Make a copy of attributes, since we're gonna remove styles from it
            attributes = attributes.copy()
            style = attributes.pop('style')
        for key, val in attributes.items():
            if callable(val):
                attributes = attributes.copy()
                if event_handlers is None:
                    event_handlers = {key: attributes.pop(key)}
                else:
                    event_handlers[key] = attributes.pop(key)
        return cls(
            tag_name=value['tagName'],
            attributes=attributes,
            style=style,
            event_handlers=event_handlers,
            children=[
                VDOM.from_dict(c) if isinstance(c, dict) else c for c in value.get('children', [])
            ],
            key=value.get('key'),
        )


upper = re.compile(r'[A-Z]')


def _upper_replace(matchobj):
    return '-' + matchobj.group(0).lower()


def convert_style_key(key):
    """Converts style names from DOM to css styles.

    >>> convert_style_key("backgroundColor")
    "background-color"
    """
    return re.sub(upper, _upper_replace, key)


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
        else:
            # Flatten children under specific circumstances
            # This supports the use case of div([a, b, c])
            # And allows users to skip the * operator
            if len(children) == 1 and isinstance(children[0], list):
                # We want children to be tuples and not lists, so
                # they can be immutable
                children = tuple(children[0])
        style = None
        event_handlers = None
        attributes = dict(**kwargs)
        if 'style' in kwargs:
            style = kwargs.pop('style')
        if 'attributes' in kwargs:
            attributes = kwargs['attributes']
        for key, value in attributes.items():
            if callable(value):
                attributes = attributes.copy()
                if event_handlers is None:
                    event_handlers = {key: attributes.pop(key)}
                else:
                    event_handlers[key] = attributes.pop(key)
        if not allow_children and children:
            # We don't allow children, but some were passed in
            raise ValueError('<{tag_name} /> cannot have children'.format(tag_name=tag_name))

        v = VDOM(tag_name, attributes, style, children, None, event_handlers)
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
