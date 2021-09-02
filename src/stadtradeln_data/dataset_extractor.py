import os
import urllib.request
import urllib.parse
import tarfile
from stadtradeln_data.status import Status
from stadtradeln_data.stadtradeln_urls import data_urls
from dataclasses import dataclass


@dataclass
class ExtractResult:
    status: Status
    filepath: str


def extract_dataset(
        year: int,
        download_path: str = "/tmp/stadtradeln_data/",
        overwrite: bool = False,
) -> ExtractResult:
    """Extracts a dataset and stores the resulting .csv file in the
    same directory next to the compressed dataset.
    :year: The dataset's year.
    :download_path: The directory containing the .tar.gz file.
    :overwrite: If True, overwrites any already existing file with the same name.
    :returns: An enum telling you if the extraction was successful or not.
    """
    if year not in data_urls.keys():
        return ExtractResult(Status.UNKNOWN_DATASET, "")

    url = data_urls[year]
    filepath = f'{download_path}/{os.path.basename(urllib.parse.urlparse(url).path)}'

    # Immediately return if file already exists
    if os.path.isfile(filepath) and not overwrite:
        return ExtractResult(Status.FILE_ALREADY_EXISTS, filepath)

    with tarfile.open(filepath) as file:
        file.extractall(download_path)

    return ExtractResult(Status.SUCCESS, filepath)
