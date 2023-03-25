#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import json
import os

import pytest
from jsonschema import ValidationError

from ..core import (
    VDOM,
    convert_style_key,
    create_component,
    create_element,
    eventHandler,
    to_json,
)
from ..helpers import b, button, div, h1, img, p

_vdom_schema_file_path = os.path.join(
    os.path.dirname(__file__), "..", "schemas", "vdom_schema_v1.json"
)
with io.open(_vdom_schema_file_path, "r") as f:
    VDOM_SCHEMA = json.load(f)


def test_to_html():
    html = div(p("Hello world", title='something')).to_html()
    assert html == '<div><p title="something">Hello world</p></div>'


def test_to_html_unicode():
    html = div(p(u"Hello world", title=u'something')).to_html()
    assert html == '<div><p title="something">Hello world</p></div>'


def test_to_html_escaping():
    html = div(p("Hello world<script>evil</script>", title='something')).to_html()
    assert (
        html == '<div><p title="something">Hello world&lt;script&gt;evil&lt;/script&gt;</p></div>'
    )


def test_css():
    el = div(
        p('Hello world'),
        style={
            'backgroundColor': 'pink',
            'color': 'white',
            # Quotes should be entity escaped
            'fontFamily': "'something something'",
        },
        title='Test',
    )
    html = el.to_html()
    expected = '<div style="background-color: pink; color: white; font-family: &#x27;something something&#x27;" title="Test"><p>Hello world</p></div>'
    assert html == expected
    assert el.to_dict() == {
        'attributes': {
            'style': {
                'backgroundColor': 'pink',
                'color': 'white',
                'fontFamily': "'something something'",
            },
            'title': 'Test',
        },
        'children': [{'attributes': {}, 'children': ['Hello world'], 'tagName': 'p'}],
        'tagName': 'div',
    }


def test_event_handler_normal_function():
    def handle_click(event):
        print(event)

    el = button('click me', onClick=handle_click)

    assert el.to_html() == '<button>click me</button>'
    assert el.to_dict() == {
        'attributes': {},
        'eventHandlers': {
            'onClick': {
                'hash': hash(handle_click),
                'stopPropagation': False,
                'preventDefault': False,
            },
        },
        'children': ['click me'],
        'tagName': 'button',
    }


def test_event_handler_decorator():
    @eventHandler(stopPropagation=True, preventDefault=True)
    def handle_click(event):
        pass

    assert handle_click.serialize() == {
        "hash": hash(handle_click._handler),
        "preventDefault": True,
        "stopPropagation": True,
    }

    el = button('click me', onClick=handle_click)

    assert el.to_dict() == {
        'attributes': {},
        'eventHandlers': {
            'onClick': {
                'hash': hash(handle_click),
                'stopPropagation': True,
                'preventDefault': True,
            },
        },
        'children': ['click me'],
        'tagName': 'button',
    }


def test_to_json():
    assert to_json({'tagName': 'h1', 'attributes': {'data-test': True}, 'children': []}) == {
        'tagName': 'h1',
        'attributes': {'data-test': True},
        'children': [],
    }

    assert to_json(div(h1('Our Incredibly Declarative Example'))) == {
        'tagName': 'div',
        'children': [
            {'tagName': 'h1', 'children': ['Our Incredibly Declarative Example'], 'attributes': {}}
        ],
        'attributes': {},
    }

    assert to_json(
        div(
            h1('Our Incredibly Declarative Example'),
            p('Can you believe we wrote this ', b('in Python'), '?'),
            img(src="https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif"),
        )
    ) == {
        'tagName': 'div',
        'children': [
            {'tagName': 'h1', 'children': ['Our Incredibly Declarative Example'], 'attributes': {}},
            {
                'tagName': 'p',
                'attributes': {},
                'children': [
                    'Can you believe we wrote this ',
                    {'tagName': 'b', 'children': ['in Python'], 'attributes': {}},
                    '?',
                ],
            },
            {
                'tagName': 'img',
                'children': [],
                'attributes': {'src': 'https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif'},
            },
        ],
        'attributes': {},
    }


def test_VDOM_from_dict():
    json = VDOM.from_dict(
        {
            'tagName': 'div',
            'children': [
                {
                    'tagName': 'h1',
                    'children': ['Our Incredibly Declarative Example'],
                    'attributes': {},
                },
                {
                    'tagName': 'p',
                    'attributes': {},
                    'children': [
                        'Can you believe we wrote this ',
                        {'tagName': 'b', 'children': ['in Python'], 'attributes': {}},
                        '?',
                    ],
                },
                {
                    'tagName': 'img',
                    'children': [],
                    'attributes': {
                        'src': 'https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif'
                    },
                },
            ],
            'attributes': {},
        }
    ).to_json()
    assert json == (
        div(
            h1('Our Incredibly Declarative Example'),
            p('Can you believe we wrote this ', b('in Python'), '?'),
            img(src="https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif"),
        ).to_json()
    )


_valid_vdom_obj = {'tagName': 'h1', 'children': 'Hey', 'attributes': {}}
_invalid_vdom_obj = {'tagName': 'h1', 'children': [{'randomProperty': 'randomValue'}]}


def test_schema_validation():
    with pytest.raises(ValidationError):
        VDOM([_valid_vdom_obj])

    # check that you can pass a valid schema
    assert VDOM(_valid_vdom_obj, schema=VDOM_SCHEMA)

    # check that an invalid schema throws ValidationError
    with pytest.raises(ValidationError):
        VDOM([_invalid_vdom_obj])


def test_component_allows_children():
    nonvoid = create_component('nonvoid', allow_children=True)
    test_component = nonvoid(div())
    assert test_component.children is not None


def test_create_element_deprecated():
    import warnings

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        create_element('warnme')
        assert len(w) == 1


def test_component_disallows_children():
    void = create_component('void', allow_children=False)
    with pytest.raises(ValueError, match='<void /> cannot have children'):
        void(div())


def test_component_disallows_children_kwargs():
    void = create_component('void', allow_children=False)
    with pytest.raises(ValueError, match='<void /> cannot have children'):
        void(children=div())


def test_immutable():
    with pytest.raises(AttributeError):
        comp = div("Hello")
        comp.children = "Nello"


def test_immutable_children():
    comp = div(h1("hello"))
    with pytest.raises(AttributeError):
        comp.children.append(h1("boo"))
    with pytest.raises(TypeError):
        comp.children[0] = h1("boo")


def test_immutable_attributes():
    comp = div(h1("hello"))
    with pytest.raises(ValueError):
        comp.attributes['class'] = 'something'


def test_invalid_children():
    with pytest.raises(ValueError):
        div(5)


def test_convert_style_key():
    assert convert_style_key("backgroundColor") == "background-color"
    assert convert_style_key("preserveAspectRatio") == "preserve-aspect-ratio"
