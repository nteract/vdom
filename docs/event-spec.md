# VDOM Event Support

This documents the event types (and respective event objects provided
to event handlers) supported by vdom elements.

## Usage

```py
count = 0

def on_click(event):
    global count
    count += 1
    my_display.update(counter())
    
def counter():
    return button(str(count), onClick=on_click, style={'width': 100, 'height': 40})

my_display = display(counter(), display_id=True)

my_display;
```

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
  target: {
    value: string
  }
}
```

### Mouse Events

Event types:

```
onClick
onContetMenu
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

