### Running

```
cd {src folder}

.\venv.ps1 - load and enter venv

.\update.ps1 - update dependencies
```

now you can call:

```
python tool.py -i {object name}
```

change View:

```
python tool.py -view {view name}
```

change preexecutor:

```
python tool.py -pre_i {wheel name}
```

Initialization is takes too long (~ 6 seconds), so if you dont want to exit:

```
python tool.py -view App.Console.InteractiveView
```

Override config values:

```
python tool.py --c.logger.print.exclude "{}"
```
