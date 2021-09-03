import pandas as pd
from typing import Tuple


def clip_to_rectangle(
        df: pd.DataFrame,
        latitude_lim: Tuple[float, float],
        longitude_lim: Tuple[float, float],
) -> pd.DataFrame:
    """
    :param df:
    :param latitude_lim:
    :param longitude_lim:
    :returns:
    """
    raise NotImplementedError


"""
in_filenames = [
    'verkehrsmengen_2018',
    'verkehrsmengen_2019',
    'verkehrsmengen_2020',
]

x_min = 7.616
x_max = 8.112
y_min = 47.87
y_max = 48.11

for filename in in_filenames:
    out_data = []

    with open(f'stadtradeln_datasets_raw\\{filename}.csv') as in_csv_file:
        with open(f'stadtradeln_datasets_raw\\{filename}_reduced.csv', 'w') as out_csv_file:

            reader = csv.reader(in_csv_file, delimiter=',')
            writer = csv.writer(out_csv_file)

            for row in reader:
                if row[0] == 'edge_geo':
                    writer.writerow(row)
                    continue

                geo_data = row[0]
                geo_data = geo_data.replace("LINESTRING(", "")
                geo_data = geo_data.replace(")", "")
                start_end = geo_data.split(',')
                start_latlon = start_end[0].split(" ")
                occurances = row[1]

                x = float(start_latlon[0])
                y = float(start_latlon[1])
                if x_min < x and x < x_max:
                    if y_min < y and y < y_max:
                        writer.writerow(row)
"""