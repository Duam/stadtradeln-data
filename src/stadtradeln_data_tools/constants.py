import pathlib

data_urls = {
    2018: {
        'verkehrsmengen': 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/'
                          'ECF9DF02-37DC-4268-B017-A7C2CF302006/verkehrsmengen_2018.csv.tar.gz',
        'geschwindigkeiten': 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/'
                             '33427A5A-0ADB-40B1-8A1A-390B67B0380B/geschwindigkeiten_2018.csv.tar.gz'
    },
    2019: {
        'verkehrsmengen': 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/'
                          'ECF9DF02-37DC-4268-B017-A7C2CF302006/verkehrsmengen_2019.csv.tar.gz',
        'geschwindigkeiten': 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/'
                             '33427A5A-0ADB-40B1-8A1A-390B67B0380B/geschwindigkeiten_2019.csv.tar.gz'
    },
    2020: {
        'verkehrsmengen': 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/'
                          'ECF9DF02-37DC-4268-B017-A7C2CF302006/verkehrsmengen_2020.csv.tar.gz',
        'geschwindigkeiten': 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/'
                             '33427A5A-0ADB-40B1-8A1A-390B67B0380B/geschwindigkeiten_2020.csv.tar.gz'
    }
}

default_cache_dir = pathlib.Path('/tmp/stadtradeln_data/')
