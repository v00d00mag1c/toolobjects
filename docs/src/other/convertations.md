### Convertations

Object can be converted to another type if it defined. To show available convertations of object:

```
python tool.py -i App.Objects.Convertations.Show -from [object name]
```

To convert object:

```
python tool.py -i App.Objects.Convertations.Convert -from [object id] -to [object id] -save_to common
```

The convertations of each class are defined in submodules with the role = ['convertation'].

```
@classmethod
def _submodules(cls) -> list:
    from Data.Types.XML.XMLToJson import XMLToJson

    return [
        Submodule(
            item = XMLToJson,
            role = ['convertation']
        )
    ]
```

`item` must be a class that extends from [Convertation](../objects/App.Objects.Convertation.md). It must have submodules with roles 'object_in' and 'object_out':

```
@classmethod
def _submodules(cls) -> list[Submodule]:
    return [
        Submodule(
            item = XML,
            role = ['object_in']
        ),
        Submodule(
            item = JSON,
            role = ['object_out']
        )
    ]
```
