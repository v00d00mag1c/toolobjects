### Media.Images.Download

Type: `Extractor`

Downloads image from `url`, saves it as `StorageUnit` and `Files.FileTypes.Image`.

#### Arguments

##### url

`type`: `Data.String`

`assertions`: NotNone

URL to download

##### gallery

`type`: `Media.Images.Gallery`

can be received by uuid

Gallery to link. If passed, links the downloaded Image to it.

##### filename

`type`: `Data.String`

`default`: `image.png`

Name that will be assigned to file in StorageUnit dir. If None, tries to get name from URL.

##### Download

`type`: `Data.Boolean`

`default`: True

Whether to download the file. If False, it will be available from source
