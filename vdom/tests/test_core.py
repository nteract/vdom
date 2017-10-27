#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..core import _flatten_children, to_json, VDOM
from ..helpers import div, p, img, h1, b
from jsonschema import ValidationError, validate
import pytest


def test_flatten_children():
    # when the first argument is an array, interpret it as the primary argument
    assert _flatten_children([1, 2, 3]) == [1, 2, 3]
    # otherwise positional arguments are fine
    assert _flatten_children(1, 2, 3) == [1, 2, 3]
    # keyword argument of children is ok too
    assert _flatten_children(children=[1, 2, 3]) == [1, 2, 3]

    # precedence tests
    # kwargs[children] is highest priority
    assert _flatten_children([1], 2, children=[3]) == [3]
    # array as first argument second highest priority
    assert _flatten_children([1], 2) == [1]
    # otherwise, positional arguments are the default
    assert _flatten_children(2, 3) == [2, 3]

    # an empty array returns an empty array
    assert _flatten_children([]) == []
    # with no arguments, we get a null
    assert _flatten_children() == None

    # If the first argument is None, we assume they explicitly wanted a
    # null element for a VDOMEl (this is ok)
    assert _flatten_children(None) == None
    assert _flatten_children(None, 1, None) == [None, 1, None]


def test_to_json():
    assert to_json({
        'tagName': 'h1',
        'attributes': { 'data-test': True },
        'children': []
    }) == {
        'tagName': 'h1',
        'attributes': { 'data-test': True},
        'children': []
    }

    assert to_json(div(h1('Our Incredibly Declarative Example'))) == {
        'tagName': 'div',
        'children': {
            'tagName': 'h1',
            'children': 'Our Incredibly Declarative Example',
            'attributes': {}
        },
        'attributes': {}
    }

    assert to_json(
        div(
            h1('Our Incredibly Declarative Example'),
            p('Can you believe we wrote this ', b('in Python'), '?'),
            img(src="https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif"
                ), )
    ) == {
        'tagName':
        'div',
        'children': [{
            'tagName': 'h1',
            'children': 'Our Incredibly Declarative Example',
            'attributes': {}
        }, {
            'tagName':
            'p',
            'attributes': {},
            'children': [
                'Can you believe we wrote this ', {
                    'tagName': 'b',
                    'children': 'in Python',
                    'attributes': {}
                }, '?'
            ]
        }, {
            'tagName': 'img',
            'children': None,
            'attributes': {
                'src':
                'https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif'
            }
        }],
        'attributes': {}
    }

_valid_vdom_obj= {'tagName': 'h1', 'children': 'Hey', 'attributes': {}}

def test_schema_validation():
    with pytest.raises(ValidationError):
        test_vdom = VDOM(
            [_valid_vdom_obj],
        )

    # make sure you can pass empty schema
    assert (
        VDOM([_valid_vdom_obj], schema = {}).json_contents == [_valid_vdom_obj]
        )
