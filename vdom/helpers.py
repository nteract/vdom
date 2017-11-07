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

from .core import create_component

# From https://developer.mozilla.org/en-US/docs/Web/HTML/Element

# Content sectioning
address = create_component('address')
article = create_component('article')
aside = create_component('aside')
footer = create_component('footer')
h1 = create_component('h1')
h2 = create_component('h2')
h3 = create_component('h3')
h4 = create_component('h4')
h5 = create_component('h5')
h6 = create_component('h6')
header = create_component('header')
hgroup = create_component('hgroup')
nav = create_component('nav')
section = create_component('section')

# Text content
blockquote = create_component('blockquote')
dd = create_component('dd')
div = create_component('div')
dl = create_component('dl')
dt = create_component('dt')
figcaption = create_component('figcaption')
figure = create_component('figure')
hr = create_component('hr', allow_children=False)
li = create_component('li')
ol = create_component('ol')
p = create_component('p')
pre = create_component('pre')
ul = create_component('ul')

# Inline text semantics
a = create_component('a')
abbr = create_component('abbr')
b = create_component('b')
br = create_component('br', allow_children=False)
cite = create_component('cite')
code = create_component('code')
data = create_component('data')
em = create_component('em')
i = create_component('i')
kbd = create_component('kbd')
mark = create_component('mark')
q = create_component('q')
s = create_component('s')
samp = create_component('samp')
small = create_component('small')
span = create_component('span')
strong = create_component('strong')
sub = create_component('sub')
sup = create_component('sup')
time = create_component('time')
u = create_component('u')
var = create_component('var')

# Image and video
img = create_component('img', allow_children=False)
audio = create_component('audio')
video = create_component('video')
source = create_component('source', allow_children=False)

# Table content
caption = create_component('caption')
col = create_component('col')
colgroup = create_component('colgroup')
table = create_component('table')
tbody = create_component('tbody')
td = create_component('td')
tfoot = create_component('tfoot')
th = create_component('th')
thead = create_component('thead')
tr = create_component('tr')

# Forms (only read only aspects)
meter = create_component('meter')
output = create_component('output')
progress = create_component('progress')
input_ = create_component('input', allow_children=False)
button = create_component('button')
label = create_component('label')

# Interactive elements
details = create_component('details')
dialog = create_component('dialog')
menu = create_component('menu')
menuitem = create_component('menuitem')
summary = create_component('summary')

style = create_component('style')
