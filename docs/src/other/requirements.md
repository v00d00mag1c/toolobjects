### Requirements

Every Object can have [Requirements](../objects/App.Objects.Requirements.Requirement.md) that define dependencies from `pip` that required to correct script work.

The requirement of one module can be installed via:

```
python tool.py -i App.Objects.Requirements.InstallFromObject -object [name of the object]
```

Requirements of each known object can be installed via (that must be did after installation):

```
python tool.py -i App.Objects.Requirements.InstallEvery
```
