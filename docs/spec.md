# VDOM Media Type

This documents the mimetype `application/vdom.v1+json` as used in Jupyter frontends.

The top level object is a `VDOMElement`, defined as:

```js
{
  // h1, b, p, marquee, etc.
  tagName: string, // Should allow standard elements & web components
  
  // See below
  children: VDOMNode,
  attributes: Object,
  // Optional
  key: number | string | null
}
```

A `VDOMNode` is a `VDOMEl`, a `string` or an `Array<VDOMNode>`.

⚠️ For the sake of security, frontends can choose not to allow certain attributes or elements to mitigate XSS concerns. ⚠️

## `tagName`

The `tagName` can be any HTML element, which by extension means any web component that is available on the page will work as well in addition to other new elements.

## `children`

Any of `VDOMEl`, `string`, or an `Array<VDOMNode>`

## `attributes`

The literal attributes to passthrough to the element. Example:

```json
{
  "tagName": "a",
  "attributes": {
    "href": "https://nteract.io"
  },
  "children": "nteract site"
}
```

becomes

```html
<a href="https://nteract.io">nteract site</a>
```

`style` is expected to be an object with `camelCased` properties, matching with the [DOM API for CSS in JavaScript](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Manipulating_documents#Manipulating_styles).

All [DOM properties and attributes should be camelCased](https://facebook.github.io/react/docs/dom-elements.html#all-supported-html-attributes). This may [no longer be a restriction in the future](https://facebook.github.io/react/blog/2017/09/08/dom-attributes-in-react-16.html) however.
