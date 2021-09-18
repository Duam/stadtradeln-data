import numpy as np
import pathlib
from stadtradeln_data_tools.constants import default_cache_dir, data_urls
from stadtradeln_data_tools.status import Status
from stadtradeln_data_tools.dataset_downloader import DownloadResult, download_dataset
from stadtradeln_data_tools.dataset_extractor import ExtractResult, extract_dataset
from stadtradeln_data_tools.dataset_clipper import ClipResult, clip_dataset
from stadtradeln_data_tools.pandas_importer import load_csv, write_csv


def download(
        year: int,
        dataset_type: str,
        download_dir: pathlib.Path = default_cache_dir,
) -> DownloadResult:
    """Downloads a whole (zipped) STADTRADELN dataset from the database of the BmVI and stores it locally.
    :param year: The year of when the dataset was collected
    :param dataset_type: The type of the dataset (e.g. "verkehrsmengen" or "geschwindigkeiten")
    :param download_dir: The directory the dataset should be stored in.
    :returns: An object containing meta-info about the download's result.
    """
    if year not in data_urls.keys():
        return DownloadResult(Status.UNKNOWN_DATASET, "")

    dataset_url = data_urls[year][dataset_type]
    dataset_filename = pathlib.Path(dataset_url).name
    print(f"Downloading {year} dataset to \"{download_dir / dataset_filename}\"")
    retry = True
    verify_ca_certificate = True
    overwrite = False
    while retry:
        download_result = download_dataset(
            dataset_url,
            destination_path=download_dir,
            verify_ca_certificate=verify_ca_certificate,
            overwrite=overwrite
        )
        if download_result.status == Status.UNKNOWN_DATASET:
            print("The dataset you requested does not exist, aborting.")
            return download_result
        elif download_result.status == Status.FILE_ALREADY_EXISTS:
            choice = input("Dataset already exists on your local disc. Download anyway? (Y/n) ")
            overwrite = True
            if choice != "Y" and choice != "y":
                print("Continuing without download.")
                return download_result
        elif download_result.status == Status.FAILURE:
            print(f"Download failed, data in \"{download_result.filepath}\" seems corrupted.")
            return download_result
        elif download_result.status == Status.SSL_ERROR:
            print("WARNING: Your CA-certificates could not be verified by the downloader. "
                  "If you do not trust your network, it is advised that you download the "
                  "files from the original BmVI website: "
                  "https://www.mcloud.de/web/guest/suche/-/results/detail/ECF9DF02-37DC-4268-B017-A7C2CF302006 "
                  f"and manually move them to \"{download_dir}\"")
            choice = input("Retry without certificate verification? (Y/n) ")
            verify_ca_certificate = False
            if choice != "Y" and choice != "y":
                print("Aborting.")
                return download_result
        elif download_result.status == Status.SUCCESS:
            retry = False
        else:
            print("Something unexpectedly went really wrong, sorry. "
                  "Pleas submit an issue with a short description of the steps "
                  "you made before encountering this error:")
            print("https://github.com/Duam/stadtradeln-data/issues/new")
            print("Aborting.")
            return download_result
    print(f"Compressed dataset is located in \"{download_result.filepath}\".")
    return download_result


def extract(
        tar_path: pathlib.Path,
        output_dir: pathlib.Path = None,
) -> ExtractResult:
    """Extracts a .csv.tar.gz dataset.
    :param tar_path: The path of the compressed dataset (.csv.tar.gz)
    :param output_dir: The directory that the file should be extracted to.
    :returns: An object containing meta-info about the extraction result.
    """
    print(f"Extracting dataset in \"{tar_path}\".")
    extract_result = extract_dataset(tar_path, output_dir)
    if extract_result.status == Status.UNKNOWN_DATASET:
        print(f"The compressed dataset was not found in \"{extract_result.filepath}\".")
        return extract_result
    elif extract_result.status == Status.FAILURE:
        print(f"Could not extract the dataset in \"{extract_result.filepath}\".")
        return extract_result
    elif extract_result.status == Status.FILE_ALREADY_EXISTS:
        print("Extracted file already exists, continuing.")
    print(f"Raw data is located in \"{extract_result.filepath}\".")
    return extract_result


def clip(
        filepath: pathlib.Path,
        output_filepath: pathlib.Path = None,
        latitude_min: float = -np.inf,
        latitude_max: float = np.inf,
        longitude_min: float = -np.inf,
        longitude_max: float = np.inf,
) -> ClipResult:
    """Clips a STADTRADELN dataset to a desired geographical region.
    :param filepath: The path to the STADTRADELN dataset in .csv format
    :param output_filepath: The path (directory + filename) of the clipped dataset.
    :param latitude_min: The minimum desired latitude.
    :param latitude_max: The maximum desired latitude.
    :param longitude_min: The minimum longitude.
    :param longitude_max: The maximum longitude.
    :returns: An object containing meta-info about the clipping result.
    """
    print(f"Clipping dataset \"{filepath}\".")
    print("Chosen geographical region:")
    print(f"\t{latitude_min} <= latitude <= {latitude_max}")
    print(f"\t{longitude_min} <= longitude <= {longitude_max}")
    output_filename = pathlib.Path(f"{filepath.with_suffix('').name}_clipped.csv")
    output_filepath = output_filepath if output_filepath is not None else filepath.parent / output_filename

    print("Loading & Clipping dataset. May take a while..")
    df = load_csv(filepath)
    df_clipped = clip_dataset(df, (latitude_min, latitude_max), (longitude_min, longitude_max))

    print(f"Writing clipped dataset to \"{output_filepath}\".")
    # Create output directory if it doesn't exist
    if not output_filepath.parent.is_dir():
        output_filepath.parent.mkdir(parents=True)

    write_csv(df_clipped, output_filepath)
    return ClipResult(Status.SUCCESS, "")
