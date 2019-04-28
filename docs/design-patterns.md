# Design Patterns

The main operating principle for `vdom` (virtual DOM) is:

> Write functions that return `vdom` elements

In matching with `React` parlance, we'll call these functions **components**. This allows you
to share, remix, and use components amongst everyone. You'll be able to compose together
components to create greater components than you have before.

## Introductory component

We'll start with a **component** that takes a level of happiness and produces a light visualization:

```python
from vdom.helpers import div, span, p, meter

def happiness(level=90):
  smiley = "😃"
  percent = level / 100.
    
  if(percent < 0.25):
    smiley = "☹️"
  elif(percent < 0.50):
    smiley = "😐"
  elif(percent < 0.75):
    smiley = "😀"

    
  return span(
      p('Happiness ', smiley),
      meter(level, min=0, low=25, high=75, optimum=90, max=100, value=level)
  )
```

The user of the component only needs to call it with a level of happiness from 0 to 100.

```python
happiness(96)
```

<span>
<p>Happiness 😃</p>
<meter min="0" low="25" high="75" optimum="90" max="100" value="96">
  96
</meter>
</span>

------------

:tada: Our first component is ready! Since we can think of `happiness` as a little building block component,
we can put several of these together to create whole layouts:

```python
div(
  happiness(10),
  happiness(32),
  happiness(65),
  happiness(80)
)
```

<span>
<p>Happiness ☹️</p>
<meter min="0" low="25" high="75" optimum="90" max="100" value="10">
  10
</meter>
</span>
<span>
<p>Happiness 😐</p>
<meter min="0" low="25" high="75" optimum="90" max="100" value="32">
  32
</meter>
</span>
<span>
<p>Happiness 😀</p>
<meter min="0" low="25" high="75" optimum="90" max="100" value="65">
  65
</meter>
</span>
<span>
<p>Happiness 😃</p>
<meter min="0" low="25" high="75" optimum="90" max="100" value="80">
  80
</meter>
</span>

-------------------


## Working with Python objects

For this section, you'll need `ggplot` and `matplotlib` packages installed. We'll create a component,
`fancy_hist`, that creates a histogram which allows for displaying side by side:

```python
import matplotlib.pyplot as plt
import io, base64, urllib
from ggplot import mpg
from vdom.helpers import div, span, p, h1, img

def fancy_hist(value, data=mpg, title="Plot", bins=12, style=None):
    if(style is None):
        style = {"display": "inline-block"}
    
    f = plt.figure()
    plt.hist(value, bins=bins, data=data)

    buf = io.BytesIO()
    f.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    
    plt.close()
        
    return div(
        h1(title),
        p(str(bins), " bins"),
        img(src='data:image/png;base64,' + urllib.parse.quote(string)),
      style=style
    )
```


```python
fancy_hist('cty', data=mpg, title="City MPG")
```

<div style="display: inline-block">
  <h1>City MPG</h1>
  <p>12 bins</p>
  <img src="https://user-images.githubusercontent.com/1857993/56857882-2b79d300-6938-11e9-8a5a-a7ad31e62ab1.png">
</div>


```python
div(
  fancy_hist('hwy', data=mpg, title="Highway MPG"),
  fancy_hist('cty', data=mpg, title="City MPG")
)

```

<div>
<div style="display: inline-block;"><h1>Highway MPG</h1><p>12 bins</p><img src="https://user-images.githubusercontent.com/1857993/56857868-fff6e880-6937-11e9-9cdf-5a2e95ae5bed.png"></div>
<div style="display: inline-block;"><h1>City MPG</h1><p>12 bins</p><img src="https://user-images.githubusercontent.com/1857993/56857850-dc33a280-6937-11e9-913d-15baf48aaca3.png"></div>
</div>
