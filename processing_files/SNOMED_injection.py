import pandas as pd
import elasticsearch as es
import xmltodict
import requests
import json
import datetime
import os
import glob

langs = ["CS", "DE", "EN", "ES", "FR", "IT", "NL", "PL", "PT"]

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


# API call wrapper

def api_call_wrapper(URL):
    response = requests.get(URL, headers={"apiKey": "akey"})
    if 400 <= response.status_code < 600:
        return {'data': [] }
    response = response.json()
    if "Endpoint" in response:
        response.update({"Endpoint" : URL.split("/")[-1]})
    return response    


# Import data

df = pd.read_excel("ORPHA-SNOMEDCT_Mapping_File_production.xlsx", skiprows=[1, 2])
snomed = df.astype(str).set_index(df.columns[0])["Unnamed: 2"].to_dict()


# Delete and create indices

for lang in langs:
    index = "rdcode_orpha_snomed_mapping_{}".format(lang.lower())
    try:
        del_req = elastic_server.indices.delete(index=index)
    except:
        print("No index")
    req = elastic_server.indices.create(index=index, body=body)
    print(req)


## If entities files have not been loaded yet 

if not os.path.exists("entities_FR.txt"):

    # Get all entities per language

    for lang in langs:
        res = api_call_wrapper(f"https://api.orphacode.org/{lang}/ClinicalEntity")
        with open(f"entities_{lang}.txt", "w") as file:
            json.dump(res, file)


# Load pack in all languages

entities = {}
with open(f"entities_CS.txt", "r", encoding="utf-8") as file:
    entities["CS"] = json.load(file)
with open(f"entities_DE.txt", "r", encoding="utf-8") as file:
    entities["DE"] = json.load(file)
with open(f"entities_EN.txt", "r", encoding="utf-8") as file:
    entities["EN"] = json.load(file)
with open(f"entities_ES.txt", "r", encoding="utf-8") as file:
    entities["ES"] = json.load(file)
with open(f"entities_FR.txt", "r", encoding="utf-8") as file:
    entities["FR"] = json.load(file)
with open(f"entities_IT.txt", "r", encoding="utf-8") as file:
    entities["IT"] = json.load(file)
with open(f"entities_NL.txt", "r", encoding="utf-8") as file:
    entities["NL"] = json.load(file)
with open(f"entities_PL.txt", "r", encoding="utf-8") as file:
    entities["PL"] = json.load(file)
with open(f"entities_PT.txt", "r", encoding="utf-8") as file:
    entities["PT"] = json.load(file)

def entity_search(array, orphacode):
    for entity in array:
        if str(entity["ORPHAcode"]) == orphacode:
            return {"Preferred term": entity["Preferred term"]}


# Documents array Creation

for lang in langs:
    print("Current Loop Language: " + lang)
    final_array = []
    for (orphacode, snomedcode) in snomed.items():
        current = entity_search(entities[lang], orphacode)
        url = "http://www.orpha.net/consor/cgi-bin/OC_Exp.php?lng=fr&Expert=" + orphacode
        references = [{
            "Code SNOMED-CT": snomedcode,
            "DisorderMappingValidationStatus": "Validated",
            "DisorderMappingRelation": "E (Exact Mapping)" 
        }]
        current.update({
            "ORPHAcode" : orphacode,
            "OrphanetURL" : url,
            "References" : references,
            "Date" : datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        })
        final_array.append(current)

    # Elastic Index Creation    

    index = '{"index": {"_index":"rdcode_orpha_snomed_mapping_' + lang.lower() + '"}}\n'
    with open(f"indices_{lang.lower()}.txt", "w", encoding="utf-8") as file:
        for entity in final_array:
            file.write(index)
            file.write(json.dumps(entity))
            file.write("\n")

    # Elastic Array Injection
    
    new_array = []
    with open("indices_{}.txt".format(lang.lower()), "r", encoding="utf-8") as index_final:
        for line in index_final.readlines():
            new_array.append(line)
        new_array.append('\n')
        res = elastic_server.bulk(body=''.join(new_array))
        if res["errors"]:
            print("At least one error happened, check server response:")
            print(res)
        else:
            print("No error for {}".format(lang.lower()))

# Deletes used files

for file in glob.glob("*.txt"):
    os.remove(file)
