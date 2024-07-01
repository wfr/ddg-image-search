# ddg-image-search
Search and download images on DuckDuckGo.

### Usage
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

### Requirements

 * urllib3>=2.0
 * Pillow
 * requests

The script is currently broken with urllib3 < 2.0. I'm not sure why and don't
have time to investigate.

This works on Debian stable:
```
python3 -m venv venv/
source venv/bin/activate
python3 -m pip install -r requirements.txt
./ddg-image-search.py ...
```

On Debian testing and later, the system packages are sufficient:
```
apt-get install python3-pil python3-requests
```
