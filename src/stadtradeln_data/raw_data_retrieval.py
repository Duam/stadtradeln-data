import os
import urllib.request
import requests
import urllib.parse
from tqdm import tqdm
import tarfile
from enum import Enum

data_urls = {
    2018: 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/ECF9DF02-37DC-4268-B017-A7C2CF302006/'
          'verkehrsmengen_2018.csv.tar.gz',
    2019: 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/ECF9DF02-37DC-4268-B017-A7C2CF302006/'
          'verkehrsmengen_2019.csv.tar.gz',
    2020: 'https://www.mcloud.de/downloads/ingrid-group_ige-iplug-mcloud/ECF9DF02-37DC-4268-B017-A7C2CF302006/'
          'verkehrsmengen_2020.csv.tar.gz',
}


class Result(Enum):
    UNKNOWN_DATASET = 0
    FILE_ALREADY_EXISTS = 1
    FAILURE = 2
    SUCCESS = 3


def download_dataset(
        year: int,
        destination_path: str = "/tmp/stadtradeln_data/",
        overwrite: bool = False,
        verify_ca_certificate: bool = False,
) -> Result:
    """Downloads a whole (zipped) STADTRADELN dataset from the database of the
    Bundesministerium für Verkehr und digitale Infrastructure (BmVI)
    and stores it locally. Skips download if it already exists locally.
    :param year: The year of the STADTRADELN event.
    :param destination_path: The download destination directory.
    :param overwrite: If set, overwrites the local file.
    :param verify_ca_certificate: Verifies the CA-certificate if True.
        Download may fail if your CA-certificates are not set up properly.
        See https://stackoverflow.com/questions/63210851/python-requests-throwing-sslerror-after-downloading-certificate
    :returns: An enum telling you if the download was successful or not.
    """
    if year not in data_urls.keys():
        return Result.UNKNOWN_DATASET

    url = data_urls[year]
    filename = os.path.basename(urllib.parse.urlparse(url).path)
    filepath = f'{destination_path}/{filename}'

    # Create destination if it doesn't exist
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    # Immediately return if file already exists
    if os.path.isfile(filepath) and not overwrite:
        return Result.FILE_ALREADY_EXISTS

    # Download data
    response = requests.get(url, verify=verify_ca_certificate, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1kB
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', ncols=100, unit_scale=True)
    with open(filepath, "w+b") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    # Check download
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        return Result.FAILURE

    return Result.SUCCESS


def extract_dataset(
        year: int,
        download_path: str = "/tmp/stadtradeln_data/",
        overwrite: bool = False,
) -> Result:
    """Extracts a dataset and stores the resulting .csv file in the
    same directory next to the compressed dataset.
    :year: The dataset's year.
    :download_path: The directory containing the .tar.gz file.
    :overwrite: If True, overwrites any already existing file with the same name.
    :returns: An enum telling you if the extraction was successful or not.
    """
    if year not in data_urls.keys():
        return Result.UNKNOWN_DATASET

    url = data_urls[year]
    filepath = f'{download_path}/{os.path.basename(urllib.parse.urlparse(url).path)}'

    # Immediately return if file already exists
    if os.path.isfile(filepath) and not overwrite:
        return Result.FILE_ALREADY_EXISTS

    with tarfile.open(filepath) as file:
        file.extractall(download_path)

    return Result.SUCCESS
