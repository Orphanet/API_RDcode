import argparse
import json
import logging
from pathlib import Path
from typing import Dict, List, Union
import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

from swagger_server.lib.elastic_ingest import EsBulkInjector

BASE_PATH = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_PATH / '.varenv')


FORMAT = '%(asctime)-26s %(name)-26ls %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
name = __name__ if __name__ != '__main__' else 'rdcode_injection'
logger = logging.getLogger(name)
# logging.getLogger("elasticsearch").setLevel(logging.WARNING)


def esConnector(url: str):
    """
    Parameters
    ----------
    url : str
        Keyword to indicate which ES instance to connect to.

        Value can be:

         - 'local': the url will be http://127.0.0.1:9200
         - 'remote' the connection parameters will taken from environment variables (port: 9243 by default)

    Returns
    -------
    Elasticsearch client instance
    """
    if url == 'local':
        es_client =  Elasticsearch(
            'http://127.0.0.1:9200',
            timeout=60,
            max_retries=3,
            retry_on_timeout=True
        )
    else:
        url = os.getenv('ELASTIC_URL', None)
        user = os.getenv('ELASTIC_USER', None)
        password = os.getenv('ELASTIC_PASS', None)

        if url and user and password:
            es_client = Elasticsearch(
                [url],
                port=9243,
                http_auth=(user, password),
                timeout=60, max_retries=3, retry_on_timeout=True
            )
        else:
            logger.error('Error: no profile configurations have been found to connect to the remote elasticsearch instance.')
            logger.error('Please ensure that a .varenv file configurations is defined in in the root of the RD-code project directory.')
            logger.error("The 3 following environment variables must exist to connect to the remote Elasticsearch instance:")
            logger.error(" - ELASTIC_URL")
            logger.error(" - ELASTIC_USER")
            logger.error(" - ELASTIC_PASS")
            exit()

    if es_client:
        logger.info('Successfully connected to ES instance: {}'.format(es_client))
        return es_client

def get_jsons(path: Union[str, Path], pattern: str=None) -> Union[Path, List]:
    """[summary]

    Parameters
    ----------
    path : Union[str, Path]
        Path to directory containing ES ready-to-inject JSON files

    Returns
    -------
    List
        List of Path instances of ES ready-to-inject JSON files 
    """
    match = '{}'.format(pattern) if pattern else '*.json'

    if isinstance(path, str):
        path = Path(path)

    if path.is_dir():
        return [x for x in path.glob(match)]
    
    if path.is_file() and path.exists():
        return path


def generate_actions(filename: str):
    with open(filename, 'r') as _file:
        for line in _file:
            if '{"index":' not in line:
                _line = json.loads(line)
                yield _line


def bulk_inject(es_client: Elasticsearch, json_filename: Union[str, Path], index: str=None, max_chunk_bytes: int=100):
    logger.info('Creating index {} and injecting documents from {}'.format(index, json_filename))

    if not isinstance(json_filename, Path):
        json_filename = Path(json_filename)

    bulk_injector = EsBulkInjector(
        es_client=es_client,
        index=index,
        doc_generator=generate_actions(filename=json_filename),
        mappings=None,
        max_chunk_bytes=max_chunk_bytes
    )
    bulk_injector.run()


def main(es_client: Elasticsearch, json_path: Union[str, Path, List], index_prefix: str=None):    
    if not isinstance(json_path, List):
        json_path = [json_path]

    for json_filename in json_path:
        _index = json_filename.stem if not index_prefix else '{}_{}'.format(index_prefix, json_filename.stem)
        bulk_inject(es_client=es_client, json_filename=json_filename, index=_index)


def check_user_choice(url_type: str) -> None:
    user_choice = ''
    if url_type == "remote":
        print(
            """
You are going to ingest new data to your remote elasticsearch instance. Please note that
all indices you want to ingest and that already exists in the instance will be first deleted.
            """
        )            

        while user_choice.lower() not in ["yes", "y", "no", "n"]:
            user_choice = input("Type (Y)es if you want to continue, (N)o otherwise: ")

        if user_choice.lower() in  ["no", "n"]:
            exit()                


def parse_args():
    parser = argparse.ArgumentParser(description='Bulk inject RD-code data in Elasticsearh')
    parser.add_argument(
        "-p",
        "--path",
        required=True,
        nargs="?",
        type=str,
        help="Path or filename of JSON file(s)"
    )
    parser.add_argument(
        "-m",
        "--match",
        required=False,
        nargs="?",
        type=str,
        default="",
        help="String used to filter JSON filenames given in -path. Only JSON files matching that string will be processed (example: *classif*)"
    )
    parser.add_argument(
        "-i",
        "--index_prefix",
        required=False,
        nargs="?",
        type=str,
        default=None,
        help="Prefix to add to the filename stem to create Elasticsearch index name (default: None - index are named based on JSON filename)."
    )
    parser.add_argument(
        "-u",
        "--url",
        required=False,
        nargs="?",
        choices=("local", 'remote'),
        type=str,
        default="local",
        help="ES URL type: either 'local' or 'remote' (default: local)."
    )
    parser.add_argument(
        '--print',
        action='store_true',
        help='Print path of JSON files that will be processed')
    
    return parser.parse_args()



def run():
    args = parse_args()

    path = args.path
    pattern = args.match
    url_type = args.url
    index_prefix = args.index_prefix

    start_time = time.time()

    json_filenames = get_jsons(path=path, pattern=pattern)
    if args.print:
        for _file in json_filenames:
            logger.info(' - ' + str(_file))
    else:
        check_user_choice(url_type=url_type)
        es_client = esConnector(url=url_type)
        main(es_client=es_client, json_path=json_filenames, index_prefix=index_prefix)

    end_time = time.time()
    
    logger.info('Injection process has finished. Time: {:.2f}'.format(end_time-start_time))


if __name__ == '__main__':
    run()