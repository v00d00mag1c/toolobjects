Object system

Every entity in the app is an Object. More correct, every py-file (except boot) is counts as object. Basically you can imagine every kind of data (that is like json) like an Object. 

Object is builded with mixins that adds functionality to it:

**Configurable**

Allows to set settinga of the object that will be applied to the whole app

**BaseModel**

Pydantic's BaseModel with some functions and hacks

**Linkable**

Allows to create links between items
