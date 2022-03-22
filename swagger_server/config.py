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
# elastic_server = Elasticsearch(hosts=[es_url], api_key=(es_api_key["id"], es_api_key["api_key"]))

# ELASTIC_URL="https://9d2d8c7975624d95aa964a1d22a96daf.eu-west-1.aws.found.io"
# ELASTIC_USER="elastic"
# ELASTIC_PASS="fSowAPgpKjaA3hD6T7NxctEf"

# elastic_server = Elasticsearch(
#     hosts=ELASTIC_URL,
#     port=9243,
#     http_auth=(ELASTIC_USER, ELASTIC_PASS),
#     timeout=20
# )

elastic_server = Elasticsearch(
    hosts=["localhost"],
    port=9200,
    timeout=20
)


scroll_timeout = "2m"
