import tarfile
import pathlib
from stadtradeln_data_tools.status import Status
from dataclasses import dataclass


@dataclass
class ExtractResult:
    status: Status
    filepath: str


def extract_dataset(
        tar_path: pathlib.Path,
        output_dir: pathlib.Path = None,
) -> ExtractResult:
    """Extracts a .csv.tar.gz dataset.
    :tar_path: The path of the compressed dataset (.tar.gz).
    :output_dir: The directory that the files should be extracted to.
    :returns: An enum telling you if the extraction was successful or not.
    """
    filepath = tar_path.with_suffix('').with_suffix('')
    output_dir = output_dir if output_dir is not None else tar_path.parent
    output_filepath = output_dir / filepath.name

    if not tar_path.exists():
        return ExtractResult(Status.UNKNOWN_DATASET, tar_path)

    if not tarfile.is_tarfile(tar_path):
        return ExtractResult(Status.FAILURE, tar_path)

    if output_filepath.is_file():
        return ExtractResult(Status.FILE_ALREADY_EXISTS, output_filepath)

    with tarfile.open(tar_path) as file:
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(file, output_dir)

    return ExtractResult(Status.SUCCESS, output_filepath)
