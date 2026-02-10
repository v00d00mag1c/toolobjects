### Unknown object

On serialization from DB it checks `obj.saved_via.object_name` property to get object's prototype. If error occurs, it returns [UnknownObject](../objects/App.Objects.Misc.UnknownObject.md).

The reason of error can be different. It can be validation error, for example. Or the file with object prototype was moved, but the name in db is the same. It can be fixed with these functionality:

#### Names redirects

You should define `objects.index.redirects` in config that will be a dict. The key is the old name of object, the value is the new. On `ObjectsList.getByName` functions it will return the object from the value.

#### Migrated object

You can define an object on the place of moved that will be extension of [Migrated](../objects/App.Objects.Misc.Migrated.md). It should contain the name of the new object in `migrated_to` field.
