### Web server

The "web" view is object "App.Web.Server":

```
python tool.py -view App.Web.Server
```

Default host (`web.options.host`) and port (`web.options.port`) are 127.0.0.1:22222.

It contains these routes:

`/api` (GET)

The same as ConsoleView: runs object from `i` param from `pre_i` executable (that was passed before server running), returns results in json. Arguments must be passed in `application/json` content-type.

`/rpc` (GET)

WebSocket-connection. You must pass data in json-format, common args at the `payload`, `type` as `object` and `event_index` (any if you don't need to distinguish messages)

```
{
    "type": "object",
    "event_index": 0,
    "payload": {
        "i": "Media.Text.Text",
        "force_flush": 1,
        "value": "1234"
    }
}
```

It will back results with the same `event_index` and `type`.

Also it pushes log messages with type=`log` (and probaly variables messages).

`/storage/{storage}/{uuid}/{path:.*}` (GET)

Returns file from storage unit. The storage name is passed in {storage}, uuid is in {uuid}, path can contain get any file in storage unit dir.

`/api/upload/{storage}` (POST)

Creates new storage unit and moves uploaded file to created dir. File must be passed as multipart/formdata in `file` field.

### Auth

...

### Web client

...
