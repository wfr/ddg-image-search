# ddg-image-search
Search and download images on DuckDuckGo.

```
usage: ddg-image-search.py [-h] [--safe-search {off,moderate,strict}]
                           [--type {all,photo,clipart,gif,transparent}]
                           [--size {all,small,medium,large,wallpaper}]
                           [--limit LIMIT] -d DESTDIR
                           term

Search for images on DuckDuckGo.

positional arguments:
  term                  search term

options:
  -h, --help            show this help message and exit
  --safe-search {off,moderate,strict}
  --type {all,photo,clipart,gif,transparent}
  --size {all,small,medium,large,wallpaper}
  --limit LIMIT         download at most N images (default 50)
  -d DESTDIR, --destdir DESTDIR
```

The resulting files are saved in the format `00000-URL.EXTENSION`.

Requires:

 * python3-pil
 * python3-requests
