# duckduckgo-image-search
A little script that searches for images on DuckDuckGo and downloads them.

```
usage: duckduckgo-image-search.py [-h] [--safe-search {off,moderate,strict}]
                                  [--type {all,photo,clipart,gif,transparent}]
                                  [--size {all,small,medium,large,wallpaper}]
                                  [--limit LIMIT] --destdir DESTDIR
                                  term
```

The resulting files are saved in the format `00000-URL.EXTENSION`.
