### Implementing script

**Validation**

Validation arguments are passed in _arguments:

```
@classmethod
def _arguments(cls) -> ArgumentsDict:
    return ArgumentsDict(items=[])
```

`items` list must contain [`App.Objects.Arguments.Argument`](../api/App.Objects.Arguments.Argument.md) Related: [`App.Objects.Arguments.ArgumentDict`](../api/App.Objects.Arguments.ArgumentDict.md)

**Entry point**

Logic of the class must be in `_implementation()` method:

```
    async def _implementation(self, i) -> Response:
        ...
```

All validated items will be returned as [`App.Objects.Arguments.ArgumentValues`](../api/App.Objects.Arguments.ArgumentValues.md) in `i` param. `_implementation()` is internal-only, to call another [`App.Objects.Executable`](../api/App.Objects.Executable.md) use `await execute({})`: it will automatically validate arguments and run hooks.

`_implementation()` should return [`Response`](../api/App.Objects.Responses.Response.md) (except `Extractor`) or return nothing.

**Settings**

To add settings, use:

```
    @classmethod
    def _settings(cls):
        return []
```

list must contain Arguments.

to get value of the option, use `self.getOption(name)`
