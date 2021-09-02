# stadtradeln-data
A Python package to download bicycle traffic count data from the [STADTRADELN](https://www.stadtradeln.de/home) [database](https://www.mcloud.de/web/guest/suche/-/results/detail/ECF9DF02-37DC-4268-B017-A7C2CF302006).

#### Folder structure
```
./
 ├ apps/                          # Executable files
 ├ src/
 │ └ stadtradeln_data/            # Source code, library 
 └ tests/                         # Unit-tests
```

#### Usage
```bash
$ git clone git@github.com:Duam/python-stadtradeln-data.git
$ cd python-stadtradeln-data
$ virtualenv venv
$ source venv/bin/activate
$ pip install -e .
$ echo "Enjoy!"
```

(a more elaborate usage section will come as soon as this repository has more functionality)

## See also
- [teelram-data](https://github.com/barentsen/telraam-data): A friendly Python package to download traffic count data from Telraam.net. (not by me)

## Notes
- This is a third-party package not officially affiliated with the STADTRADELN project.