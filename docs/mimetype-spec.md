# VDOM Media Type

This documents the media type `application/vdom.v1+json` as used in Jupyter and
nteract frontends.

## `VDOMElement`

The top level object is a `VDOMElement`, defined in JavaScript as:

```js
{
  // HTML tags like h1, b, p, marquee, etc.
  tagName: string,  // Should allow standard elements & web components

  // See below
  children: VDOMNode,
  attributes: Object,

  // Optional
  key: number | string | null
}
```

## What makes up a `VDOMElement`?

⚠️ Frontends can disallow certain attributes or elements to mitigate XSS security concerns. ⚠️

### `VDOMNode`

A `VDOMNode` may be a `VDOMEl`, a `string` an `Array<VDOMNode>`, or `null`.

### `tagName`

The `tagName` can be any HTML element. By extension, this means any web
component that is available on the page will work as well, in addition
to other new elements.

### `children`

`children` can be a `VDOMNode`, which is a `VDOMEl`, a `string` an
`Array<VDOMNode>`, or `null`

### `attributes`

The literal attributes to passthrough to the element.

#### `style`

The `style` attribute is expected to be an object with `camelCased` properties, matching with the
[DOM API for CSS in JavaScript](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Manipulating_documents#Manipulating_styles).


## An example

A `VDOMElement` represented in JSON:

```json
{
  "tagName": "a",
  "attributes": {
    "href": "https://nteract.io"
  },
  "children": "nteract site"
}
```

becomes the following HTML:

```html
<a href="https://nteract.io">nteract site</a>
```


### Coding style and syntax

All [DOM properties and attributes should be camelCased](https://facebook.github.io/react/docs/dom-elements.html#all-supported-html-attributes).
This may [no longer be a restriction in the future](https://facebook.github.io/react/blog/2017/09/08/dom-attributes-in-react-16.html) however.
