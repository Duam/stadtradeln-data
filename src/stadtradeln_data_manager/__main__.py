import click
import numpy as np
from stadtradeln_data_tools.constants import default_cache_path
from stadtradeln_data_tools.status import Status
from stadtradeln_data_manager.cli_utils import (
    download as download_dataset,
    extract as extract_dataset,
    clip as clip_dataset
)


@click.group()
def cli():
    pass


@cli.command()
@click.argument("year_of_stadtradeln_event", type=int)
@click.option("-p", "--path", type=click.Path(), default=default_cache_path,
              help="The directory to store the downloaded STADTRADELN dataset in.")
@click.option("-o", "--overwrite", is_flag=True, default=False,
              help="Overwrite the locally stored file. Useful if the file was corrupted for some reason during "
                   "a previous download.")
@click.option("-x", "--extract", is_flag=True, default=False,
              help="Immediately extracts the compressed dataset after the download has finished.")
@click.pass_context
def download(ctx, year_of_stadtradeln_event, path, overwrite, extract):
    """Downloads and extracts a specified STADTRADELN dataset. The dataset
    is determined using the year it was collected. By default, the dataset
    is stored on your local computer in the directory /tmp/stadtradeln_data_tools/.
    """
    year = year_of_stadtradeln_event
    download_result = download_dataset(year_of_stadtradeln_event, path, overwrite)
    if download_result.status != Status.SUCCESS and download_result.status != Status.FILE_ALREADY_EXISTS:
        return

    if extract:
        extract_result = extract_dataset(year, download_result.filepath.parent, overwrite)
        if not extract_result.status != Status.SUCCESS or not extract_result.status != Status.FILE_ALREADY_EXISTS:
            return

    click.echo("Done.")


@cli.command()
@click.argument("year_of_stadtradeln_event", type=int)
@click.option("-p", "--path", type=click.Path(), default=default_cache_path,
              help="The directory to containing the compressed STADTRADELN dataset.")
@click.option("-o", "--overwrite", is_flag=True, default=False,
              help="Overwrite the locally stored file. Useful if the file was corrupted for some reason during "
                   "a previous extraction.")
@click.pass_context
def extract(ctx, year_of_stadtradeln_event, path, overwrite):
    """Extracts a specified STADTRADELN dataset that has been downloaded previously.
    The extracted dataset will be put in the same directory as the compressed file.
    """
    year = year_of_stadtradeln_event
    extract_result = extract_dataset(year, path, overwrite)
    if not extract_result.status != Status.SUCCESS or not extract_result.status != Status.FILE_ALREADY_EXISTS:
        return


@cli.command()
@click.argument("year_of_stadtradeln_event", type=int)
@click.option("-p", "--path", type=click.Path(), default=default_cache_path,
              help="The directory to store the downloaded STADTRADELN dataset in.")
@click.option("-o", "--overwrite", is_flag=True, default=False,
              help="Overwrite the locally stored file. Useful if the file was corrupted for some reason during "
                   "a previous clipping.")
@click.option("--latitude-min", type=float, default=-np.inf, help="Minimum latitude")
@click.option("--latitude-max", type=float, default=np.inf, help="Maximum latitude")
@click.option("--longitude-min", type=float, default=-np.inf, help="Minimum longitude")
@click.option("--longitude-max", type=float, default=np.inf, help="Maximum longitude")
@click.pass_context
def clip(ctx, year_of_stadtradeln_event, path, overwrite, latitude_min, latitude_max, longitude_min, longitude_max):
    """Clips a specified STADTRADELN dataset to a desired geographic region.
    The clipped dataset file will be put in the same directory as the raw dataset file.
    """
    print(f"{year_of_stadtradeln_event}, {path}, {overwrite}, {latitude_min}, {latitude_max}, {longitude_min}, "
          f"{longitude_max}")
    clip_result = clip_dataset(
        year=year_of_stadtradeln_event,
        path=path,
        output_path=None,
        overwrite=overwrite,
        latitude_min=latitude_min,
        latitude_max=latitude_max,
        longitude_min=longitude_min,
        longitude_max=longitude_max)
    if not clip_result.status != Status.SUCCESS or not clip_result.status != Status.FILE_ALREADY_EXISTS:
        pass


if __name__ == '__main__':
    cli()
