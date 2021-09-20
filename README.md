# stadtradeln-data

[![pytest](https://github.com/Duam/stadtradeln-data/actions/workflows/pytest.yml/badge.svg?branch=master)](https://github.com/Duam/stadtradeln-data/actions/workflows/pytest.yml)

A Python package to download bicycle traffic count data from the [STADTRADELN](https://www.stadtradeln.de/home) [database](https://www.mcloud.de/web/guest/suche/-/results/detail/ECF9DF02-37DC-4268-B017-A7C2CF302006).

This package installs two things:
- The executable `stadtradeln-data-manager`: A command line interface (cli) for downloading, extracting and clipping STADTRADELN datasets.
- The library `stadtradeln_data_tools`: Methods for importing STADTRADELN datasets to `pandas`

####  Example: `stadtradeln-data-manager`
```bash
$ # Show available commands
$ stadtradeln-data-manager --help

$ # Download and extract 2020's "verkehrsmengen" dataset to /tmp/stadtradeln_data/.
$ # Instead of "verkehrsmengen" you can also choose "geschwindigkeiten".
$ # use `stadtradeln-data-manager download --help` for more options.
$ stadtradeln-data-manager download 2020 verkehrsmengen
$ stadtradeln-data-manager extract 2020 verkehrsmengen

$ # Clip them to the area of Freiburg im Breisgau.
$ # Stores the resulting file in the same directory as the source file.
$ # Here: /tmp/stadtradeln_data/verkehrsmengen_2020_clipped.csv
$ stadtradeln-data-manager clip 2020 verkehrsmengen -latmin 7.616 -latmax 8.112 -lonmin 47.87 -lonmax 48.11
```

#### Example: `stadtradeln_data_tools`
```python
import stadtradeln_data_tools as sdt

# Assumes that you have previously downloaded and extracted a dataset
df = sdt.pandas_importer.load_csv("/tmp/stadtradeln_data/verkehrsmengen_2020_clipped.csv")

# Possibly further clip the data
df = sdt.dataset_clipper.clip_dataset(
    df=df,
    latitude_lim=(7.9, 8.1),
    longitude_lim=(47.9, 48.1)
)

# Continue work with the pandas.DataFrame
print(df)
```


## The repository
#### Installation
```bash
$ git clone git@github.com:Duam/python-stadtradeln-data.git
$ cd python-stadtradeln-data
$ virtualenv venv
$ source venv/bin/activate
$ pip install -e .
$ stadtradeln-data-manager --help
```

#### Folder structure
```
./
 ├ src/
 │ ├ stadtradeln_data_tools/      # The API for processing the datasets
 │ └ stadtradeln_data_manager/    # A command line interface for handling datasets manually
 └ tests/                         # Unit-tests
```


## See also
- [teelram-data](https://github.com/barentsen/telraam-data): A friendly Python package to download traffic count data from Telraam.net. (not by me)
- [MOVEBIS](https://www.bmvi.de/SharedDocs/DE/Artikel/DG/mfund-projekte/verbesserung-der-fahrradinfrastruktur-movebis.html)

## Notes
- This is a third-party package not officially affiliated with the STADTRADELN project.