"""

Module used to download XML orphadata products. 

XML file URLs are retrieved from product-related JSONs 
located in http://www.orphadata.org/cgi-bin/...

"""
import argparse
import logging
from pathlib import Path
import shutil
from typing import Dict, Union
import requests
import os
import time
import zipfile
from shutil import unpack_archive


FORMAT = '%(asctime)-26s %(name)-26s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
name = __name__ if __name__ != '__main__' else 'rdcode_download'
logger = logging.getLogger(name)

ISO_LANG = ["cs", "de", "en", "es", "fr", "it", "nl", "pl", "pt"]
PACK_BASENAME = "http://www.orphadata.org/data/RD-CODE-FULL/Orphanet_Nomenclature_Pack_{}.tar.gz"

URL_PACK_NOMENCLATURE = [ PACK_BASENAME.format(_) for _ in ISO_LANG ]


def parse_args():
    parser = argparse.ArgumentParser(description='Bulk inject RD-code data in Elasticsearh')
    parser.add_argument(
        "-o",
        "--outpath",
        required=True,
        nargs="?",
        type=str,
        help="Path or directory name where the Nomenclature pack will be downloaded."
    )
    parser.add_argument(
        "-xml",
        required=False,
        nargs="?",
        type=str,
        default="xml_data",
        help="Output directory where all XML files will be moved to after download. Default: 'xml_data'."
    )
    return parser.parse_args()


def write_response(response: requests.Response, outpath: Union[str, Path]):
    logger.info('Writing response: {} '.format(outpath))
    with open(outpath, 'wb') as _f:
        for chunk in response.iter_content(50*1024*1024):
            _f.write(chunk)


def download_xml(urls: Union[str, Path, list], outdir: Union[str, Path]) -> Union[str, Path, list]:
    """Download orphadata XML product

    Parameters
    ----------
    urls : Union[str, Path, List]
        URL(s) linking the XML product
    outdir : Union[str, Path], optional
        Path to download XML files to, by default OUTPATH
    """
    logger.info('Downloading XML files...')

    downloaded_filenames = []

    os.makedirs(outdir, exist_ok=True)

    if not isinstance(urls, list):
        urls = [urls]
    
    for url in urls:
        if not isinstance(url, Path):
            filename = Path(url).name
        else:
            filename = url.name

        logger.info('GET request to {}'.format(url))
        with requests.get(url=str(url)) as response:
            response.raise_for_status()
            downloaded_filenames.append(outdir/filename)
            write_response(response=response, outpath=outdir/filename)            

    if len(downloaded_filenames) == 1:
        return downloaded_filenames[0]

    return downloaded_filenames


def unzip(filename: str, extract_to: str) -> None:
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def extract_all(filename: Union[str, Path, list], extract_path: str):
    if not isinstance(filename, list):
        filename = [filename]

    for _filename in filename:
        if not isinstance(_filename, Path):
            _filename = Path(_filename)

        if _filename.exists():
            unpack_archive(_filename, extract_path)


def move_files_to(rootpath, destination):
    os.makedirs(destination, exist_ok=True)
    destination = Path(destination)

    for root, dirs, files in os.walk(rootpath, topdown=False):
        for name in files:
            filename = Path(root) / name
            if filename.suffix == ".xml":
                logger.info("Moving {} to {}".format(filename, destination))
                shutil.move(src=filename, dst=destination / filename.name)


def run():
    args = parse_args()
    outdir = Path(args.outpath)
    xml_path = outdir / Path(args.xml)

    
    start_time = time.time()

    # download nomenclature packs from chouette and stores their path
    # filenames = download_xml(urls=URL_PACK_NOMENCLATURE, outdir=outdir)

    # unarchive all downloaded archives
    # extract_all(filename=filenames, extract_path=outdir)

    # move all xml files from all nomenclature pack into a single path: xml_data (default)
    move_files_to(rootpath=outdir, destination=xml_path)

    end_time = time.time()

    logger.info('Download process has finished. Time: {:.2f}'.format(end_time-start_time))


if __name__ == '__main__':
    run()