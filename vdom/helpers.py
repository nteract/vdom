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

# From https://developer.mozilla.org/en-US/docs/Web/HTML/Element

## Content sectioning
address = createComponent('address')
article = createComponent('article')
aside = createComponent('aside')
footer = createComponent('footer')
h1 = createComponent('h1')
h2 = createComponent('h2')
h3 = createComponent('h3')
h4 = createComponent('h4')
h5 = createComponent('h5')
h6 = createComponent('h6')
header = createComponent('header')
hgroup = createComponent('hgroup')
nav = createComponent('nav')
section = createComponent('section')

## Text content
blockquote = createComponent('blockquote')
dd = createComponent('dd')
div = createComponent('div')
dl = createComponent('dl')
dt = createComponent('dt')
figcaption = createComponent('figcaption')
figure = createComponent('figure')
hr = createComponent('hr')
li = createComponent('li')
ol = createComponent('ol')
p = createComponent('p')
pre = createComponent('pre')
ul = createComponent('ul')

## Inline text semantics
a = createComponent('a')
abbr = createComponent('abbr')
b = createComponent('b')
br = createComponent('br')
cite = createComponent('cite')
code = createComponent('code')
data = createComponent('data')
em = createComponent('em')
i = createComponent('i')
kbd = createComponent('kbd')
mark = createComponent('mark')
q = createComponent('q')
s = createComponent('s')
samp = createComponent('samp')
small = createComponent('small')
span = createComponent('span')
strong = createComponent('strong')
sub = createComponent('sub')
sup = createComponent('sup')
time = createComponent('time')
u = createComponent('u')
var = createComponent('var')

## Image and video
img = createComponent('img')
audio = createComponent('audio')
video = createComponent('video')
source = createComponent('source')

## Table content
caption = createComponent('caption')
col = createComponent('col')
colgroup = createComponent('colgroup')
table = createComponent('table')
tbody = createComponent('tbody')
td = createComponent('td')
tfoot = createComponent('tfoot')
th = createComponent('th')
thead = createComponent('thead')
tr = createComponent('tr')

## Forms (only read only aspects)
meter = createComponent('meter')
output = createComponent('output')
progress = createComponent('progress')
input_ = createComponent('input')

## Interactive elements
details = createComponent('details')
dialog = createComponent('dialog')
menu = createComponent('menu')
menuitem = createComponent('menuitem')
summary = createComponent('summary')


