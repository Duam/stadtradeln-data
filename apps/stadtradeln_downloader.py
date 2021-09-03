import click
from stadtradeln_data.status import Status
from stadtradeln_data.cli_utils import download, extract


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
    download_result = download(year_of_stadtradeln_event, path, overwrite)
    if download_result.status != Status.SUCCESS:
        return

    extract_result = extract(year, download_result.filepath)
    if not extract_result.status != Status.SUCCESS:
        return


if __name__ == '__main__':
    download_and_extract()
