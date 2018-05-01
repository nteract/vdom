#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..core import create_component, create_element, to_json, VDOM
from ..helpers import div, p, img, h1, b
from jsonschema import ValidationError, validate
import os
import io
import json
import pytest
import warnings


_vdom_schema_file_path = os.path.join(
    os.path.dirname(__file__), "..", "schemas", "vdom_schema_v1.json")
with io.open(_vdom_schema_file_path, "r") as f:
    VDOM_SCHEMA = json.load(f)


def test_to_json():
    assert to_json({
        'tagName': 'h1',
        'attributes': {
            'data-test': True
        },
        'children': []
    }) == {
        'tagName': 'h1',
        'attributes': {
            'data-test': True
        },
        'children': []
    }

    assert to_json(div(h1('Our Incredibly Declarative Example'))) == {
        'tagName': 'div',
        'children': [{
            'tagName': 'h1',
            'children': ['Our Incredibly Declarative Example'],
            'attributes': {}
        }],
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
            'children': ['Our Incredibly Declarative Example'],
            'attributes': {}
        }, {
            'tagName':
            'p',
            'attributes': {},
            'children': [
                'Can you believe we wrote this ', {
                    'tagName': 'b',
                    'children': ['in Python'],
                    'attributes': {}
                }, '?'
            ]
        }, {
            'tagName': 'img',
            'children': [],
            'attributes': {
                'src':
                'https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif'
            }
        }],
        'attributes': {}
    }


_valid_vdom_obj = {'tagName': 'h1', 'children': 'Hey', 'attributes': {}}
_invalid_vdom_obj = {'tagName': 'h1', 'children':[{'randomProperty': 'randomValue'}]}


def test_schema_validation():
    with pytest.raises(ValidationError):
        test_vdom = VDOM([_valid_vdom_obj], )

  
    # check that you can pass a valid schema
    assert (VDOM(_valid_vdom_obj, schema=VDOM_SCHEMA))

    # check that an invalid schema throws ValidationError
    with pytest.raises(ValidationError):
        test_vdom = VDOM([_invalid_vdom_obj], )    

    
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
    with pytest.raises(ValueError, message='<void /> cannot have children'):
        void(div())


def test_component_disallows_children_kwargs():
    void = create_component('void', allow_children=False)
    with pytest.raises(ValueError, message='<void /> cannot have children'):
        void(children=div())
