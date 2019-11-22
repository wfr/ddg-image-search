# ddg-image-search
Search and download images on DuckDuckGo.

```
usage: ddg-image-search.py [-h] [--safe-search {off,moderate,strict}]
                                [--type {all,photo,clipart,gif,transparent}]
                                [--size {all,small,medium,large,wallpaper}]
                                [--limit LIMIT] --destdir DESTDIR
                                term
```

The resulting files are saved in the format `00000-URL.EXTENSION`.

Requires:

 * python3-pil
 * python3-requests
