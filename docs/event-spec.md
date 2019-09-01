# VDOM Event Support

This documents how vdom can be used to handle DOM events in Python and create
interactive widgets similar to Jupyter widgets (ipywidgets).

This allows vdom users to quickly and efficiently create UI for interacting with
a kernel. For example, a user could filter large datasets on the kernel using an
`onChange` event on an `input` element to minimize memory usage on the client or
use buttons, sliders, and other UI controls to tweak algorithm parameters.

## Usage

To add event handlers to your VDOM all you need to do is define an attribute whose value
is callable. In the example below we show how you can create a simple button that responds
to click events:

```py
from vdom import button
from ipython.display import display

# Create a variable to store counter state
count = 0

# Define an "on-click" handler
def on_click(event):
    global count
    count += 1
    # Use ipython's `update_display` feature to update the counter's output/display
    counter_display.update(counter())

# Create a function that returns the counter vdom object
# We will use this to render the counter initially and update it when `count` changes
def counter():
    return button(str(count), onClick=on_click, style={'width': 100, 'height': 40})

# Create a display handle that we can update in the click handler
counter_display = display(counter(), display_id=True)

# Display the counter
counter_display;
```

### Advanced Event Behavior

In some use cases it's neccssary to tinker with the behavior of events after they occur.
For example, you might want to stop an ancor element from jumping to its `href` when
clicked or you might want to prevent an event from bubbling up to a parent handler. Both
of these goals can be achieved by using an `eventHandler` decorator. In the following
example we've registered an "on-click" handler to an ancor, and to an outer div. If the
`inner_on_click` handler **didn't** `preventDefault` and `stopPropogation`, upon clicking
the ancor, the page would jump to the top as the `href` indicates and we would see a
printout for both the inner and outer click handlers. However, the page will not jump to
the top because `preventDefault=True`, and only the inner click hander will respond to
the event because `stopPropogation=True`:

```py
import vdom
from ipython.display import display

def outer_on_click(event):
    print("outer")

@vdom.eventHandler(preventDefault=True, stopPropogation=True)
def inner_on_click(event):
    print("inner")

model = vdom.div(
    vdom.a("click this link", href-"#", onClick=inner_on_click)
    onClick=outer_on_click,
)

display(model, display_id=True)
```


## How it works

### On the kernel

For any vdom attribute whose value is callable (e.g. event handler function),
vdom will:

1. Register a new comm channel
2. On incoming messages, call the event handler with the event object (dict) as
   the single argument
3. Replace the attribute value with an object with the following signature:

```python
{
    '{eventName}': {
        'hash': string,
        'stopPropagation': boolean,
        'preventDefault': boolean
    }
}
```

4. Move the attribute from the `attributes` property of the vdom object to the
   `event_handlers` property

### On the client

For any event handlers in the vdom object, the
[transform-vdom](https://github.com/nteract/nteract/tree/master/packages/transform-vdom)
will:

1. Connect to the comm channel of that target name value
2. Replace the attribute value with an anonymous function that will send a comm
   message to that comm channel with the event object as the single argument

As a result, like using React in Javascript, vdom elements can define event
handlers as Python functions for DOM events such as `click`, `change`, `scroll`,
etc. When those DOM events occur on the client, a comm message containing the
event object (as described in the [Reference section](#reference)) is sent to
the kernel, and the Python function is called with the event object as its
argument.

## Supported Events

- [Clipboard Events](#clipboard-events)
- [Composition Events](#composition-events)
- [Keyboard Events](#keyboard-events)
- [Focus Events](#focus-events)
- [Form Events](#form-events)
- [Mouse Events](#mouse-events)
- [Pointer Events](#pointer-events)
- [Selection Events](#selection-events)
- [Touch Events](#touch-events)
- [UI Events](#ui-events)
- [Wheel Events](#wheel-events)
- [Media Events](#media-events)
- [Image Events](#image-events)
- [Animation Events](#animation-events)
- [Transition Events](#transition-events)
- [Other Events](#other-events)

## Reference

### Clipboard Events

Event types:

```
onCopy
onCut
onPaste
```

Event object:

```javascript
{
  clipboardData: DOMDataTransfer
}
```

### Composition Events

Event types:

```
onCompositionEnd
onCompositionStart
onCompositionUpdate
```

Event object:

```javascript
{
  data: string
}
```

### Keyboard Events

Event types:

```
onKeyDown
onKeyPress
onKeyUp
```

Event object:

```javascript
{
  altKey: boolean,
  charCode: number,
  ctrlKey: boolean,
  key: string,
  keyCode: number,
  locale: string,
  location: number,
  metaKey: boolean,
  repeat: boolean,
  shiftKey: boolean,
  which: number
}
```

### Focus Events

Event types:

```
onFocus
onBlur
```

Event object:

```javascript
{}
```

### Form Events

Event types:

```
onChange
onInput
onInvalid
onSubmit
```

```javascript
{
  value: string
}
```

### Mouse Events

Event types:

```
onClick
onContextMenu
onDoubleClick
onDrag
onDragEnd
onDragEnter
onDragExit
onDragLeave
onDragOver
onDragStart
onDrop
onMouseDown
onMouseEnter
onMouseLeave
onMouseMove
onMouseOut
onMouseOver
onMouseUp
```

Event object:

```javascript
{
  altKey: boolean,
  button: number,
  buttons: number,
  clientX: number,
  clientY: number,
  ctrlKey: boolean,
  metaKey: boolean,
  pageX: number,
  pageY: number,
  screenX: number,
  screenY: number,
  shiftKey: boolean
}
```

### Pointer Events

Event types:

```
onPointerDown
onPointerMove
onPointerUp
onPointerCancel
onGotPointerCapture
onLostPointerCapture
onPointerEnter
onPointerLeave
onPointerOver
onPointerOut
```

Event object:

```javascript
{
  pointerId: number,
  width: number,
  height: number,
  pressure: number,
  tiltX: number,
  tiltY: number,
  pointerType: string,
  isPrimary: boolean
}
```

### Selection Events

Event types:

```
onSelect
```

Event object:

```javascript
{}
```

### Touch Events

Event types:

```
onTouchCancel
onTouchEnd
onTouchMove
onTouchStart
```

Event object:

```javascript
{
  altKey: boolean,
  ctrlKey: boolean,
  metaKey: boolean,
  shiftKey: boolean
}
```

### UI Events

Event types:

```
onScroll
```

Event object:

```javascript
{
  detail: number
}
```

### Wheel Events

Event types:

```
onWheel
```

Event object:

```javascript
{
  deltaMode: number,
  deltaX: number,
  deltaY: number,
  deltaZ: number
}
```

### Media Events

Event types:

```
onAbort
onCanPlay
onCanPlayThrough
onDurationChange
onEmptied
onEncrypted
onEnded
onError
onLoadedData
onLoadedMetadata
onLoadStart
onPause
onPlay
onPlaying
onProgress
onRateChange
onSeeked
onSeeking
onStalled
onSuspend
onTimeUpdate
onVolumeChange
onWaiting
```

Event object:

```javascript
{}
```

### Image Events

Event types:

```
onLoad
onError
```

Event object:

```javascript
{}
```

### Animation Events

Event types:

```
onAnimationStart
onAnimationEnd
onAnimationIteration
```

Event object:

```javascript
{
  animationName: string,
  pseudoElement: string,
  elapsedTime: float
}
```

### Transition Events

Event types:

```
onTransitionEnd
```

Event object:

```javascript
{
  propertyName: string,
  pseudoElement: string,
  elapsedTime: float
}
```

### Other Events

Event types:

```
onToggle
```

Event object:

```javascript
{}
```
