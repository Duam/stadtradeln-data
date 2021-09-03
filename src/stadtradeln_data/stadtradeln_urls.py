import pathlib

data_urls = {
    2018: 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/ECF9DF02-37DC-4268-B017-A7C2CF302006/'
          'verkehrsmengen_2018.csv.tar.gz',
    2019: 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/ECF9DF02-37DC-4268-B017-A7C2CF302006/'
          'verkehrsmengen_2019.csv.tar.gz',
    2020: 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/ECF9DF02-37DC-4268-B017-A7C2CF302006/'
          'verkehrsmengen_2020.csv.tar.gz',
}

default_path = pathlib.Path('/tmp/stadtradeln_data/')
