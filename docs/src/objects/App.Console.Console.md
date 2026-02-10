### App.Console.Console

Console (and the default) interface of the app.

To run scripts:

```
python tool.py -i App.Tests.Console.ConsoleLogTest
```

If the argument name contains dots, it should be passed with two dashes:

```bash
python tool.py -i Media.Get -object Media.Text -text 123 -force_flush 1 --force_flush.as_args 1
```

By default it returns text that describes object (from `_display_as_string()` function) with it uuid, if return result is [ObjectsList](App.Objects.Responses.ObjectsList.md). To not show its uuids, pass `--console.print.display_ids 0`. 
<!--The divider between those items is defined by `--console.print.divider`.-->

If you want to display results as json, pass `--console.print.as json`. To not print anything, pass `--console.print 0`.

Auth token is passed in `auth`. By default it logs as root.

There is no way to pass JSON in cmd.

#### Config override

Config values can be overriden in runtime with those arguments:

```
python tool.py --c.logger.print.exclude "[]"
```

### Related

* [App.Console.Interactive](App.Console.Interactive.Interactive.md)
