import click
from stadtradeln_data.status import Status
from stadtradeln_data.dataset_downloader import download_dataset
from stadtradeln_data.dataset_extractor import extract_dataset


@click.command()
@click.argument("year_of_stadtradeln_event", type=int)
@click.option("-p", "--path", type=click.Path(), default="/tmp/stadtradeln_data/",
              help="The directory to store the STADTRADELN dataset in.")
@click.option("-o", "--overwrite", is_flag=True, default=False,
              help="Overwrite the locally stored file. Useful if the file was corrupted for some reason.")
@click.pass_context
def download_and_extract(ctx, year_of_stadtradeln_event, path, overwrite):
    """Downloads and extracts a specified STADTRADELN dataset. The dataset
    is determined using the year it was collected. By default, the dataset
    is stored on your local computer in the directory /tmp/stadtradeln_data/.
    """
    year = year_of_stadtradeln_event
    print(f"Downloading {year} dataset to path \"{path}\"")
    retry = True
    verify_ca_certificate = True
    while retry:
        download_result = download_dataset(
            year,
            destination_path=path,
            verify_ca_certificate=verify_ca_certificate,
            overwrite=overwrite
        )
        if download_result.status == Status.UNKNOWN_DATASET:
            print("The dataset you requested does not exist, aborting.")
            return
        elif download_result.status == Status.FILE_ALREADY_EXISTS:
            print(f"File already exists, continuing.")
            retry = False
        elif download_result.status == Status.FAILURE:
            print(f"Download failed, data in \"{download_result.filepath}\" seems corrupted.")
            return
        elif download_result.status == Status.SSL_ERROR:
            print("WARNING: Your CA-certificates could not be verified by the downloader. "
                  "If you do not trust your network, it is advised that you download the "
                  "files from the original BmVI website: "
                  "https://www.mcloud.de/web/guest/suche/-/results/detail/ECF9DF02-37DC-4268-B017-A7C2CF302006 "
                  f"and manually move them to \"{path}\"")
            choice = input("Retry without certificate verification (Y/n)? ")
            verify_ca_certificate = False
            if choice != "Y" and choice != "y":
                print("Aborting.")
                return
        elif download_result.status == Status.SUCCESS:
            retry = False
        else:
            # TODO: Prompt the user to write an issue
            print("Something unexpectedly went really wrong, sorry.")
            return
    print(f"Dataset is located in \"{download_result.filepath}\".")

    # TODO: filepath has a double backslash in it
    # like this: /tmp/stadtradeln_data//verkehrsmengen_2019.csv.tar.gz
    print(f"Extracting {year} dataset in \"{download_result.filepath}\".")
    extract_result = extract_dataset(year)
    if extract_result.status == Status.UNKNOWN_DATASET:
        print(f"The compressed dataset was not found in path \"{extract_result.filepath}\".")
    elif extract_result.status == Status.FAILURE:
        print("Could not extract the dataset (unknown reason).")
    print(f"Extraction succeeded. Raw data is located in \"{extract_result.filepath}\".")


if __name__ == '__main__':
    download_and_extract()
