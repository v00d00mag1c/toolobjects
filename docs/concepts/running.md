every executable has execute() and implementation() methods. You can call them outside program using View. 

also it has proxy executable App.Objects.Operations.DefaultExecutorWheel

### Literal flushing

on `force_flush` = 1 "i" will be flushed not using execution interface, passed by other arguments.

usage example:

1. getting rss channel and updating it

```
-i Data.RSS.GetFeed -url https://feeds.bbci.co.uk/news/world/rss.xml -force_flush 1 -save_to tmp
-i App.Storage.DB.Search -storage tmp
-i App.Objects.Operations.ExecuteById -item {got uuid} -sift 1
```
