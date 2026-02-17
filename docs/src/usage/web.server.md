to run server only:

```
python tool.py -view App.Server
```

to run UI:

```
python tool.py -view App.Client
```

##### routes

`/?i={page}`: show displayment for object with name

`/api?i={object_name}`: call executable

`/rpc`: websocket connection

`/api/upload?storage={storage name}`: upload storage unit to some storage
