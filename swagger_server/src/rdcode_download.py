"""

Module used to download XML orphadata products. 

XML file URLs are retrieved from product-related JSONs 
located in http://www.orphadata.org/cgi-bin/...

"""
import argparse
import logging
from pathlib import Path
from typing import Dict, Union
import requests
import os
import time
import zipfile


FORMAT = '%(asctime)-26s %(name)-26s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
name = __name__ if __name__ != '__main__' else 'rdcode_download'
logger = logging.getLogger(name)

URL_PACK_NOMENCLATURE = "http://www.orphadata.org/data/RD-CODE-FULL/Orphanet_Nomenclature_Pack_EN_FULL.zip"


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
    
    return parser.parse_args()


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
            downloaded_filenames.append(filename)

            logger.info('Writing {} into {}'.format(filename, outdir))
            with open( outdir / filename, 'wb') as _f:
                for chunk in response.iter_content(50*1024*1024):
                    _f.write(chunk)

    if len(downloaded_filenames) == 1:
        return downloaded_filenames[0]

    return downloaded_filenames


def unzip(filename: str, extract_to: str) -> None:
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)


def run():
    args = parse_args()
    outdir = Path(args.outpath)
    
    start_time = time.time()
    filename = download_xml(urls=URL_PACK_NOMENCLATURE, outdir=outdir)
    unzip(filename=filename, extract_to=outdir)
    end_time = time.time()

    logger.info('Download process has finished. Time: {:.2f}'.format(end_time-start_time))


if __name__ == '__main__':
    run()