import logging
from pathlib import Path
from typing import Union

from swagger_server.src import rdcode_download


FORMAT = '%(asctime)-26s %(name)-26s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
name = __name__ if __name__ != '__main__' else 'rdcode_update'
logger = logging.getLogger(name)


def download(outdir: Union[str, Path]) -> None:    
    filename = rdcode_download.download_xml(urls=rdcode_download.URL_PACK_NOMENCLATURE, outdir=outdir)
    rdcode_download.unzip(filename=filename, extract_to=outdir)


