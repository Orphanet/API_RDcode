import pandas as pd
import elasticsearch as es
import xmltodict
import requests
import json
import datetime
import os
import glob

elastic_server = es.Elasticsearch("http://localhost:9200")
body = json.dumps({
  "mappings": {
    "properties": {
      "ExternalReference" : {
        "type": "nested"
      }
    }
  }
})

### SETTINGS FOR DATA PROCESSING - ELASTICSEARCH INJECTION - FILE INPUTS AND OUTPUTS ### 
# The paths SHOULD be modified before use.  #

pack_path = "Orphanet_Nomenclature_Pack_en/ORPHA_ICD11_mapping_en_newversion.xml"
base_path = "../../"
indices_output = base_path + "indices.txt"
path_file = base_path + pack_path

xml_classif_array = []
final_dicts = {}
classif_dicts = {}

inactiv_codes = ["513", "8208", "8225", "8449"]

# Delete and create indices

index = "rdcode_orpha_icd11_mapping_en"
try:
    del_req = elastic_server.indices.delete(index=index)
except:
    print("No index")
req = elastic_server.indices.create(index=index, body=body)
print(req)

# Actual processing 

with open(path_file, encoding='ISO-8859-1') as file:
    xml = xmltodict.parse(file.read())
    xml = xml['JDBOR']['DisorderList']['Disorder']
    for disorder in xml:
        orpha = disorder['OrphaCode']
        name = disorder['Name']['#text']
        synonyms = disorder.get('SynonymList', None)
        if synonyms and len(synonyms.keys()) > 1:
            synonyms = synonyms["Synonym"]
            if isinstance(synonyms, list):
                synonyms = [d["#text"] for d in synonyms]
            else:
                synonyms = synonyms["#text"]
        else:
            synonyms = None
        ext_ref = disorder.get("ExternalReferenceList", [])
        if ext_ref:
            ext_ref = ext_ref["ExternalReference"]
        refs_array = []
        if not isinstance(ext_ref, list):
            ext_ref = [ext_ref]
        for ref_tmp in ext_ref:
            ref = { }
            ref.update({"Code ICD11" : ref_tmp["Reference"]})
            ref.update({"DisorderMappingRelation" : ref_tmp["DisorderMappingRelation"]["Name"]["#text"]})
            ref.update({"DisorderMappingValidationStatus" : ref_tmp["DisorderMappingValidationStatus"]["Name"]["#text"]})
            ref.update({"DisorderMappingICDRelation" : ref_tmp["DisorderMappingICDRelation"]["Name"]["#text"]})
            ref.update({"DisorderMappingICDRefUrl" : ref_tmp["DisorderMappingICDRefUrl"]})
            ref.update({"DisorderMappingICDRefUri" : ref_tmp["DisorderMappingICDRefUri"]})
            refs_array.append(ref)
        tmp = { }
        tmp.update({"ORPHAcode" : orpha})
        tmp.update({"Preferred term" : name})
        tmp.update({"Synonym" : synonyms})
        tmp.update({"References" : refs_array})
        tmp.update({"Date" : datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")})         
        final_dicts.update({orpha : tmp})

# Elastic Index Creation    

index = '{"index": {"_index":"rdcode_orpha_icd11_mapping_en"}}\n'
with open(f"indices_en.txt", "w", encoding="utf-8") as file:
    for k,v in final_dicts.items():
        file.write(index)
        file.write(json.dumps(v, ensure_ascii=False))
        file.write("\n")

# Elastic Array Injection

new_array = []
with open("indices_en.txt", "r", encoding="utf-8") as index_final:
    for line in index_final.readlines():
        new_array.append(line)
    new_array.append('\n')
    res = elastic_server.bulk(body=''.join(new_array))
    if res["errors"]:
        print("At least one error happened, check server response:")
        print(res)
    else:
        print("No error")