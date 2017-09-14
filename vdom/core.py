def toJSON(el):
    if(type(el) is str):
        return el
    if(type(el) is list):
        return list(map(toJSON, el))
    if(hasattr(el, 'tagName') and hasattr(el, 'attributes')):
        return {
            'tagName': el.tagName,
            'attributes': el.attributes,
            'children': toJSON(el.children)
        }
    return el

class VDOM():
    def __init__(self, obj):
        self.obj = obj

    def _repr_mimebundle_(self, include, exclude, **kwargs):
        return {
                'application/vdom.v1+json': toJSON(self.obj)
        }
def createElement(tagName):
    class VDOMEl():
        def __init__(self, children=None, **kwargs):
            self.children = children
            self.attributes = kwargs
            self.tagName = tagName

        def _repr_mimebundle_(self, include, exclude, **kwargs):
            return VDOM(self)
    return VDOMEl


h1 = createElement('h1')
p = createElement('p')
div = createElement('div')
