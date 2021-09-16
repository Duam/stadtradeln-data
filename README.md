# stadtradeln-data
A Python package to download bicycle traffic count data from the [STADTRADELN](https://www.stadtradeln.de/home) [database](https://www.mcloud.de/web/guest/suche/-/results/detail/ECF9DF02-37DC-4268-B017-A7C2CF302006).

#### Folder structure
```
./
 ├ src/
 │ ├ stadtradeln_data_tools/      # The API for processing the datasets
 │ └ stadtradeln_data_manager/    # A command line interface for handling datasets manually
 └ tests/                         # Unit-tests
```

#### Usage
```bash
$ git clone git@github.com:Duam/python-stadtradeln-data.git
$ cd python-stadtradeln-data
$ virtualenv venv
$ source venv/bin/activate
$ pip install -e .
$ stadtradeln-data-manager --help
```

Example: Download the "verkehrsmengen" dataset of 2020 and clip them to the area of Freiburg im Breisgau.
```
$ stadtradeln-data-manager download 2020 verkehrsmengen
$ stadtradeln-data-manager extract 2020 verkehrsmengen
$ stadtradeln-data-manager clip 2020 verkehrsmengen -latmin 7.616 -latmax 8.112 -lonmin 47.87 -lonmax 48.11
```

## See also
- [teelram-data](https://github.com/barentsen/telraam-data): A friendly Python package to download traffic count data from Telraam.net. (not by me)
- [MOVEBIS](https://www.bmvi.de/SharedDocs/DE/Artikel/DG/mfund-projekte/verbesserung-der-fahrradinfrastruktur-movebis.html)

## Notes
- This is a third-party package not officially affiliated with the STADTRADELN project.