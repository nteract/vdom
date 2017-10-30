# Releasing

[Jump to Summary](#summary)

## Prerequisites

```
pip install --upgrade pip
pip install twine
```

## Detailed Steps

:warning: Make sure you're on latest master (or whatever commit is being shipped) and that your workspace is clean. 

Pick the next tag (e.g. `0.5`) by looking at the current tags:

```
$ git tag
0.1
0.2
0.3
0.4
```

Then go ahead and tag it,

```
git tag 0.5
```

push up the tagged commit,

```
git push && git push --tags
```

build it,

```
python setup.py sdist bdist_wheel
```

and ship it:

```
twine upload dist/vdom-0.5*
```


## Summary

```
git tag x.y
git push && git push --tags
python setup.py sdist bdist_wheel
twine upload dist/*
```

## TODO

* [ ] Provide a way to test the release
* [ ] Ensure that we're on latest master, shipping from the right tag
* [ ] Track `CHANGES` somehow
