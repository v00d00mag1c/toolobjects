You can log messages via Logger is an entity that allows to print messages. It can be used directly as a singletone, or from section mixin functions:

self.log()

it will set the section and prefix automatically.

Logger creates Log objects. They contain section - maybe, place where message is from? Prefix - identifier if section does not fixes the mess. Message - text of message. Role - list with roles of message. It can contain any strings, but "error", "success" will change it color.

### Hiding useless messages

Option logger.print.exclude allows to hide some logs from being displayed. It uses App.Logger.HideCategory class.

i may recomend:

```
    "logger.print.exclude": [
        {
            "role": "objects_loading"  
        }
    ],
    "logger.print.file": false,
    "logger.print.console.show_time": false,
    "logger.print.console.show_role": true,
```
