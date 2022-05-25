"""

Module used to convert each orphadata XML file in JSON format.

JSON files represent the inputs to be injected in Elasticsearch instance.

"""
import argparse
import copy
import json
import logging
from pathlib import Path
import re
import time
from typing import Union
import xmltodict
import os


from swagger_server.lib import utils


FORMAT = '%(asctime)-26s %(name)-26s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
name = __name__ if __name__ != '__main__' else 'orpha_xml2json'
logger = logging.getLogger(name)


class Config():
    def __init__(self) -> None:        
        self.xmlpath = ''
        self.out_folder = Path('json_data')
        self.input_encoding = 'auto'
        self.index_prefix = ''
        self.cast_as_integer = True
        self.output_encoding = "UTF-8"

    def set_attributes(self, args) -> None:
        self.xmlpath = Path(args.xmlpath)
        self.out_folder = Path(args.out)
        self.input_encoding = args.encoding
        self.index_prefix = args.index_prefix
        self.cast_as_integer = args.cast_int
        self.output_encoding = args.out_encoding


def parse_args():
    parser = argparse.ArgumentParser(description='Convert XML from Orphanet Nomenclature Pack into Elasticsearch compatible JSON files.')
    parser.add_argument(
        "-xmlpath",
        required=True,
        nargs="?",
        type=str,
        help="Path or filename of XML file(s)"
    )
    parser.add_argument(
        "-out",
        required=False,
        nargs="?",
        type=str,
        default="json_data",
        help="Output directory where JSON files will be written. Default: 'json_data'."
    )
    parser.add_argument(
        "-encoding",
        required=False,
        nargs="?",
        type=str,
        default="auto",
        help="Encoding type (UTF-8, ISO-8859-1 or others - 'auto' will try to automatically find the relevant encoding type) to be used when reading XML files. Default: 'auto'"
    )
    parser.add_argument(
        "-index_prefix",
        required=False,
        nargs="?",
        type=str,
        default="rdcode",
        help="Prefix of the index name that will be created in Elasticsearch. Default: 'rdcode'."
    )
    parser.add_argument(
        "-cast_int",
        required=False,
        nargs="?",
        type=bool,
        default=True,
        help="True to remap numbers as integers, False otherwise. Default: True."
    )
    parser.add_argument(
        "-out_encoding",
        required=False,
        nargs="?",
        type=str,
        default="UTF-8",
        help="Encoding type ((UTF-8, ISO-8859-1 or others) to be used when writing JSON files. Default: UTF-8"
    )

    config = Config()
    config.set_attributes(parser.parse_args())

    return config


def output_elasticsearch_file(node_list: dict, json_filename: str, es_index_name: str, output_encoding: str):
    """
    Output json file, elasticsearch injection ready

    :param json_filename: path to output file
    :param index: name of the elasticsearch index
    :param node_list: list of Disorder, each will form an elasticsearch document
    :param output_encoding: "UTF-8" or "iso-8859-1"
    :return: None
    """
    start = time.time()
    indent = None
    with open(json_filename, "w", encoding=output_encoding) as out:
        for val in node_list:
            out.write("{{\"index\": {{\"_index\":\"{}\"}}}}\n".format(es_index_name))
            out.write(json.dumps(val, indent=indent, ensure_ascii=False) + "\n")
    logger.info("writing time: {}s".format(time.time() - start))


def process(in_file_path: Path, config: Config):
    # process(filename, config.out_folder, config.input_encoding, config.indent_output, config.output_encoding)
    """
    Complete Orphadata XML to Elasticsearch JSON process

    :param in_file_path: input file path
    :param config: Config instance
    :return: None (Write file (mandatory) / upload to elastic cluster)
    """
    file_stem = utils.parse_file_stem(filename=in_file_path)
    logger.info("####################")
    logger.info('file stem:  {}'.format(file_stem))

    # create ES index name variable    
    index = config.index_prefix
    if index:
        index = "{}_{}".format(index, file_stem)
    else:
        index = file_stem
    
    # create json outfilename variable
    out_file_name = index + ".json"
    out_file_path = config.out_folder / out_file_name

    # Parse source xml file and return the date also reroot the xml to skip the trivial JDBOR/*List/
    xml_dict, extract_date = utils.parse_file(in_file_path, config.input_encoding, False)
    xml_dict = utils.subset_xml_dict(xml_dict)

    # get variable parameters for convert function
    if "ORPHAclassification".lower() in file_stem:
        hch_id = file_stem.split("_")[1]
        classification_orpha = xml_dict["Classification"]["OrphaNumber"]

    # initialize time computation variable
    start = time.time()

    # remove intermediary dictionary (xml conversion artifact) and rename OrphaNumber
    rename_orpha = True  # OrphaNumber to ORPHAcode
    node_list = utils.simplify(xml_dict, rename_orpha)

    # Regroup textual_info for product1 or RDcode orphanomenclature
    node_list = utils.clean_textual_info(node_list, file_stem=file_stem)

    if "ORPHAclassification".lower() not in file_stem:
        # Remap object with single "Name" to string
        node_list = utils.clean_single_name_object(node_list)

    if "ORPHAclassification".lower() in file_stem:
        hch_id = file_stem.split("_")[1]
        node_list = utils.convert(hch_id, node_list, classification_orpha)

    # Cast number as integer (from string)
    if config.cast_as_integer:
        node_list = utils.remap_integer(node_list)

    node_list = utils.insert_date(node_list, extract_date)
    if "ORPHAclassification".lower() not in file_stem:
        node_list = utils.rename_terms(node_list)
    if "orpha_icd10_" in file_stem:
        node_list = utils.rework_ICD(node_list, _type="icd10")
    if "orpha_icd11_" in file_stem:
        node_list = utils.rework_ICD(node_list, _type="icd11")
    if "orpha_omim_" in file_stem:
        node_list = utils.rework_OMIM(node_list)

    logger.info("process time: {}s".format(time.time() - start))

    return node_list, out_file_path, index


def main(config: Config):
    # check if xml path exists
    if not config.xmlpath.exists():
        logger.error('ERROR: Your XML path {} seems to not exist.'.format(config.xmlpath))
        exit(1)

    # create output folder if it doesn't exist
    os.makedirs(config.out_folder, exist_ok=True)

    # ensure xml inputs being iterable 
    if config.xmlpath.is_file():
        xml_inputs =[config.xmlpath]
    elif config.xmlpath.is_dir():
        xml_inputs = config.xmlpath.iterdir()

    # Process files in designated folders
    for filename in xml_inputs:
        if filename.suffix == ".xml" and "orphaclassification_235" not in filename.stem.lower():
            logger.info(filename)
            # process xml data
            node_list, json_filename, es_index_name = process(in_file_path=filename, config=config)
            # write ES compatible json file
            output_elasticsearch_file(node_list=node_list, json_filename=json_filename, es_index_name=es_index_name, output_encoding=config.output_encoding)


def run():
    config = parse_args()
    start = time.time()
    main(config)
    logger.info('Total computation time: {}s'.format(time.time() - start))


if __name__ == "__main__":
    run()