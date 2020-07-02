from elasticsearch import Elasticsearch

# ELASTIC SEARCH
# Local test
#elastic_server = Elasticsearch(hosts=["localhost"])

# Local test from docker
# elastic_server = Elasticsearch(hosts=["host.docker.internal"])

# Online
# Check redmine ticket http://redminor.orpha.net/issues/15752
# ES endpoint
es_url = "https://9d2d8c7975624d95aa964a1d22a96daf.eu-west-1.aws.found.io:9243"
es_api_key = {"id": "8Y5gTXIB0AJkm0jhUTep",
              "name": "rdcodeapi",
              "api_key": "bgP9GTdNQ3C3AkrDUpsNeQ"
              }
elastic_server = Elasticsearch(hosts=[es_url], api_key=(es_api_key["id"], es_api_key["api_key"]))


scroll_timeout = "2m"
