#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vdom.svg
~~~~~~~~

Little helper functions for the SVG Elements.

from vdom.svg import rect, svg

svg(
    rect(x=10, y=10, width=100, height=100),
    width=120, height=120
)

"""

from .core import create_component

# From https://developer.mozilla.org/en-US/docs/Web/SVG/Element

# Animation elements
animate = create_component('animate')
animateColor = create_component('animateColor')
animateMotion = create_component('animateMotion')
animateTransform = create_component('animateTransform')
discard = create_component('discard')
mpath = create_component('mpath')
set_ = create_component('set')

# Basic shapes
circle = create_component('circle')
ellipse = create_component('ellipse')
line = create_component('line')
polygon = create_component('polygon')
polyline = create_component('polyline')
rect = create_component('rect')

# Container elements
a = create_component('a')
defs = create_component('defs')
g = create_component('g')
marker = create_component('marker')
mask = create_component('mask')
missing_glyph = create_component('missing-glyph')
pattern = create_component('pattern')
svg = create_component('svg')
switch = create_component('switch')
symbol = create_component('symbol')
unknown = create_component('unknown')

# Descriptive elements
desc = create_component('desc')
metadata = create_component('metadata')
title = create_component('title')

# Filter primitive elements
feBlend = create_component('feBlend')
feColorMatrix = create_component('feColorMatrix')
feComponentTransfer = create_component('feComponentTransfer')
feComposite = create_component('feComposite')
feConvolveMatrix = create_component('feConvolveMatrix')
feDiffuseLighting = create_component('feDiffuseLighting')
feDisplacementMap = create_component('feDisplacementMap')
feDropShadow = create_component('feDropShadow')
feFlood = create_component('feFlood')
feFuncA = create_component('feFuncA')
feFuncB = create_component('feFuncB')
feFuncG = create_component('feFuncG')
feFuncR = create_component('feFuncR')
feGaussianBlur = create_component('feGaussianBlur')
feImage = create_component('feImage')
feMerge = create_component('feMerge')
feMergeNode = create_component('feMergeNode')
feMorphology = create_component('feMorphology')
feOffset = create_component('feOffset')
feSpecularLighting = create_component('feSpecularLighting')
feTile = create_component('feTile')
feTurbulence = create_component('feTurbulence')

# Font elements
font = create_component('font')
font_face = create_component('font-face')
font_face_format = create_component('font-face-format')
font_face_name = create_component('font-face-name')
font_face_src = create_component('font-face-src')
font_face_uri = create_component('font-face-uri')
hkern = create_component('hkern')
vkern = create_component('vkern')

# Gradient elements
linearGradient = create_component('linearGradient')
meshgradient = create_component('meshgradient')
radialGradient = create_component('radialGradient')
stop = create_component('stop')

# Graphics elements
image = create_component('image')
mesh = create_component('mesh')
path = create_component('path')
text = create_component('text')
use = create_component('use')

# Graphics referencing elements
audio = create_component('audio')
iframe = create_component('iframe')
video = create_component('video')

# HTML elements
canvas = create_component('canvas')

# Light source elements
feDistantLight = create_component('feDistantLight')
fePointLight = create_component('fePointLight')
feSpotLight = create_component('feSpotLight')

# Never-rendered elements
clipPath = create_component('clipPath')
hatch = create_component('hatch')
script = create_component('script')
style = create_component('style')

# Paint server elements
solidcolor = create_component('solidcolor')

# Renderable elements
foreignObject = create_component('foreignObject')
textPath = create_component('textPath')
tspan = create_component('tspan')

# Text content elements
altGlyph = create_component('altGlyph')
altGlyphDef = create_component('altGlyphDef')
altGlyphItem = create_component('altGlyphItem')
glyph = create_component('glyph')
glyphRef = create_component('glyphRef')
tref = create_component('tref')

# Uncategorized elements
color_profile = create_component('color-profile')
cursor = create_component('cursor')
filter_ = create_component('filter')
hatchpath = create_component('hatchpath')
meshpatch = create_component('meshpatch')
meshrow = create_component('meshrow')
view = create_component('view')
