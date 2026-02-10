Every thing in this app is an Object: it contain fields, functions etc. Object is consists of:

BaseModel

Pydantic model with class names functions

There is Objects with entry point - Executables. They can create other objects from data they receive.

Client needs to know the list of objects in the app, so we collecting it in ObjectsList.

We need to know what arguments we should pass to Executable, so defining it at ArgumentsDict with Argument class.

We need to log messages at runtime, so we using Logger.

We need to store settings of something, so we using Config or Env.

Objects can be linked to each other, also you can replace an object field by LinkInsertion.

We need to save and load objects from persistent storage, so we have Storage and DBAdapter.

Object can use files, so we using StorageUnit to represent them.

### App

App is a singletone that creates at the boot (tool.py). The app wrapper is View that is an executable. For example "Console" view that gets executable name in "i" param and runs it.
