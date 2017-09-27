#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
vdom.helpers
~~~~~~~~~

Little helper functions for (many of) the HTML Elements.

from vdom.helpers import div, img

div(
    img(src="http://bit.ly/storybot-vdom")
)

"""

from .core import createComponent

h1 = createComponent('h1')
p = createComponent('p')
div = createComponent('div')
img = createComponent('img')
b = createComponent('b')

table = createComponent('table')
thead = createComponent('thead')
th = createComponent('th')
tr = createComponent('tr')
tbody = createComponent('tbody')
td = createComponent('td')

input_ = createComponent('input')
