### Object meta

Object has metainformation that divided to subjective (`local_obj`) and objective (`obj`). They are described [there](../objects/App.Objects.Misc.ObjectMeta.md). There i want to describe thumbnails and sources.

#### Thumbnail

Files are stored locally, but we may need a thumbnail, for example, in video. Currently, thumbnails generated only in [Media.Get] methods.

Thumbnail is another object that wrapped under [Thumbnail](../objects/App.Objects.Misc.Thumbnail.md) object. It has `obj` (the object), `role` (can be "image" or "video") and `is_common`. Thumbnail methods are stored in submodules with role = 'thumbnail'.

Thumbnails are related to object, but, on the other side, they does not adds something, so, for some reason, they are stored in `local_obj`, in `thumbnails` list.

#### Sources

Same as Thumbnail, but describes the source of object. It also can be any object. The common source is defined by `is_common` field.

Example of source:

```
from App.Objects.Misc.Source import Source

...

    item.obj.set_common_source(Source(
        obj = FilePath(
            value = str(...)
        )
    ))
```
