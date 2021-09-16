import pathlib
import click
import numpy as np
from stadtradeln_data_tools.constants import default_cache_dir, data_urls
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
@click.argument("year", type=click.Choice([str(i) for i in data_urls.keys()]))
@click.argument("type", type=click.Choice(['verkehrsmengen', 'geschwindigkeiten'], case_sensitive=False))
@click.option("-d", "--destination-dir", type=click.Path(), default=default_cache_dir,
              help="The directory to store the downloaded STADTRADELN dataset in.")
@click.option("-x", "--extract", is_flag=True, default=False,
              help="Immediately extracts the compressed dataset after the download has finished.")
@click.pass_context
def download(ctx, year, dataset_type, destination_dir, extract):
    """Downloads a dataset.

    The dataset is determined by the year it was collected and by the kind of data you desire.

    By default, the dataset is stored on your local computer in the directory /tmp/stadtradeln_data/.
    """
    year = int(year)
    download_result = download_dataset(year, dataset_type, destination_dir)
    if download_result.status != Status.SUCCESS and download_result.status != Status.FILE_ALREADY_EXISTS:
        return

    if extract:
        extract_result = extract_dataset(year, download_result.filepath.parent, True)
        if not extract_result.status != Status.SUCCESS or not extract_result.status != Status.FILE_ALREADY_EXISTS:
            return

    click.echo("Done.")


@cli.command()
@click.argument("year", type=click.Choice([str(i) for i in data_urls.keys()]))
@click.argument("dataset_type", type=click.Choice(['verkehrsmengen', 'geschwindigkeiten'], case_sensitive=False))
@click.option("-d", "--data-dir", type=click.Path(), default=default_cache_dir,
              help="The directory containing the compressed dataset.")
@click.pass_context
def extract(ctx, year, dataset_type, data_dir):
    """Extracts a dataset to .csv format.
    that has been downloaded previously.
    The extracted dataset will be put in the same directory as the compressed file.
    """
    year = int(year)
    tar_filename = pathlib.Path(data_urls[year][dataset_type]).name
    tar_dir = pathlib.Path(data_dir)
    extract_result = extract_dataset(tar_dir / tar_filename, tar_dir)
    if not extract_result.status != Status.SUCCESS or not extract_result.status != Status.FILE_ALREADY_EXISTS:
        return


@cli.command()
@click.argument("year", type=click.Choice([str(i) for i in data_urls.keys()]))
@click.argument("dataset_type", type=click.Choice(['verkehrsmengen', 'geschwindigkeiten'], case_sensitive=False))
@click.option("-d", "--data-dir", type=click.Path(), default=default_cache_dir,
              help="The directory containing the whole dataset.")
@click.option("-latmin", "--latitude-min", type=float, default=-np.inf, help="Minimum latitude")
@click.option("-latmax", "--latitude-max", type=float, default=np.inf, help="Maximum latitude")
@click.option("-lonmin", "--longitude-min", type=float, default=-np.inf, help="Minimum longitude")
@click.option("-lonmax", "--longitude-max", type=float, default=np.inf, help="Maximum longitude")
@click.pass_context
def clip(ctx, year, dataset_type, data_dir, latitude_min, latitude_max, longitude_min, longitude_max):
    """Clips an extracted dataset to a desired geographical region.
    """
    year = int(year)
    filepath = pathlib.Path(data_urls[year][dataset_type]).with_suffix('').with_suffix('')
    filename = filepath.name
    output_filename = pathlib.Path(f"{filepath.with_suffix('').name}_clipped.csv")
    directory = pathlib.Path(data_dir)
    clip_result = clip_dataset(
        filepath=directory / filename,
        output_filepath=directory / output_filename,
        latitude_min=latitude_min,
        latitude_max=latitude_max,
        longitude_min=longitude_min,
        longitude_max=longitude_max)
    if not clip_result.status != Status.SUCCESS or not clip_result.status != Status.FILE_ALREADY_EXISTS:
        pass

    click.echo("Done.")


if __name__ == '__main__':
    cli()
