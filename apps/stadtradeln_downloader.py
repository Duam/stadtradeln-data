from stadtradeln_data.download import Result, download_dataset, extract_dataset

print("Trying to download file")
result = download_dataset(2018)
if result == Result.UNKNOWN_DATASET:
    print("The dataset you requested does not exist")
    quit(0)
elif result == Result.FILE_ALREADY_EXISTS:
    print("File already exists")
elif result == Result.DOWNLOAD_FAILED:
    print("Download failed")
    quit(0)
else:
    print("Download succeeded")

print("Extracting dataset")
extract_dataset(2018)
print("Extraction done.")

"""
# TODO:
Create a command-line interface.

There seem to be problems with downloading the STADTRADELN datasets
if the CA-certificates are not properly configured on the user system.
It is always possible to ignore the verification process (by passing
the verify_ca_certificates=False parameter), but some users might
mistrust this script.

Give the user the option to
A) ignore verification (potentially unsafe)
B) Throw a warning in the cli, like:
"
Your CA-certificates could not be verified by the downloader.
If you do not trust this script, it is adviced that you download the
files from the original BmVI website:
https://www.mcloud.de/web/guest/suche/-/results/detail/ECF9DF02-37DC-4268-B017-A7C2CF302006
and move them to /tmp/stadtradeln_data/
"
"""