# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "attrs==21.4.0",
    "certifi==2021.10.8",
    "charset-normalizer==2.0.12",
    "click==8.0.4",
    "clickclick==20.10.2",
    "connexion==2.6.0",
    "elasticsearch==7.6.0",
    "Flask==2.0.3",
    "Flask-Cors==3.0.10",
    "Flask-Testing==0.8.1",
    "idna==3.3",
    "importlib-resources==5.4.0",
    "inflection==0.5.1",
    "itsdangerous==2.1.1",
    "Jinja2==3.0.3",
    "jsonschema==4.4.0",
    "MarkupSafe==2.1.1",
    "openapi-schema-validator==0.2.3",
    "openapi-spec-validator==0.4.0",
    "pyrsistent==0.18.1",
    "python-dateutil==2.6.0",
    "python-dotenv==0.20.0",
    "PyYAML==6.0",
    "requests==2.27.1",
    "six==1.16.0",
    "swagger-ui-bundle==0.0.6",
    "urllib3==1.26.9",
    "Werkzeug==2.0.3",
    "xmltodict==0.13.0",
    "zipp==3.7.0"
    ]

setup(
    name=NAME,
    version=VERSION,
    description="ORPHA Nomenclature - RD-CODE project",
    author_email="data.orphanet@inserm.fr",
    url="",
    keywords=["Swagger", "ORPHA Nomenclature - RD-CODE project"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'swagger_server=swagger_server.__main__:main',
            'rdcode_download=swagger_server.src.rdcode_download:run',
            'rdcode_xml2json=swagger_server.src.rdcode_xml2json:run',
            'rdcode_injection=swagger_server.src.rdcode_injection:run',
            ]
        },
    long_description="""\
    The Orphanet nomenclature is a multilingual, standardised, controlled medical terminology specific to rare diseases, that includes all clinical entities registered in the Orphanet database (www.orpha.net). Each clinical entity (disorder, group of disorders, or subtype of a disorder) is associated with a unique numerical identifier named ORPHAcode, as well as a preferred term, synonyms, and a definition.  In the frame of the RD-CODE project, co-funded by the European Union’s Third Health Program, Orphanet developped this API. It intends to support Member States in the implementation of the ORPHA nomenclature to rare diseases-specific codification systems. Starting with countries that have no systematic implementation of the Orpha codification yet, but that are actively committed already in doing so, this project will provide a sufficient real-world implementation experience to be captured by other countries in the future.  Disclaimers:  The API arise from the RD-CODE project which has received funding from the European Union in the framework of the Health Program.  The content of this API represents the views of the author only and is his/her sole responsibility; it cannot be considered to reflect the views of the European Commission and/or the Consumers, Health, Agriculture and Food Executive Agency or any other body of the European Union. The European Commission and the Agency do not accept any responsibility for use that may be made of the information it contains.  We have chosen to apply the Commons Attribution 4.0 International (CC BY 4.0) to all copyrightable parts of our databases. This means that you are free to copy, distribute, display and make commercial use of these databases in all legislations, provided you give us credit.
    """
)
