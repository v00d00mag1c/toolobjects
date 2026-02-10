### Documentation

Functionality that allows to describe argument or object. In argument it is a `documentation` field, in object its the `_documentation` class method.

Example:

```
    Argument(
        name = 'define',
        default = False,
        orig = Boolean,
        documentation = Documentation(
            name = Key(
                value = 'Define prices of each new product'
            ),
            description = Key(
                value = 'On True, every item will receive it\'s own generated price. On False, the \"price\" should be set manually'
            )
        )
    ),
```

Values should contain text on english. The `key` can contain id of self that will allow to translate the string.

Locales are `.json` files ([example](../../../src/locales/en.json)) with ids and translations. They are stored in `src/locales`, but can be added via `app.locales.langs`. The current language id is the `app.locales.current` config value.
