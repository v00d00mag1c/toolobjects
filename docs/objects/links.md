### Links

Every object can be linked to each with `Linkable` mixin. 

#### Methods

`link()`, `addLink()`

TODO

#### Link object

`item` — python link to another Object

`role` — meta about link. what its purpose? List with roles (for example, "internal", "content")

#### Link insertions

You can insert linked class to any field of Object using the `App.Objects.LinkInsertion` class.

Firstly, you need to annotate it:

```
class Text(Object):
    text: str = Field(default = '')
```

to

```
from App.Objects.LinkInsertion import LinkInsertion

class Text(Object):
    text: str | LinkInsertion = Field(default = '')
```

then you should call `toInsert()` in the got link and set the annotated field.

on model serialization, every LinkInsertion will be replaced to Link.item value. To define what field it will took, LinkInsertion takes `field`
