# VDOM

Write Declarative Pythonic layouts, render in Jupyter frontends, or serialize for rehydration in your web app.

:warning: This library is a work in progress. We'd love your input on the exposed API :warning:

```python
from vdom import VDOM, h1, p, img, div, b

VDOM(
    div([
        h1('Now Incredibly Declarative'),
        p(['Can you believe we wrote this ', b('in Python'), '?']),
        img(src="https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif"),
    ])
)
```

-----------------------

# Now Incredibly Declarative

Can you believe we wrote this *in Python*?

![](https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif)

-----------------------

## Install

```
pip install vdom
```

## Development

```
git clone https://github.com/nteract/vdom
cd vdom
pip install -e .
```
