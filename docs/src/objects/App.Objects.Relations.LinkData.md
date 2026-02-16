### App.Objects.Relations.LinkData

Data about link. Currently, there is only `role`, but it was moved to a separate class for extensibility.

#### Fields

|Field|Type|Description|
|--|--|--|
|role|`list[str]`|Description of the relation|

**Roles table**

|Role|Description|
|--|--|
|object|Link is related to the data of this object (or used in [LinkInsertion](./App.Objects.Relations.LinkInsertion.md))|
|common|Link was created by script|
|thumbnail|Link's object is a thumbnail of this object|
|revision|Link's object is a new version of this object|
|list_item|Link's object is an item of collection (that is this object)|
|horizontal|Link's object does not belongs to the current object|
|external|Link is not related to this object|
