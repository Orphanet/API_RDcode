from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from pathlib import Path
import os

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.varenv')  # load variable environments for elasticsearch config

# ELASTIC SEARCH
# Local test
#elastic_server = Elasticsearch(hosts=["localhost"])

# Local test from docker
# elastic_server = Elasticsearch(hosts=["host.docker.internal"])

# Online
# Check redmine ticket http://redminor.orpha.net/issues/15752
# ES endpoint

ELASTIC_URL = os.getenv('ELASTIC_URL', 'Elastic URL not found.')
ELASTIC_USER = os.getenv('ELASTIC_USER', 'Elastic user not found.')
ELASTIC_PASS =  os.getenv('ELASTIC_PASS', 'Elastic pass not found.')

elastic_server = Elasticsearch(
    hosts=[ELASTIC_URL],
    port=9243,
    http_auth=(ELASTIC_USER, ELASTIC_PASS),
    timeout=20
)
"""
elastic_server = Elasticsearch(
     hosts=["localhost"],
     port=9200,
     timeout=20
)
"""
scroll_timeout = "2m"
