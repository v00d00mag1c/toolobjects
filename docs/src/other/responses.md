### Responses

Usually scripts are using only one type of response - [ObjectsList](../objects/App.Objects.Responses.ObjectsList.md). But there also [AnyResponse](../objects/App.Objects.Responses.AnyResponse.md) that can return any value, [Error](../objects/App.Objects.Responses.Error.md) that represents error, [NoneResponse](../objects/App.Objects.Responses.NoneResponse.md) and [Responses](../objects/App.Objects.Responses.Responses.md) — many other responses.

ObjectsList is used in [Extractor](../objects/App.Objects.Extractor.md). It has fields: 

`supposed_to_be_single` that does nothing, but can have value in hypothetical client

`unsaveable` — values will not be flushed. It means the list of objects that are got inside app, e.g. found from search.

`ignore_flush_hooks` — ignores hooks on flushing.
