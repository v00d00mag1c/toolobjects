### App.Objects.Argument

Object that used in some validation cases.

#### name

Name of the argument

### orig

The class that will be used to compare is passed in `orig` field. It may be a link to class or class instance. During the validation, it will call class function `asArgument()` that will convert input value to value that expected, or `asArgumentAsInstance()` if `orig` is an instance. Any class can be passed as `orig`.

For example, if you need to get integer value from input, `orig` should be [Data.Types.Int](Data.Types.Int.md). If you need to define the min and max values, it should be something like:

```
Argument(
    name = 'year',
    orig = Int(
        min_value = 0,
        max_value = 2026
    )
)
```

#### default

If nothing returned from `asArgument`, it returns `default` value. `default` can be a function. 

#### is_sensitive

Should `default` be hidden.

#### config_fallback

Gets the value from config if the input value is `None`. It's a tuple, first element is the name of the option, second is boolean: True: if this option is from the `env` and False: this option is from the `config`.

#### allowed_values

Values that allowed to get. Contains [App.Objects.Arguments.AllowedValues](App.Objects.Arguments.AllowedValues.md) item.

#### assertions

List of App.Objects.Arguments.Assertions objects. They can be NotNone, InputNotInValues.

#### by_id

If `by_id` is True, the value is allowed to be an id and the object with this name will be returned.

### Other

- If script needs to get multiple values, it should use [ListArgument](../objects/App.Objects.Arguments.ListArgument.md).

- There is no difference between None and Undefined and python, so if the value is set to `None` is the same that it was not set.

#### Argument names

- Name of the argument should be short and reflect what it affects.
- If argument refers to behavior of another argument, the name should contain the name of argument that it refers, for example, `force_flush` and `force_flush.as_args`.
- Forbidden arguments names are `i`, `auth` etc.
