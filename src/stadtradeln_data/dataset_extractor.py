import tarfile
import pathlib
from stadtradeln_data.constants import default_cache_path
from stadtradeln_data.status import Status
from stadtradeln_data.constants import data_urls
from dataclasses import dataclass


@dataclass
class ExtractResult:
    status: Status
    filepath: str


def extract_dataset(
        year: int,
        download_path: str = default_cache_path,
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

    filename_csvtargz = pathlib.Path(data_urls[year]).name
    filepath_csvtargz = pathlib.Path(download_path, filename_csvtargz)
    filepath_csv = filepath_csvtargz.with_suffix('').with_suffix('')

    # Immediately return if file already exists
    if filepath_csv.is_file() and not overwrite:
        return ExtractResult(Status.FILE_ALREADY_EXISTS, filepath_csv)

    # Extract file
    with tarfile.open(filepath_csvtargz) as file:
        file.extractall(download_path)

    return ExtractResult(Status.SUCCESS, filepath_csv)
