import requests
import pathlib
from tqdm import tqdm
from dataclasses import dataclass
from stadtradeln_data_tools.status import Status
from stadtradeln_data_tools.constants import default_cache_dir


@dataclass
class DownloadResult:
    status: Status
    filepath: str


def download_dataset(
        url: str,
        destination_path: str = default_cache_dir,
        overwrite: bool = False,
        verify_ca_certificate: bool = False,
) -> DownloadResult:
    """Downloads a whole (zipped) STADTRADELN dataset from the database of the
    Bundesministerium für Verkehr und digitale Infrastructure (BmVI)
    and stores it locally. Skips download if it already exists locally.
    :param url: The URL pointing to the desired dataset.
    :param destination_path: The download destination directory.
    :param overwrite: If set, overwrites the local file.
    :param verify_ca_certificate: Verifies the CA-certificate if True.
        Download may fail if your CA-certificates are not set up properly.
        See https://stackoverflow.com/questions/63210851/python-requests-throwing-sslerror-after-downloading-certificate
    :returns: An enum telling you if the download was successful or not and (if successful) the resulting filepath.
    """
    destination_path = pathlib.Path(destination_path)
    filename = pathlib.Path(url).name
    filepath = pathlib.Path(destination_path, filename)

    # Create destination if it doesn't exist
    if not destination_path.is_dir():
        destination_path.mkdir(parents=True)

    # Immediately return if file already exists
    if filepath.is_file() and not overwrite:
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
