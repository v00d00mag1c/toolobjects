### App.Objects.Arguments.Argument

Object that allows to define what arguments something (executable) uses. It takes string on input and can convert it to stated in name value. To get final value, it uses class link from the `orig` field (`asArgument()`)

List of this must be passed in Data.DictList for convenience; it relays on "name" field

Argument can be used not only for validation, but for storing (queue prestart, variables)

`name`: name of the argument

`orig`: link to class that will be used for validation

`literally`: skip `asArgument()` and return class

`default`: What value will be set if nothing passed. callable can be passed here

`assertions`: List of App.Objects.Arguments.Assertions.*; post-getValue() checks. it saves "inputs" and "current" for this

`id_allow`: shortcut to get item by [uuid](App.Storage.StorageUUID)

`current`: what was got after "getValue()"

`auto_apply`: `current` will be set after constructor()

`check_json`: parses json from input value

`role` `['config', 'env']`: role for settings

#### Variations

[App.Objects.Arguments.ListArgument](App.Objects.Arguments.ListArgument.md)
[App.Objects.Arguments.LiteralArgument](App.Objects.Arguments.LiteralArgument.md)
