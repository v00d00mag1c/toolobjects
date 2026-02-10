### Implementing TODO list

We need to create the class. "TODO" is too general name, we need some more common, so choosing "Checkmarks". It's will be in "Data" category.

We divide the checkmarks list and Checkmark. Two files can't be at the same level with other `Data` classes, moving it to separate dir.

Checkmarks will be linked to List, contain `state` that shows was they checked and `label`

`Data.Checkmarks.List`:

```
from App.Objects.Object import Object

class List(Object):
    pass
```

`Data.Checkmarks.Checkmark`:

```
from App.Objects.Object import Object
from pydantic import Field

class Checkmark(Object):
    state: bool = Field(default = False)
    label: str = Field()
```

Trying to save?

```cli
> python tool.py -i Data.Checkmarks.List -force_flush 1 -save_to common
> python tool.py -i Data.Checkmarks.Checkmark -label 123 -force_flush 1 -save_to common
> python tool.py -i App.DB.Link -owner {id1} -items {id2}
```

Getting from db:

```
> python tool.py -i App.DB.Search -storage common -uuids {id1}

<Data.Checkmarks.List> [common_0]
```

OK, lets add checkmarks list showing:

...

It's so nested, but it works and shows many ids:

```
Checkmarks list "None"
[ ] 123 [content_1]
[content_0]
```

Let's add API for marking as checked:

```
class SetChecked(Act):
    @classmethod
    def _arguments(cls) -> ArgumentDict:
        return ArgumentDict(items = [
            Argument(
                name = 'item',
                by_id = True,
                orig = Checkmark
            ),
            Argument(
                name = 'state',
                default = False,
                orig = Boolean
            )
        ])
    
    def implementation(self, i):
        item = i.get('item')
        item.state = i.get('state')
        item.save()

        return ObjectsList(items = [item])
```

Calling it:

```
> python tool.py -i Data.Checkmarks.SetChecked -item content_0 -state 1
```

Calling `App.DB.Search` will show that it was checked.
