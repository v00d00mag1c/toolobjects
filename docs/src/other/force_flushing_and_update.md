### Force flushing

Even if the object has execute function, it can be flushed via `force_flush`:

```
python tool.py -i Media.Text -value 123 -force_flush 1 -save_to common
```

(`-force_flush.as_args` will save every argument to `args` dict)

Then it can be executed:

```
python tool.py -i App.Objects.Operations.ExecuteById -item [got id] 
```

Additional arguments:

`link` - link items to the object that was executed from db

`is_update` - do "update". It is a pretty obscure mechanism that allows to compare sift values. It uses `update()` function that takes old version of object and got values as arguments.
