every executable has execute() and implementation() methods. You can call them outside program using View. 

also it has proxy executable App.Objects.Operations.DefaultExecutorWheel

### Literal flushing

on `force_flush` = 1 "i" will be flushed not using execution interface, passed by other arguments.

on `as_args` = 1, all arguments will be moved to `args` dict of the json

using `App.Objects.Operations.ExecuteById`, you can execute flushed literally executables, with `sift` it will call classes `update()` function

Example: getting RSS channel and updating it (tmp will reset anyway)

```
> python tool.py -view App.Console.InteractiveView
-i Media.RSS.GetFeed -url https://feeds.bbci.co.uk/news/world/rss.xml -force_flush 1 -save_to tmp
-i App.DB.Search -storage tmp
-i App.Objects.Operations.ExecuteById -item {got uuid} -is_update 1
```
