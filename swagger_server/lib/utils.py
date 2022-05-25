import copy
import json
from pathlib import Path
import logging
import re
import time
from typing import Union
import xmltodict
import os


FORMAT = '%(asctime)-26s %(name)-26s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


class Node(dict):
    def __init__(self):
        super().__init__()
        self["Preferred term"] = ""
        self["ORPHAcode"] = ""
        self["Classification"] = {}
        self["Classification"]["ID of the classification"] = ""
        self["Classification"]["ORPHAcode"] = ""
        self["Classification"]["Name of the classification"] = ""
        self["Classification"]["Preferred term"] = ""
        self["Parent"] = []
        self["Child"] = []


def parse_file_stem(filename: Union[str, Path]) -> str:
    """Return a file stem according to the data type of a given filename 

    Parameters
    ----------
    filestem : Union[str, Path]
        Stem of the file to parse

    Returns
    -------
    str
        A renamed file stem 
    """    
    file_stem = filename.stem.lower()
    if "CZ" in file_stem:
        file_stem = file_stem.replace("CZ", "CS")
    if "cz" in file_stem:
        file_stem = file_stem.replace("cz", "cs")

    # Remove the suffixed date
    file_stem = re.sub("_[0-9]{4}(?![0-9])", "", file_stem)

    # rename file_stem for ORPHAclassification files (e.g. orphaclassification_146_rare_cardiac_disease_en -> orphaclassification_146_en)
    if "ORPHAclassification".lower() in file_stem:
        file_stem_split = file_stem.split("_")
        file_stem = "{}_{}_{}".format(file_stem_split[0], file_stem_split[1], file_stem_split[-1])

    return file_stem


def parse_file(in_file_path, input_encoding, xml_attribs):
    """
    Parse an xml file with "xmltodict" external module and return the file as a dictionary and the extraction date.
    Can read the encoding of the file in the xml header if input_encoding=="auto" OR decode the file with
    the specified encoding.
    Can read the JDBOR extraction date in the xml attribute of the JDBOR node but the rest of the code is meant to
    work without the xml attributes to read them call with xml_attribs=True.

    :param in_file_path: path, source xml file
    :param input_encoding: valid encoding OR "auto"
    :param xml_attribs: Boolean, read the xml attribute such as "id" in <Disorder id="12948"> ?
    :return: tuple(xml_dict, extraction date)
        WHERE
        xml_dict: xml source file parsed as a dictionary
        extraction date: str, date of JDBOR extraction
    """
    start = time.time()

    # Encoding detection
    with open(in_file_path, "rb") as ini:
        xml_declaration = ini.readline()
        date = ini.readline()

    if input_encoding.lower() == "auto":
        xml_declaration = xml_declaration.decode()
        pattern = re.compile("encoding=\"(.*)\"[ ?]")
        encoding = pattern.search(xml_declaration).group(1)
        logger.info('encoding: {} (auto)'.format(encoding))

        with open(in_file_path, "r", encoding=encoding) as ini:
            xml_dict = xmltodict.parse(ini.read(), xml_attribs=xml_attribs)

    else:
        with open(in_file_path, "r", encoding=input_encoding) as ini:
            logger.info('encoding: {} (from config file)'.format(input_encoding))
            xml_dict = xmltodict.parse(ini.read(), xml_attribs=xml_attribs)

    # Get JDBOR extraction date
    try:
        date_regex = re.compile("ExtractionDate=\"(.*)\" version")
        date = date_regex.search(date.decode()).group(1)
    except:
        date_regex = re.compile("date=\"(.*)\" version")
        date = date_regex.search(date.decode()).group(1)
    logger.info("JDBOR extract: {}".format(date))

    # print(xml_dict)
    # DumpS then loadS: convert ordered dict to dict
    # xml_dict = json.loads(json.dumps(xml_dict, ensure_ascii=False))
    logger.info("parsing: {}".format(time.time() - start))
    return xml_dict, date


def subset_xml_dict(xml_dict):
    """
    Reroot the xml to skip the trivial JDBOR/*List/ for homogeneity (ClassificationList vs DisorderList)

    :param xml_dict: xml source file parsed as a dictionary
    :return: xml source file parsed as a dictionary rerooted to the first *List
    """
    # Return the first meaningful node for homogeneity
    key = list(xml_dict["JDBOR"].keys())
    if "Availability" in key:
        key.pop(key.index("Availability"))

    new_key = []
    for item in key:
        # the xml attribute are prefixed with @ and can be discarded for application
        if "@" not in item:
            new_key.append(item)
    # print(key)
    if len(new_key) == 1:
        new_key = new_key[0]
    else:
        logger.error("ERROR: Multiple root XML key: {}".format(new_key))
        exit(1)

    xml_dict = xml_dict["JDBOR"][new_key]
    return xml_dict


def simplify(xml_dict, rename_orpha):
    """
    :param xml_dict: xml source file parsed as a dictionary
    :param rename_orpha: boolean, force the conversion of ALL OrphaNumber/i or OrphaCode/i to ORPHAcode
    :return: node_list: List of Disorder object with simplified structure
    i.e.:
    [{
        "name": "Congenital pericardium anomaly",
        "ORPHAcode": "2846",
        "hch_id": "148",
        "parents": ["97965"],
        "childs": ["99129", "99130", "99131"]
    },
    {...}
    ]
    """
    # start = time.time()

    # Simplify the xml structure for homogeneity
    xml_dict = simplify_xml_list(xml_dict)

    # print(xml_dict)
    # output_simplified_dictionary(out_file_path, index, xml_dict)

    key = list(xml_dict.keys())
    # print(key)

    if len(key) == 1:
        key = key[0]
    else:
        logger.error("ERROR: Multiple root XML key: {}".format(key))
        exit(1)

    node_list = xml_dict[key]
    node_list = json.dumps(node_list, ensure_ascii=False)

    pattern = re.compile("List\":")
    node_list = pattern.sub("\":", node_list)
    if rename_orpha:
        pattern = re.compile("OrphaCode", re.IGNORECASE)
        node_list = pattern.sub("ORPHAcode", node_list)
        pattern = re.compile("OrphaNumber", re.IGNORECASE)
        node_list = pattern.sub("ORPHAcode", node_list)
    node_list = json.loads(node_list)

    logger.info("Disorder concepts number: {}".format(len(node_list)))
    return node_list


def simplify_xml_list(xml_dict):
    """
    Recursively simplify the xml structure for homogeneity
    Remove
    <ClassificationNodeList count="XX">
        <ClassificationNode>
            <ClassificationNodeChildList count="XX">
    To produce
    ClassificationNode: [{*current node information*, ClassificationNodeChild: {}}, ...]

    :param xml_dict: xml source file parsed as a dictionary
    :return: simplified xml_dict
    """
    if isinstance(xml_dict, dict):
        for key, elem in xml_dict.items():
            if key.endswith("List"):
                xml_dict = simplify_list(xml_dict, key)
            simplify_xml_list(elem)
    elif isinstance(xml_dict, list):
        for elem_list in xml_dict:
            simplify_xml_list(elem_list)
    return xml_dict


def simplify_list(parent, key):
    """
    Remove trivial key and regroup it's children as a "child" property of the trivial key's parent
    Properly map empty children as 'None'

    :param parent: Dictionary containing key to simplify
    :param key: Dictionary key containing the term "*List"
    :return: simplified dictionary
    """
    child_value = parent[key]
    if child_value is not None and child_value != "0":
        child_value = [child_value[child] for child in child_value if child][0]
        if isinstance(child_value, dict) or isinstance(child_value, str):
            child_value = [child_value]
        parent[key] = child_value
    else:
        parent[key] = None
    return parent


def clean_textual_info(node_list, file_stem):
    """
    For product 1 (cross references) or ORPHAnomenclature data (RDcode)

    "SummaryInformation" in xml
    output:
    "SummaryInformation": [{"Definition": "definition text"}, {"info": "automatic definition text"}]
    Definition AND info key are both optional, in this case SummaryInformation: None

    :param node_list: list of disorder
    :param node_list: File stem of the processed xml file
    :return: list of disorder with reworked textual info
    """
    if "product1" in str(file_stem).lower():
        # for each disorder object in the file
        for disorder in node_list:
            TextAuto = ""
            textual_information_list = []
            if "TextAuto" in disorder:
                temp = {}
                TextAuto = disorder["TextAuto"]["Info"]
                temp["Info"] = TextAuto
                textual_information_list.append(temp)
                disorder.pop("TextAuto")
            if "SummaryInformation" in disorder:
                if disorder["SummaryInformation"] is not None:
                    for text in disorder["SummaryInformation"]:
                        if text["TextSection"] is not None:
                            temp = {}
                            key = text["TextSection"][0]["TextSectionType"]["Name"]
                            temp[key] = text["TextSection"][0]["Contents"]
                            textual_information_list.append(temp)
                if textual_information_list:
                    disorder["SummaryInformation"] = textual_information_list
                else:
                    disorder["SummaryInformation"] = None
            else:
                disorder["SummaryInformation"] = None
    elif "orphanomenclature" in file_stem:
        for disorder in node_list:
            textual_information_list = []
            if "SummaryInformation" in disorder:
                if disorder["SummaryInformation"] is not None:
                    if "TextAuto" in disorder["SummaryInformation"][0]:
                        if disorder["SummaryInformation"][0]["TextAuto"] is not None:
                            TextAuto = disorder["SummaryInformation"][0]["TextAuto"]["Info"]
                            disorder["Definition"] = TextAuto
                    elif "TextSection" in disorder["SummaryInformation"][0]:
                        if disorder["SummaryInformation"][0]["TextSection"] is not None:
                            if disorder["SummaryInformation"][0]["TextSection"][0] is not None:
                                Definition = disorder["SummaryInformation"][0]["TextSection"][0]["Contents"]
                                disorder["Definition"] = Definition
                    disorder.pop("SummaryInformation")
                else:
                    disorder["Definition"] = "None available"
            else:
                disorder["Definition"] = "None available"
        
    return node_list


def clean_single_name_object(node_list):
    """
    Take the list of disorder and substitute object by a text if they contain only one "Name" property
    keeps multi-property object otherwise
    i.e.:
    disorder["DisorderType"]["Name"] = "Disease"
    to =>
    disorder["DisorderType"] = "Disease"
    Work in depth recursively
    :param node_list: list of disorder
    :return: list of disorder without single name object
    """
    for disorder in node_list:
        for elem in disorder:
            disorder[elem] = recursive_clean_single_name_object(disorder[elem])
    return node_list


def recursive_clean_single_name_object(elem):
    """
    Take the list of disorder and substitute object by a text if they contain only one "Name" property
    keeps multi-property object otherwise
    i.e.:
    disorder["DisorderType"]["Name"] = "Disease"
    to =>
    disorder["DisorderType"] = "Disease"
    Work in depth recursively
    :param elem: property of disorder
    :return: list of disorder without single name object
    """
    if isinstance(elem, dict):
        keys = elem.keys()
        if len(keys) == 1:
            if "Name" in keys:
                name = elem.pop("Name")
                elem = name
        else:
            for child in elem:
                elem[child] = recursive_clean_single_name_object(elem[child])
    elif isinstance(elem, list):
        for index, sub_elem in enumerate(elem):
            sub_elem = recursive_clean_single_name_object(sub_elem)
            elem[index] = sub_elem
    return elem


def convert(hch_id, xml_dict, classification_orpha):
    """
    :param hch_id: String, Orphanet classification number
    :param xml_dict: xml source file parsed as a dictionary
    :param classification_orpha: Orpha_ID of classification
    :return: node_list: List collection of Disorder
    i.e.:
    [
    {"Preferred term": "Congenital pericardium anomaly",
    "OrphaNumber": "2846",
    "hch_id": "148",
    "Parent": ["97965"],
    "Child": ["99129", "99130", "99131"]
    },
    {...}
    ]
    """
    start = time.time()
    # With 2020 dataset the Orphanet classification level appear in the file, it contain only the OrphaNumber(ORPHAcode)
    # and the name, we need to capture this special case
    try:
        disorder = {'ORPHAcode': xml_dict["ORPHAcode"], 'ExpertLink': xml_dict["ExpertLink"], 'Name': xml_dict["Name"]}
    except KeyError:
        disorder = {'ORPHAcode': xml_dict["ORPHAcode"], 'ExpertLink': "", 'Name': xml_dict["Name"]}

    # With 2020 dataset the Orphanet classification level appear in the file, it has a scpecial label for hierarchy,
    # we need to capture this special case
    try:
        ClassificationNodeChild = xml_dict["ClassificationNode"][0]["ClassificationNodeChild"]
    except KeyError:
        ClassificationNodeChild = xml_dict["ClassificationNodeRoot"]

    xml_dict = {"Disorder": disorder, "ClassificationNodeChild": ClassificationNodeChild}

    hch_tag = xml_dict["Disorder"]["Name"]
    parent = None

    node_dict = {}
    node_dict = make_node_dict(node_dict, xml_dict, hch_id, hch_tag, parent, classification_orpha)

    node_list = list(node_dict.values())

    logger.info("{} disorder concepts".format(len(node_list)))
    logger.info("convert time: {}s".format(time.time() - start))
    return node_list


def make_node_dict(node_dict, xml_dict, hch_id, hch_tag, parent, classification_orpha):
    """
    Recursively parse xml_dict to output a collection of Disorder with all their children

    :param node_dict: Dictionary of Disorders i.e.
    {2846: {
        "Preferred term": "Congenital pericardium anomaly",
        "OrphaNumber": "2846",
        "hch_id": "148",
        "Parent": ["97965"],
        "Child": ["99129", "99130", "99131"]
        },
    2847: {...}
    }
    :param hch_id: String, Orphanet classification number
    :param hch_tag: String, Orphanet classification tag
    :param xml_dict: xml source file parsed as a dictionary
    :param parent: Orpha_ID of parent Disorder
    :param classification_orpha: Orpha_ID of classification
    :return: node_dict
    """
    # print(xml_dict)
    node = Node()
    node["ORPHAcode"] = xml_dict["Disorder"]["ORPHAcode"]
    node["Preferred term"] = xml_dict["Disorder"]["Name"]
    node["Classification"]["ORPHAcode"] = classification_orpha
    node["Classification"]["ID of the classification"] = hch_id
    node["Classification"]["Name of the classification"] = hch_tag
    node["Classification"]["Preferred term"] = hch_tag
    node["Parent"] = [parent]
    # print(node)
    if xml_dict["ClassificationNodeChild"] is not None:
        for child in xml_dict["ClassificationNodeChild"]:
            node["Child"].append(child["Disorder"]["ORPHAcode"])
            node_dict = make_node_dict(node_dict, child, hch_id, hch_tag, node["ORPHAcode"], classification_orpha)
    if node["ORPHAcode"] in node_dict:
        node_dict[node["ORPHAcode"]]["Child"] = merge_unique(node_dict[node["ORPHAcode"]]["Child"], node["Child"])
        node_dict[node["ORPHAcode"]]["Parent"] = merge_unique(node_dict[node["ORPHAcode"]]["Parent"], node["Parent"])
        # print(node_dict[node.OrphaNumber].Child)
    else:
        node_dict[node["ORPHAcode"]] = node
    return node_dict


def merge_unique(list1, list2):
    """
    Merge two list and keep unique values
    """
    for item in list2:
        if item not in list1:
            list1.append(item)
    return list1


def remap_integer(node_list):
    """
    Cast number as integer (from string) using regex
    SKIP number preceded by "Reference: "

    :param node_list: list of disorder
    :return:
    """
    node_list = json.dumps(node_list)

    def hexrepl(match):
        """ Replace function for the capture group """
        value = match.group()[1:-1]
        return value

    pattern = re.compile("(?<!Reference\":\\s)\"\\d+\"")
    node_list = pattern.sub(hexrepl, node_list)

    node_list = json.loads(node_list)
    return node_list


def insert_date(node_list, extract_date):
    """
    Append the JDBOR extract date to each disorder entry

    :param node_list: list of disorder objects
    :param extract_date: JDBOR extract date
    :return: node_list with extract date
    """
    for node in node_list:
        node["Date"] = extract_date
    return node_list


def rename_terms(node_list):
    """
    Rename some terms for RDcode

    :param node_list: list of disorder objects
    :return: node_list with renamed terms
    """
    node_list = json.dumps(node_list)

    patterns = {"\"Totalstatus\":": "\"Status\":",
                "\"Name\":": "\"Preferred term\":",
                "\"PreferredTerm\":": "\"Preferred term\":",
                # "\"GroupOfType\":": "\"ClassificationLevel\":",
                "\"ExpertLink\":": "\"OrphanetURL\":",
                "\"DisorderType\":": "\"Typology\":",
                }

    for key, value in patterns.items():
        pattern = re.compile(key)
        node_list = pattern.sub(value, node_list)

    node_list = json.loads(node_list)
    return node_list


def rework_ICD(node_list, _type: str="icd10"):
    """
    remove "source" from ICD external reference
    rename ExternalReference to Code ICD and reference to Code ICD10

    :param node_list:
    :return: node_list with reworked ICD reference
    """
    node_list = json.dumps(node_list)

    # patterns = {"\"ExternalReference\":": "\"Code ICD\":",
    #             "\"Reference\":": "\"Code ICD10\":"}

    patterns = {
        "ExternalReference": "Code ICD",
        "Reference": "Code {}".format(_type.upper())
        }

    for key, value in patterns.items():
        pattern = re.compile(key)
        node_list = pattern.sub(value, node_list)

    node_list = json.loads(node_list)

    for node in node_list:
        if node["Code ICD"]:
            for index, ref in enumerate(node["Code ICD"]):
                node["Code ICD"][index].pop("Source")
    return node_list


def rework_OMIM(node_list):
    """
    remove "source" from OMIM external reference
    rename ExternalReference and reference to Code OMIM

    :param node_list:
    :return: node_list with reworked OMIM reference
    """
    node_list = json.dumps(node_list)

    patterns = {"\"ExternalReference\":": "\"Code OMIM\":",
                "\"Reference\":": "\"Code OMIM\":"}

    for key, value in patterns.items():
        pattern = re.compile(key)
        node_list = pattern.sub(value, node_list)

    node_list = json.loads(node_list)

    for node in node_list:
        if node["Code OMIM"]:
            for index, ref in enumerate(node["Code OMIM"]):
                node["Code OMIM"][index].pop("Source")

    return node_list


def output_simplified_dictionary(out_file_path, index, xml_dict, indent_output, output_encoding):
    """
    Output simplified dictionary in json format DEBUG helper function

    Simplified the xml structure to give a consistent hierarchy:
    Disorder: {}
    Child: [
        {
        Disorder: {}
        Child: []
        },
        {
        Disorder: {}
        Child: []
        }
    ]

    :param out_file_path: path to output file
    :param index: name of the elasticsearch index
    :param xml_dict: xml source file parsed as a dictionary
    :return: None
    """
    if indent_output:
        indent = 2
    else:
        indent = None
    with open(out_file_path, "w", encoding=output_encoding) as out:
        out.write("{{\"index\": {{\"_index\":\"{}\"}}}}\n".format(index))
        out.write(json.dumps(xml_dict, indent=indent, ensure_ascii=False) + "\n")


def gene_indexing(node_list_gene):
    """
    Invert the indexing of the product6 "gene" to index the relationships between gene and disorder
    from the gene point of view

    :param node_list_gene: copy of processed node_list
    :return: similar list of disorder-gene relation but indexed by gene
    ie.
    [
    {
    "Name": "kinesin family member 7",
    "Symbol": "KIF7",
    "Synonym": [
        "JBTS12"
    ],
    "GeneType": "gene with protein product",
    "ExternalReference": [
        {
        "Source": "Ensembl",
        "Reference": "ENSG00000166813"
        },
        {...},
    ],
    "Locus": [
        {
        "GeneLocus": "15q26.1",
        "LocusKey": "1"
        }
    ],
    "GeneDisorderAssociation": [
        {
        "SourceOfValidation": "22587682[PMID]",
        "DisorderGeneAssociationType": "Disease-causing germline mutation(s) in",
        "DisorderGeneAssociationStatus": "Assessed",
        "disorder": {
            "ORPHAcode": "166024",
            "ExpertLink": "http://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=en&Expert=166024",
            "Name": "Multiple epiphyseal dysplasia, Al-Gazali type",
            "DisorderType": "Disease",
            "DisorderGroup": "Disorder"
        }
        },
        {...}
    ]
    }
    ]
    """
    gene_dict = dict()
    for disorder in node_list_gene:
        # disorder still contains gene association
        disorder_info = copy.deepcopy(disorder)

        # association_list : list, need to exploit with according gene
        # disorder_info now only contains disorder
        association_list = disorder_info.pop("DisorderGeneAssociation")

        for association_info in association_list:
            # Each association_info contains a different Gene,
            # we need to index the Gene then substitute it with disorder_info
            gene_info = association_info.pop("Gene")
            gene_index = gene_info["Symbol"]
            # Initialize the Gene index on first occurrence
            if gene_index not in gene_dict:
                gene_dict[gene_index] = {}
                for gene_prop, gene_prop_value in gene_info.items():
                    gene_dict[gene_index][gene_prop] = gene_prop_value
                gene_dict[gene_index]["GeneDisorderAssociation"] = []
            # insert disorder_info in the association_info
            association_info["disorder"] = disorder_info
            # Extend the GeneDisorderAssociation with this new disorder relation
            gene_dict[gene_index]["GeneDisorderAssociation"].append(association_info)

    node_list_gene = list(gene_dict.values())
    return node_list_gene


def recursive_unwanted_orphacode(elem):
    """
    Remove the ORPHAcode past the one defined at the disorder's root level
    ! NO quality check !
    Useless since new Orphadata generation

    :param elem: disorder object or property
    :return: disorder object or property without ORPHAcode key
    """
    if isinstance(elem, dict):
        if "ORPHAcode" in elem.keys():
            elem.pop("ORPHAcode")
        for child in elem:
            recursive_unwanted_orphacode(elem[child])
    elif isinstance(elem, list):
        for sub_elem in elem:
            recursive_unwanted_orphacode(sub_elem)
    return elem


def remove_unwanted_orphacode(node_list):
    """
    Remove the ORPHAcode past the one defined at the disorder's root level
    ! NO quality check !
    Useless since new Orphadata generation

    :param node_list: list of disorder
    :return: list of disorder without ORPHAcode key past the main one
    """
    for disorder in node_list:
        # elem is an attribute of the disorder
        for elem in disorder:
            recursive_unwanted_orphacode(disorder[elem])
    return node_list


def recursive_template(elem):
    if isinstance(elem, dict):
        for child in elem:
            recursive_template(child)
    elif isinstance(elem, list):
        for sub_elem in elem:
            recursive_template(sub_elem)
    return elem

