# [VDOM](https://github.com/nteract/vdom)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Why use VDOM

- Write **Declarative** Pythonic layouts.
- Create headings, prose, images, and more common user interface items with user-friendly declarative statements.
- Render the layout in _Jupyter_ frontends, such as **nteract** and JupyterLab.
- Serialize the layout for rehydration and later use in your web app.

---

## Check out the power of VDOM

Create layouts by writing and running Python code. Let's see an example
below to create and display a heading, styled prose, and a GIF:

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

**Voila!**

Your example created a layout and served it below:

# Now Incredibly Declarative

Can you believe we wrote this **in Python**?

![](https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif)

What will **you** create next?

---

## Getting started

### Install the Python package

```bash
pip install vdom
```

### Usage

First, import `vdom.helpers` for headings, text, and images:

```python
from vdom.helpers import h1, p, img, div, b
```

Create a layout using the VDOM helpers in Python code. Here's an example code
layout block:

```python
my_pretty_layout = div(
    h1('Our Incredibly Declarative Example'),
    p('Can you believe we wrote this ', b('in Python'), '?'),
    img(src="https://media.giphy.com/media/xUPGcguWZHRC2HyBRS/giphy.gif"),
    p('What will ', b('you'), ' create next?'),
)
```

To display the layout, use IPython's display method:

```python
from IPython.display import display


display(my_pretty_layout)
```

The full example, including rendered output, is found [above](#check-out-the-power-of-vdom).

## Documentation

- [Design Patterns](./docs/design-patterns.md)
- [Specification - VDOM Media Type](./docs/mimetype-spec.md)
- [Specification - VDOM Event Support](./docs/event-spec.md)

## Contribute to VDOM

### Developer install from source code

```bash
git clone https://github.com/nteract/vdom
cd vdom
pip install -e .
```

### Contributing Guidelines and Releases

We follow these [Contributing Guidelines](CONTRIBUTING.md).

For contributors helping with creating releases, the [RELEASING.md] document
outlines the process.

## Find out more about nteract

Take a look at the [nteract website](https://nteract.io) to see other projects
that we are working on.
