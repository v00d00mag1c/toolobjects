App creates the list of the objects at the start. It takes them from current working directory. That's allows to get Object by name and know in advance all of them.

### Namespaces

Namespace (App.Objects.Index.Namespace) is a dir from objects are loaded (`root`). There is two namespaces by default: current working directory and `Custom`. Objects from `Custom` folder should be called by `X`, not `Custom.X` because this folder is ignored by common namespace.

Custom namespaces can be added by option `objects.index.namespaces`, it can be any folder on pc

Custom objects can load malware, so the Namespace doesn't loads module after finding a file by default, but it did not helps. More, it creates problem to get all config 

You can switch between available namespaces with `objects.index.namespaces.current` settings by passing their names. You should pass `common` and `custom`

Namespace can contain prioritized names: `load_before` and `load_after`. It can load all objects once via `load_once`

To hide object load messages at the start:

```
    "logger.print.exclude": [
        {
            "role": "objects_loading"  
        }
    ]
```
