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

from .core import createComponent

# From https://developer.mozilla.org/en-US/docs/Web/SVG/Element

## Animation elements
animate = createComponent('animate')
animateColor = createComponent('animateColor')
animateMotion = createComponent('animateMotion')
animateTransform = createComponent('animateTransform')
discard = createComponent('discard')
mpath = createComponent('mpath')
set_ = createComponent('set')

## Basic shapes
circle = createComponent('circle')
ellipse = createComponent('ellipse')
line = createComponent('line')
polygon = createComponent('polygon')
polyline = createComponent('polyline')
rect = createComponent('rect')

## Container elements
a = createComponent('a')
defs = createComponent('defs')
g = createComponent('g')
marker = createComponent('marker')
mask = createComponent('mask')
missing_glyph = createComponent('missing-glyph')
pattern = createComponent('pattern')
svg = createComponent('svg')
switch = createComponent('switch')
symbol = createComponent('symbol')
unknown = createComponent('unknown')

## Descriptive elements
desc = createComponent('desc')
metadata = createComponent('metadata')
title = createComponent('title')

## Filter primitive elements
feBlend = createComponent('feBlend')
feColorMatrix = createComponent('feColorMatrix')
feComponentTransfer = createComponent('feComponentTransfer')
feComposite = createComponent('feComposite')
feConvolveMatrix = createComponent('feConvolveMatrix')
feDiffuseLighting = createComponent('feDiffuseLighting')
feDisplacementMap = createComponent('feDisplacementMap')
feDropShadow = createComponent('feDropShadow')
feFlood = createComponent('feFlood')
feFuncA = createComponent('feFuncA')
feFuncB = createComponent('feFuncB')
feFuncG = createComponent('feFuncG')
feFuncR = createComponent('feFuncR')
feGaussianBlur = createComponent('feGaussianBlur')
feImage = createComponent('feImage')
feMerge = createComponent('feMerge')
feMergeNode = createComponent('feMergeNode')
feMorphology = createComponent('feMorphology')
feOffset = createComponent('feOffset')
feSpecularLighting = createComponent('feSpecularLighting')
feTile = createComponent('feTile')
feTurbulence = createComponent('feTurbulence')

## Font elements
font = createComponent('font')
font_face = createComponent('font-face')
font_face_format = createComponent('font-face-format')
font_face_name = createComponent('font-face-name')
font_face_src = createComponent('font-face-src')
font_face_uri = createComponent('font-face-uri')
hkern = createComponent('hkern')
vkern = createComponent('vkern')

## Gradient elements
linearGradient = createComponent('linearGradient')
meshgradient = createComponent('meshgradient')
radialGradient = createComponent('radialGradient')
stop = createComponent('stop')

## Graphics elements
image = createComponent('image')
mesh = createComponent('mesh')
path = createComponent('path')
text = createComponent('text')
use = createComponent('use')

## Graphics referencing elements
audio = createComponent('audio')
iframe = createComponent('iframe')
video = createComponent('video')

## HTML elements
canvas = createComponent('canvas')

## Light source elements
feDistantLight = createComponent('feDistantLight')
fePointLight = createComponent('fePointLight')
feSpotLight = createComponent('feSpotLight')

## Never-rendered elements
clipPath = createComponent('clipPath')
hatch = createComponent('hatch')
script = createComponent('script')
style = createComponent('style')

## Paint server elements
solidcolor = createComponent('solidcolor')

## Renderable elements
foreignObject = createComponent('foreignObject')
textPath = createComponent('textPath')
tspan = createComponent('tspan')

## Text content elements
altGlyph = createComponent('altGlyph')
altGlyphDef = createComponent('altGlyphDef')
altGlyphItem = createComponent('altGlyphItem')
glyph = createComponent('glyph')
glyphRef = createComponent('glyphRef')
tref = createComponent('tref')

## Uncategorized elements
color_profile = createComponent('color-profile')
cursor = createComponent('cursor')
filter_ = createComponent('filter')
hatchpath = createComponent('hatchpath')
meshpatch = createComponent('meshpatch')
meshrow = createComponent('meshrow')
view = createComponent('view')
