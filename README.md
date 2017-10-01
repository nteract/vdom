# [VDOM](https://github.com/nteract/vdom)

## Why use VDOM?

- Write **Declarative** Pythonic layouts.
- Render the layout in Jupyter frontends.
- Serialize layout for rehydration in your web app.

:warning: This library is a work in progress. :warning:

## Check out the power of VDOM!

Start with Python code and run it:

```python
from IPython.display import display
from vdom.helpers import h1, p, img, div, b

display(
    div(
        h1('Our Incredibly Declarative Example'),
        p('Can you believe we wrote this ', b('in Python'), '?'),
        img(src="https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif"),
        p('What will ', b('you'), ' create next?'),
    )
)
```

**Voila!** Your layout is served below:

# Now Incredibly Declarative

Can you believe we wrote this **in Python**?

![](https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif)

What will **you** create next?

---

## Install the Python package

```bash
pip install vdom
```

## Developer install from source code

```bash
git clone https://github.com/nteract/vdom
cd vdom
pip install -e .
```

## We welcome feedback.

Since this project and its API is still a work in progress, we would love to
hear your thoughts on the API and suggestions for enhancements. Please take a look at the [VDOM spec](docs/spec.md) too.

## Find out more about nteract

Take a look at the [nteract website](https://nteract.io) to see other projects
that we are working on.
