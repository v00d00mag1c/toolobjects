### Search

[StorageItem](../objects/App.Storage.Item.StorageItem.md) encapsulates db and files. DB backend can be different, so we can't use the api of one lib. Every adapter must implement search functions in Query class. There will be a usage.

Firstly, we need to get it:

```
storage = app.Storage.get('tmp')
query = storage.adapter.getQuery()
```

Then we can add conditions:

```
from App.DB.Query.Values.Value import Value
from App.DB.Query.Condition import Condition
from App.DB.Query.Sort import Sort

...

query.addCondition(Condition(
    val1 = Value(
        column = 'content',
        json_fields = ['os']
    ),
    operator = '==',
    val2 = Value(
        value = 'sailfish'
    ),
))
```

`val1` means the first part of query, a value that will be compared. As content is stored in json string, json_fields defines the list of keys that will be used to get value. (`['info', 'system', 'os', 'name']` will mean `phone['info']['system']['os']['name']`).

`operator` defines the function that will be used between these two values. They are manually defined in adapter object.

`val2` means the value to compare.

Also we can add function to `val1`:

```
query.addCondition(Condition(
    val1 = Value(
        column = 'uuid',
        func = '%',
        args = [2]
    ),
    operator = '==',
    val2 = Value(
        value = 0
    )
))
```

We can add a condition to find objects only with some prototype:

```
query.where_object(Phone)
```

Also we can sort it randomly:

```
query.addSort(Sort(
    condition = Condition(
        val1 = Value(
            column = 'uuid',
            func = 'random',
        )
    )
))
```

We can get a count of items:

```
query.count()
```

And get the items:

```
lists = query.toObjectsList()
lists..unsaveable = True
```

---

There is an Act search function, [App.DB.Search](../objects/App.DB.Search.md):

```
python tool.py -i App.DB.Search -storage common -q phone --q.in_description 1
```
