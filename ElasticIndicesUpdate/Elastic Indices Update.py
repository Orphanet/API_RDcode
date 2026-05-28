import os
import glob
import xmltodict
import json
import requests
import pandas as pd
import tarfile
import elasticsearch as es
from elasticsearch.helpers import scan
import os
import copy
import random
import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.varenv")
ELASTIC_URL = os.getenv("ELASTIC_URL")
ELASTIC_USER = os.getenv("ELASTIC_USER")
ELASTIC_PASS = os.getenv("ELASTIC_PASS")

es_server_prod = es.Elasticsearch(
    ELASTIC_URL,
    basic_auth=(ELASTIC_USER, ELASTIC_PASS)
)

body = json.dumps({
  "mappings": {
    "properties": {
      "ExternalReference" : {
        "type" : "nested"
      }
    }
  }
})

pack_path = "../../NomenclaturePack25/Orphanet_Nomenclature_Pack_"
langs = ["cs", "de", "en", "es", "fr", "it", "nl", "pl", "pt"]
inactiv_codes = ["513", "8208", "8225", "8449"]

relation = {"cs" : "E (přesné mapování (termíny a pojmy jsou rovnocenné))",
           "de" : "Genaues Mapping (der Begriff und das Konzept ist äquivalent)",
           "en" : "E (Exact mapping: the two concepts are equivalent)",
           "es" : "correspondencia exacta (los términos y los conceptos son equivalentes)",
           "fr" : "E (Alignement exact: les deux concepts sont équivalents)",
           "it" : "mappatura corretta (i termini e i concetti sono equivalenti)",
           "nl" : "exacte overeenkomst (de termen en concepten zijn equivalent)",
           "pl" : "E (dokładne mapowanie (terminy i pojęcia są równoważne)",
           "pt" : "Direção exacta (os termos e os conceitos são equivalentes)"}

validation = {"cs" : "Ověřeno",
           "de" : "Validiert",
           "en" : "Validated",
           "es" : "Validado",
           "fr" : "Validé",
           "it" : "Confermato",
           "nl" : "Gevalideerd",
           "pl" : "Zwalidowany",
           "pt" : "Validado"}

parentPref = {"cs" : "Preferenční rodič",
           "de" : "Bevorzugte Zuordnung",
           "en" : "Preferential parent",
           "es" : "Cabeza de clasificación preferencial",
           "fr" : "Parent préférentiel",
           "it" : "Termine madre preferenziale",
           "nl" : "Preferentiële ouder",
           "pl" : "Uprzywilejowany rodzic",
           "pt" : "Progenitor preferencial"}



# ## Load Snomed mapping file


def load_snomed():
    df = pd.read_excel("ORPHA-SNOMEDCT_Mapping_File_production_2025.xlsx", skiprows=[1, 2])
    snomed = df.astype(str).set_index(df.columns[0])["Unnamed: 2"].to_dict()
    return snomed

snomed = load_snomed()


# ## Load diff file

prefixes = {
    "Newly included ORPHAcodes" : "newly_included_",
    "Newly Inactive ORPHAcodes" : "newly_inactive_",
    "Classification level update" : "classif_update_",
    "New ORPHA-to-ICD10 mapping" : "new_icd10_",
    "Updated ORPHA-to-ICD10 mapping" : "update_icd10_",
    "Removed ORPHA-to-ICD10 mapping" : "removed_icd10_",
    "New ORPHA-to-ICD11 mapping" : "new_icd11_",
    "Updated ORPHA-to-ICD11 mapping" : "update_icd11_",
    "Removed ORPHA-to-ICD11 mapping" : "removed_icd11_"
}

def diffLoad():
    result = { } 

    names = pd.ExcelFile("../../NomenclaturePack25/Orphanet_Nomenclature_Pack_EN/ORPHAnomenclature_diff_en_2025.xlsx").sheet_names
    df_dict = pd.read_excel("../../NomenclaturePack25/Orphanet_Nomenclature_Pack_EN/ORPHAnomenclature_diff_en_2025.xlsx", skiprows=1, sheet_name=names)

    for sheet, tmp in df_dict.items():
        if "ORPHAcode" not in tmp.columns:
            new_header = tmp.iloc[0] 
            df = tmp[1:] 
            df.columns = new_header
        else:
            df = tmp
        for index, row in df.iterrows():
            orpha = str(row["ORPHAcode"])
            if orpha not in result:
                result[orpha] = { } 
            for key in row.keys():
                result[orpha].update({prefixes[sheet] + key : row[key]})
    return result

diff = diffLoad()

def diffGet(dico, key):
    result = False
    for sheets in prefixes.values():
        result = dico.get(sheets + key, False)
        if result:
            return result

def diffFormat(diff):
    result = { } 
    for k, v in diff.items():
        result[k] = {
            "ORPHAcode" : None,
            "Preferred term" : None,
            "ClassificationLevel" : None,
            "Status": None,
            "Status Update" : { },
            "Classification Update" : { },
            "ICD10 Update" : { },
            "ICD11 Update" : { }
        }
        result[k]["ORPHAcode"] = diffGet(v, "ORPHAcode")
        result[k]["Preferred term"] = diffGet(v, "Name (Preferred_Term)")
        result[k]["ClassificationLevel"] = diffGet(v, "ClassificationLevel")

    return result

finalDiff = diffFormat(diff)


# # Build main dictionary

def parcours_prof(node, current_classif, final_dict, parent):
    if current_classif["ID of the classification"] == "235":
        node = node["ClassificationNodeChildList"]["ClassificationNode"]
    if "Disorder" in node:
        typology = node["Disorder"]["DisorderType"]["Name"]["#text"]
        orphacode = node["Disorder"]["OrphaCode"]
        children = []
    else:
        return

    if node['ClassificationNodeChildList']['@count'] != '0':
        if node['ClassificationNodeChildList']['@count'] == '1':
            children.append(parcours_prof(node['ClassificationNodeChildList']['ClassificationNode'], current_classif, final_dict, orphacode)) 
        else:
            for child in node['ClassificationNodeChildList']['ClassificationNode']:
                children.append(parcours_prof(child, current_classif, final_dict, orphacode)) 

    if orphacode in final_dict.keys():
        exists = False
        tmp_classif = final_dict[orphacode].get("Classification", [])
        for classif in tmp_classif:
            if current_classif["ID of the classification"] == classif["ID of the classification"]:
                exists = True
                break
        if not exists:
            tmp_classif.append(current_classif)
    else:
        final_dict[orphacode] = { }
        tmp_classif = [current_classif]

    tmpParent = [parent] if parent else []
    if not "Inheritance" in final_dict[orphacode]:
        final_dict[orphacode]["Inheritance"] = { }
    elif current_classif["ID of the classification"] in final_dict[orphacode]["Inheritance"] :
        tmpParent = final_dict[orphacode]["Inheritance"][current_classif["ID of the classification"]].get("Parent", None)
        if tmpParent:
            tmpParent.append(parent)

    final_dict[orphacode]["Inheritance"].update({
        current_classif["ID of the classification"] : {
            "Parent" : tmpParent,
            "Children" : children if children else None
        }
    })
    tmp = { 
        "Typology" : typology,
        "Classification" : tmp_classif,
        "Inheritance" : final_dict[orphacode]["Inheritance"]
    }
    final_dict.update({orphacode: tmp})

    return orphacode


def raw_extraction(pack_path, encoding):
    final_dict = {}
    for path_file in glob.glob(pack_path, recursive=True):
        if ".xml" in path_file:
            with open(path_file, encoding=encoding) as file:
                xml = xmltodict.parse(file.read())
                xml = xml['JDBOR']['DisorderList']['Disorder']
                for disorder in xml:
                    orpha = disorder['OrphaCode']
                    name = disorder['Name']['#text']

                    status = disorder.get('Totalstatus')
                    if status:
                        status = status["#text"]

                    flag = disorder.get('FlagValue', None)

                    tmpAssociation = [ ] 
                    if "DisorderDisorderAssociationList" in disorder and disorder["DisorderDisorderAssociationList"].get("@count") != "0":
                        if disorder["DisorderDisorderAssociationList"].get("@count") == "1":
                            elt = disorder["DisorderDisorderAssociationList"]["DisorderDisorderAssociation"]
                            tmpAssociation.append({
                                    "TargetDisorder": {
                                        "ORPHAcode": elt["TargetDisorder"].get("OrphaCode", None),
                                        "Preferred term" : elt["TargetDisorder"].get("Name", {}).get("#text")
                                    },
                                    "RootDisorder": { 
                                        "ORPHAcode" : elt["RootDisorder"].get("OrphaCode", None) ,
                                        "Preferred term" : elt["RootDisorder"].get("Name", {}).get("#text")
                                    },
                                    "DisorderDisorderAssociationType" : elt["DisorderDisorderAssociationType"]["Name"]["#text"]
                                })
                        else:
                            for asso in disorder["DisorderDisorderAssociationList"]["DisorderDisorderAssociation"]:
                                tmpAssociation.append({
                                    "TargetDisorder": {
                                        "OrphaCode": elt["TargetDisorder"].get("OrphaCode", None),
                                        "Name" : elt["TargetDisorder"].get("Name", {}).get("#text")
                                    },                                    "RootDisorder": { 
                                        "OrphaCode" : asso["RootDisorder"]["OrphaCode"],
                                        "Name" : asso["RootDisorder"]["Name"]["#text"]
                                    },
                                    "DisorderDisorderAssociationType" : asso["DisorderDisorderAssociationType"]["Name"]["#text"]
                                })
##                          
                    synonyms = disorder.get('SynonymList', None)
                    if synonyms and len(synonyms.keys()) > 1:
                        synonyms = synonyms["Synonym"]
                        if isinstance(synonyms, list):
                            synonyms = [d["#text"] for d in synonyms]
                        else:
                            synonyms = [synonyms["#text"]]
                    else:
                        synonyms = None

                    classif = disorder.get('ClassificationLevel', None)
                    if classif:
                        classif = classif["Name"]["#text"]

                    definition = disorder.get('SummaryInformationList', None)
                    if definition and definition["@count"] == '1': #7204
                        definition = definition.get("SummaryInformation", None)
                        #at least germans can have 0, 1 or more definitions 
                        if definition["TextSectionList"]["@count"] == '0':
                            definition = definition.get("TextAuto", None)
                            if definition:
                                definition = definition["Info"]["#text"]
                        elif definition["TextSectionList"]["@count"] == '1': #6843
                            definition = definition["TextSectionList"]["TextSection"]["Contents"]
                        else: #361
                            definition = definition["TextSectionList"]["TextSection"][0]["Contents"]    
                    else:
                        definition = None

                    aggreg = disorder.get("AggregationLevelSection")
                    if aggreg and aggreg["AggregationLevelList"]["@count"] != "0":
                        #print(aggreg)
                        aggreg = {
                            "AggregationLevel" : [{ 
                                "ORPHAcode" : disorder["AggregationLevelSection"]["AggregationLevelList"]["AggregationLevel"]["OrphaCode"],
                                "Preferred term" : disorder["AggregationLevelSection"]["AggregationLevelList"]["AggregationLevel"]["PreferredTerm"]["#text"],
                                "AggregationLevelStatus" : disorder["AggregationLevelSection"]["AggregationLevelList"]["AggregationLevel"]["AggregationLevelStatus"]
                                }]
                            }

                    ext_ref = disorder.get("ExternalReferenceList", [])
                    if ext_ref:
                        ext_ref = ext_ref["ExternalReference"]
                    refs_array = []
                    if orpha in final_dict:
                        refs_array = final_dict[orpha]["ExternalReference"]
                    if not isinstance(ext_ref, list):
                        ext_ref = [ext_ref]
                    for ref_tmp in ext_ref:
                        reference = ref_tmp["Reference"]
                        source = ref_tmp["Source"]
                        icd11url = ref_tmp.get("DisorderMappingICDRefUrl", None)
                        icd11uri = ref_tmp.get("DisorderMappingICDRefUri", None)
                        ref = { }
                        ref.update({"Reference" : reference})
                        ref.update({"Source" : source})
                        ref.update({"DisorderMappingRelation" : ref_tmp["DisorderMappingRelation"]["Name"]["#text"]})
                        ref.update({"DisorderMappingValidationStatus" : ref_tmp["DisorderMappingValidationStatus"]["Name"]["#text"]})
                        if 'ICD' in source:
                            ref.update({"DisorderMappingICDRelation" : ref_tmp["DisorderMappingICDRelation"]["Name"]["#text"]})
                            #if icd11uri and icd11url:
                            ref.update({"DisorderMappingICDRefUri" : icd11uri,
                                        "DisorderMappingICDRefUrl" : icd11url})
                        refs_array.append(ref)

                    tmp = { }
                    tmp.update({"ORPHAcode" : orpha})
                    tmp.update({"Preferred term" : name})
                    tmp.update({"OrphanetURL" : "https://www.orpha.net/fr/disease/detail/" + orpha})
                    if status:
                        tmp.update({"Status" : status})
                    if flag:
                        tmp.update({"FlagValue" : flag})
                    tmp.update({"Synonym" : synonyms})
                    if classif:
                        tmp.update({"ClassificationLevel" : classif})
                    if definition:
                        tmp.update({"Definition" : definition})
                    if aggreg:
                        tmp.update({"AggregationlevelSection" : aggreg})
                    if tmpAssociation:
                        tmp.update({"DisorderDisorderAssociation": tmpAssociation})
                    tmp.update({"ExternalReference" : refs_array})

                    if orpha in final_dict:
                        final_dict[orpha].update(tmp)
                    else:
                        final_dict[orpha] = tmp
    return final_dict


def dict_format(final_dict):
    for orphacode, elt in final_dict.items():

        elt.update({"Date" : datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")})

        if "ExternalReference" not in elt:
            continue
        for ref in elt["ExternalReference"]:
            if "ICD-10" in ref["Source"]:
                tmp = {
                    "Code ICD10" : ref["Reference"],
                    "DisorderMappingRelation" : ref["DisorderMappingRelation"],
                    "DisorderMappingICDRelation" : ref["DisorderMappingICDRelation"],
                    "DisorderMappingValidationStatus" : ref["DisorderMappingValidationStatus"] 
                }
                if "Code ICD10" in elt:
                    elt["Code ICD10"].append(tmp)
                else:
                    elt.update({"Code ICD10" : [tmp]})
            elif "ICD-11" in ref["Source"]:
                tmp = {
                    "Code ICD11" : ref["Reference"],
                    "DisorderMappingRelation" : ref["DisorderMappingRelation"],
                    "DisorderMappingICDRelation" : ref["DisorderMappingICDRelation"],
                    "DisorderMappingValidationStatus" : ref["DisorderMappingValidationStatus"],
                    "DisorderMappingICDRefUrl" : ref["DisorderMappingICDRefUrl"],
                    "DisorderMappingICDRefUri" : ref ["DisorderMappingICDRefUri"]
                }
                if "Code ICD11" in elt:
                    elt["Code ICD11"].append(tmp)
                else:
                    elt.update({"Code ICD11" : [tmp]})
            elif "SNOMED-CT" in ref["Source"]:
                elt.update({
                    "Code SNOMED-CT" : [
                        {
                            "Code SNOMED-CT" : ref["Reference"],
                            "DisorderMappingRelation" : ref["DisorderMappingRelation"],
                            "DisorderMappingValidationStatus" : ref["DisorderMappingValidationStatus"]
                        }
                    ]
                })
            elif "OMIM" in ref["Source"]:
                tmp = {
                    "Code OMIM" : ref["Reference"],
                    "DisorderMappingRelation" : ref["DisorderMappingRelation"],
                    "DisorderMappingValidationStatus" : ref["DisorderMappingValidationStatus"]
                }
                if "Code OMIM" in elt:
                    elt["Code OMIM"].append(tmp)
                else:
                    elt.update({"Code OMIM" : [tmp]})


def buildData(lang):
    encoding = "UTF-8" if lang in ["cs", "pl", "es", "fr", "nl", "pt", "de", "en"] else "ISO-8859-1" 
    typo_classif_dict = { }
    for path_file in glob.glob(f"../../NomenclaturePack25/Orphanet_Nomenclature_Pack_{lang.upper()}/Classifications/*"):
        with open(path_file, encoding=encoding) as file:
            xml = xmltodict.parse(file.read())
            current_classif = {
                "ID of the classification": xml['JDBOR']["ClassificationList"]["Classification"]["@id"],
                "Name of the classification": xml['JDBOR']["ClassificationList"]["Classification"]["Name"]["#text"],
                "Preferred term": xml['JDBOR']["ClassificationList"]["Classification"]["Name"]["#text"],
                "ORPHAcode": xml['JDBOR']["ClassificationList"]["Classification"]["OrphaNumber"]
            } 
            xml = xml['JDBOR']['ClassificationList']['Classification']['ClassificationNodeRootList']['ClassificationNode']
            parcours_prof(xml, current_classif, typo_classif_dict, None)
    final_dict = raw_extraction(pack_path + lang.upper() + "/*", encoding)
    #
    for k, v in typo_classif_dict.items():
        if k not in final_dict:
            final_dict[k] = { }
        final_dict[k].update({"Typology" : v["Typology"]})
        final_dict[k].update({"Classification" : v["Classification"]})
        final_dict[k].update({"Inheritance" : v["Inheritance"]})
    #
    for k,v in final_dict.items():
        if k in snomed:
            if not "ExternalReference" in final_dict[k]:
                final_dict[k]["ExternalReference"] = []
            final_dict[k]["ExternalReference"].append({"Reference" : snomed[k],
                                   "Source" : "SNOMED-CT",
                                   "DisorderMappingRelation" : relation[lang],
                                   "DisorderMappingValidationStatus" : validation[lang]})    
    dict_format(final_dict)
    return final_dict


# # Creation of indices dictionaries

packorphaIndices = ["ORPHAcode", "Preferred term", "Status", "Synonym", "ClassificationLevel", "Definition", "Typology", "ExternalReference", "Date"]
rdcodeICD10Indices = ["ORPHAcode", "Preferred term", "Synonym", "OrphanetURL", "Date", "Code ICD10"]
rdcodeICD11Indices = ["ORPHAcode", "Preferred term", "Synonym", "OrphanetURL", "Date", "Code ICD11"]
rdcodeOMIMIndices = ["ORPHAcode", "Preferred term", "Synonym", "OrphanetURL", "Code OMIM", "Date"]
rdcodeSNOMEDIndices = ["ORPHAcode", "Preferred term", "Synonym", "OrphanetURL", "Code SNOMED-CT", "Date"]
rdcodeLinearisationIndices = ["ORPHAcode", "Preferred term", "OrphanetURL", "DisorderDisorderAssociation", "Date"] 
rdcodeNomenclatureIndices = ["ORPHAcode", "OrphanetURL", "Preferred term", "FlagValue", "Status", "Synonym", "ClassificationLevel", "Definition", "Typology", "DisorderDisorderAssociation", "AggregationlevelSection", "Date"]
rdcodeClassifIndices = ["ORPHAcode", "Preferred term", "Classification", "Inheritance", "Date"] 

classifList = ["146", "147", "148", "150", "152", "156", "181", "182", "183", "184", "185", "186", "187", "188", "189", 
"193", "194", "195", "196", "197", "198", "199", "200", "201", "202", "203", "204", "205", "209", "212", "216", "231", "233", "235"]

globals()["packorpha_en_product"] = {}

for lang in langs:
    globals()[f"Pack_{lang}"] = buildData(lang)

    globals()[f"rdcode_orpha_icd10_mapping_{lang}"] = {}
    globals()[f"rdcode_orpha_icd11_mapping_{lang}"] = {}
    globals()[f"rdcode_orpha_omim_mapping_{lang}"] = {}
    globals()[f"rdcode_orpha_snomed_mapping_{lang}"] = {}
    globals()[f"rdcode_orphalinearisation_{lang}"] = {}
    globals()[f"rdcode_orphanomenclature_{lang}"] = {}

    for classif in classifList :
        globals()[f"rdcode_orphaclassification_{classif}_{lang}"] = {}

    for (k, v) in globals()[f"Pack_{lang}"].items():
        if lang == "en":
            globals()[f"packorpha_en_product"].update({ k : {x : y for (x, y) in v.items() if x in packorphaIndices}})

        globals()[f"rdcode_orpha_icd10_mapping_{lang}"].update({ k : {x : y for (x, y) in v.items() if x in rdcodeICD10Indices}})
        if ("Code ICD" in globals()[f"rdcode_orpha_icd10_mapping_{lang}"][k]): 
            globals()[f"rdcode_orpha_icd10_mapping_{lang}"][k]["Code ICD"] = globals()[f"rdcode_orpha_icd10_mapping_{lang}"][k].pop("Code ICD10")

        globals()[f"rdcode_orpha_icd11_mapping_{lang}"].update({ k : {x : y for (x, y) in v.items() if x in rdcodeICD11Indices}})
        if ("Code ICD" in globals()[f"rdcode_orpha_icd10_mapping_{lang}"][k]): 
            globals()[f"rdcode_orpha_icd11_mapping_{lang}"][k]["Code ICD"] = globals()[f"rdcode_orpha_icd11_mapping_{lang}"][k].pop("Code ICD11")

        globals()[f"rdcode_orpha_omim_mapping_{lang}"].update({ k : {x : y for (x, y) in v.items() if x in rdcodeOMIMIndices}})

        globals()[f"rdcode_orpha_snomed_mapping_{lang}"].update({ k : {x : y for (x, y) in v.items() if x in rdcodeSNOMEDIndices}})

        globals()[f"rdcode_orphalinearisation_{lang}"].update({ k : {x : y for (x, y) in v.items() if x in rdcodeLinearisationIndices}})

        tmp = {}
        tmp.update({ k : {x : y for (x, y) in v.items() if x in rdcodeNomenclatureIndices}})
        try:
            tmp[k]["DisorderDisorderAssociation"] = \
            [x for x in tmp[k]["DisorderDisorderAssociation"] if x["DisorderDisorderAssociationType"] != "Preferential parent"]
        except:
            tmp[k]["DisorderDisorderAssociation"] = []
        for l,w in tmp.items():
            if "ORPHAcode" in w:
                globals()[f"rdcode_orphanomenclature_{lang}"][l] = w

        #classif
        for classif in classifList:
            #if any(e in v.keys() for e in rdcodeClassifIndices)
            if "Classification" in v and classif in [x["ID of the classification"] for x in v["Classification"]]:
                globals()[f"rdcode_orphaclassification_{classif}_{lang}"].update({ k : {x : y for (x, y) in v.items() if x in rdcodeClassifIndices}})
                globals()[f"rdcode_orphaclassification_{classif}_{lang}"][k]["Classification"] = \
                    [x for x in globals()[f"rdcode_orphaclassification_{classif}_{lang}"][k]["Classification"] if x["ID of the classification"] == classif]
                inheritance = globals()[f"rdcode_orphaclassification_{classif}_{lang}"][k].pop("Inheritance") 
                globals()[f"rdcode_orphaclassification_{classif}_{lang}"][k].update({"Parent" : inheritance[classif]["Parent"]})
                globals()[f"rdcode_orphaclassification_{classif}_{lang}"][k].update({"Child" : inheritance[classif]["Children"]})


# # Indices files creation


if not os.path.exists("./ElasticIndices/"):
    os.mkdir("./ElasticIndices/")
if not os.path.exists("./ElasticIndices/packorpha/"):
    os.mkdir("./ElasticIndices/packorpha/")
if not os.path.exists("./ElasticIndices/rdcode/"):
    os.mkdir("./ElasticIndices/rdcode/")
FileIndex = []

### rdcode_diff

index = f"rdcode_orpha_diff"
index_output = f"ElasticIndices/index_{index}.txt"
es_index = '{"index": {"_index":"' + index + '"}}\n'
with open(index_output, "w", encoding="utf-8") as file:
    for index, row in diff.iterrows():
        file.write(es_index)
        file.write(json.dumps(row.to_dict(), ensure_ascii=False))
        file.write('\n')


for lang in langs:

    ### packorpha_en_product
    if lang == "en":
        index = f"packorpha_en_product"
        index_output = f"ElasticIndices/index_{index}.txt"
        es_index = '{"index": {"_index":"' + index + '"}}\n'
        with open(index_output, "w", encoding="utf-8") as file:
            for local_dico in packorpha_en_product.values():
                file.write(es_index)
                file.write(json.dumps(local_dico, ensure_ascii=False))
                file.write('\n')


    ### rdcode indices
    if not os.path.exists(f"./ElasticIndices/rdcode/rdcode_{lang}/"):
        os.mkdir(f"./ElasticIndices/rdcode/rdcode_{lang}/")
    if not os.path.exists(f"./ElasticIndices/rdcode/rdcode_{lang}/Classifications/"):
        os.mkdir(f"./ElasticIndices/rdcode/rdcode_{lang}/Classifications/")
    ## indices definition

    FileIndex.extend([
    f"rdcode_orpha_icd10_mapping_{lang}",
    f"rdcode_orpha_icd11_mapping_{lang}",
    f"rdcode_orpha_omim_mapping_{lang}",
    f"rdcode_orpha_snomed_mapping_{lang}",
    f"rdcode_orphalinearisation_{lang}",
    f"rdcode_orphanomenclature_{lang}"
    ])

    for file in glob.glob(f"../../NomenclaturePack25/Orphanet_Nomenclature_Pack_{lang.upper()}/Classifications/*"):
        basename = os.path.basename(file)
        FileIndex.append("rdcode_orphaclassification_" + basename.split("_")[1].split("_")[0] + f"_{lang}")

        ## iterates on indices to create them 
for index_output in FileIndex:
    lang = index_output.split("_")[-1]
    #sub_folder = "Classifications/" if "classification" in index_output else ""
    sub_folder = ""
    es_index = '{"index": {"_index":"' + index_output + '"}}\n'
    #with open(f"./ElasticIndices/rdcode_{lang}/{sub_folder}{index_output}.txt", "w", encoding="utf-8") as file:
    with open(f"./ElasticIndices/{index_output}.txt", "w", encoding="utf-8") as file:
        for _, local_dico in globals()[index_output].items():
            file.write(es_index)
            file.write(json.dumps(local_dico, ensure_ascii=False))
            file.write('\n')
        file.close()



# # Injecting indices into Elasticsearch

#packorpha
index_output = "packorpha_en_product"
index = "ElasticIndices/packorpha/index_packorpha_en_product.txt"
try:
    del_req = es_server.indices.delete(index=index_output)
    req = es_server.indices.create(index=index_output, body=body)
except Exception as e:
    print() 
new_array = []
with open(index, "r", encoding="utf-8") as index_final:
    for line in index_final.readlines():
        new_array.append(line)
    new_array.append('\n')
    try:
        res = es_server.bulk(body=''.join(new_array))
    except:
        print("Error on index: " + index)


#rdcode
for index_output in FileIndex:
    lang = index_output.split("_")[-1]
    sub_folder = "Classifications/" if "classification" in index_output else ""
    index = f"./ElasticIndices/rdcode/rdcode_{lang}/{sub_folder}{index_output}.txt"
    try:
        del_req = es_server.indices.delete(index=index_output)
        req = es_server.indices.create(index=index_output, body=body)
    except Exception as e:
        print(e) 
    new_array = []
    with open(index, "r", encoding="utf-8") as index_final:
        for line in index_final.readlines():
            new_array.append(line)
        new_array.append('\n')
        try:
            res = es_server.bulk(body=''.join(new_array))
        except Exception as e:
            print("Error on index: " + index)
            print(e)
    print("Successful injection for: " + index_output)

#rdcode diff
index = "ElasticIndices/index_rdcode_orpha_diff.txt"
index_output = "rdcode_orpha_diff"
try:
    del_req = es_server.indices.delete(index=index_output)
    req = es_server.indices.create(index=index_output, body=body)
except Exception as e:
    print(e) 
new_array = []
with open(index, "r", encoding="utf-8") as index_final:
    for line in index_final.readlines():
        new_array.append(line)
    new_array.append('\n')
    try:
        res = es_server.bulk(body=''.join(new_array))
    except Exception as e:
        print("Error on index: " + index)
        print(e)
