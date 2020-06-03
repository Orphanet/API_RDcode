# API_RDcode

Ver: june 2020

Author: Cyril Bigot

# Technical documentation

## Software Version

The API description is written according to OpenAPI v3 standards.

The server stub has been auto-generated from the description
 with swagger-codegen version 3.0.20 in Python3-flask.

Developed with Elasticsearch 7.X.

Other modules requirement are referenced in 
python-flask-server.requirements.txt:
    
    swagger-ui-bundle == 0.0.6
    connexion == 2.6.0
    elasticsearch == 7.6
    python_dateutil == 2.6.0
    setuptools >= 21.0.0
    Flask-Testing >= 0.8.0

## Server setup

Create a server stub with the OpenAPI v3 description 
([swagger_v3_Rdcode](backup_manual_code/BU_RDcode-2-oas3-swagger.yaml))
with Python3-flask.

Two possibilities:
* Use the [online swagger-codegen](https://editor.swagger.io/)
(frequent new releases and features, potentially unstable)
* Use the [swagger-codegen-cli.jar](./tools/swagger-codegen-cli.jar)
from this distribution and follow the 
[swagger codegen instructions](./tools/swagger%20codegen%20instructions.txt)

/!\ One copy of OpenAPI definition MUST be kept separated from the one included
 in the RDcode_API_server because the codegen dereference everything /!\

/!\ Backup the full RDcode_API_server folder to 
[backup_manual_code](./backup_manual_code) /!\

One convenient way to deploy a new stub is to create a new branch to do 
a MANUAL merge with pycharm "VCS/Git/compare with branch"

The required packages can be installed by launching the following command
in the operating system's console (preferentially virtual environment console)
from the server's root [RDcode_API_server/swagger_server](swagger_server)
    
    pip3 install -r requirements.txt

Note that 'test-requirements.txt' is auto generated and has not been used

## Deployment

#### Host
Gandi.net

SFTP:

    3723642@sftp.sd3.gpaas.net
pwd:

    5d...C6

host selected built-in:

    Python 3.8
    MySQL 8.0
#### host documentation:
https://docs.gandi.net/fr/simple_hosting/connexion/git.html

To upload and deploy from the local build folder:

    git remote add gandi git+ssh://3723642@git.sd3.gpaas.net/default.git
    git push gandi master
    
    # for deploying master branch
    ssh 3723642@git.sd3.gpaas.net deploy default.git    
    # OR append local branch name if necessary
    ssh 3723642@git.sd3.gpaas.net deploy default.git deployment

Server URL:

https://api.orphacode.org/

## Authorization by APIkey:
Mandatory in request header:

* any string for user level

        curl -X GET "http://localhost:8080/.../..."
             -H  "accept: application/json"
             -H  "SIMPLE-API-KEY: test"