import os
import urllib.request
import requests
import urllib.parse
from tqdm import tqdm
from dataclasses import dataclass
from stadtradeln_data.status import Status
from stadtradeln_data.stadtradeln_urls import data_urls


@dataclass
class DownloadResult:
    status: Status
    filepath: str


def download_dataset(
        year: int,
        destination_path: str = "/tmp/stadtradeln_data/",
        overwrite: bool = False,
        verify_ca_certificate: bool = False,
) -> DownloadResult:
    """Downloads a whole (zipped) STADTRADELN dataset from the database of the
    Bundesministerium für Verkehr und digitale Infrastructure (BmVI)
    and stores it locally. Skips download if it already exists locally.
    :param year: The year of the STADTRADELN event.
    :param destination_path: The download destination directory.
    :param overwrite: If set, overwrites the local file.
    :param verify_ca_certificate: Verifies the CA-certificate if True.
        Download may fail if your CA-certificates are not set up properly.
        See https://stackoverflow.com/questions/63210851/python-requests-throwing-sslerror-after-downloading-certificate
    :returns: An enum telling you if the download was successful or not and (if successful) the resulting filepath.
    """
    if year not in data_urls.keys():
        return DownloadResult(Status.UNKNOWN_DATASET, "")

    url = data_urls[year]
    filename = os.path.basename(urllib.parse.urlparse(url).path)
    filepath = f'{destination_path}/{filename}'

    # Create destination if it doesn't exist
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    # Immediately return if file already exists
    if os.path.isfile(filepath) and not overwrite:
        return DownloadResult(Status.FILE_ALREADY_EXISTS, filepath)

    # Download data
    try:
        response = requests.get(url, verify=verify_ca_certificate, stream=True)
    except requests.exceptions.SSLError:
        return DownloadResult(Status.SSL_ERROR, "")

    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 10 * 1024  # 10kB
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', ncols=100, unit_scale=True)
    with open(filepath, "w+b") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()

    # Check download
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        return DownloadResult(Status.FAILURE, "")

    return DownloadResult(Status.SUCCESS, filepath)
