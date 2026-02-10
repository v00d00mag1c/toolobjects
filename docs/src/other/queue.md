### Queue

Object that allows to create sequence of another objects. 

Fields:

`prestart`: arguments and variables

`items`: sequence of executables

`output`: format of response (relies on `response_name` and `value`)

`prestart` and `items` contains `predicate` — the name of the object, `build` — constructor values and `arguments` — what will be passed in `execute()`.

Values in `arguments` can be actual value or a reference to one of queue's element. "specific" arguments are dict with one of these values:

`direct_value` ([LinkValue](../objects/App.Objects.Queue.LinkValue.md)) — references to `prestart` or `items` element. It gets element by prefix and it's index. `#` prefix means the value from `items`, `$` means the value from `prestart`. It can get any property of the object, so there can be a vulnerability. Notice that values from `prestart` should be get like `$0.arg_value`.

`replacements` ([ValueWithReplaces](../objects/App.Objects.Queue.ValueWithReplaces.md)) — allows to insert `direct_value` to some string. It looks like this:

```
{
    'predicate': 'Data.Random.GetInt',
    'arguments': {
        'min': 0,
        'max': 80
    }
},
{
    'predicate': 'Web.URL',
    'build': {
        'value': {
            'value': 'https://example.com/images/',
            'replacements': [{
                'position': (28, 29),
                'value': '#0.arg_value'
            }]
        }
    },
    'arguments': {
        'force_flush': True,
        'do_save': False
    }
}
```

Let see the "replacements": why not to use `format()` function? also it's inconvenient to measure the distance to character, but however.

Queue runs by:

```
python tool.py -i App.Objects.Queue.Run -queue [id]
```

An object of Queue can be created via `App.Objects.Queue.Create` or `force_flush`. But it's impossible to pass JSON from console, so try to create it in DB viewer.
