### Autostart and daemons

After the start of the [Server](../objects/App.Server.md), it runs autostart scripts. They are stored in config, in `app.autostart.items` value:

```
"app.autostart.items": [
    {
        "deactivated": false,
        "args": {
            "i": "App.Objects.Operations.ExecuteIterative",
            "i_2": "App.Tests.Console.ConsoleLogTest",
            "max_iterations": 10,
            "auth": "root"
        }
    }
]
```

You may use [App.Objects.Operations.ExecuteIterative](../objects/App.Objects.Operations.ExecuteIterative.md) to create a loop of one function.

Because all objects requires user, you must pass token in `auth` or pass "root" if `app.autostart.as_root` = true.
