### Usage in ShareX

1. Get token:

```
python tool.py -i App.ACL.Tokens.Get -username root -password root -infinite 1
```

2. Create collection for screenshots:

```
python tool.py -i Media.List.Create -name Screenshots -media_types Media.Images.Image -save_to common
```

3. Open ShareX window
4. Open "Custom uploader settings..."
5. Create new uploader, set destination type to "Image uploader"
6. Set Request URL to "http://127.0.0.1:22222/api/upload/common"
7. URL parameters: set "auth" to what you get in step 1, "return_url" to "1" and "save_name" to "image.jpeg".
8. Set "i_after" to:

```
\{"i": "Media.Get", "object": "Media.Images.Image", "link_to": "[got collection id]"\}
```

8. Set "File form name" to "file", "URL" to "{response}"
