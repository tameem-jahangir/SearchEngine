import requests
import json
from connection import estf
import pprint
data = {
"search_request": {
    '_source':['title', 'extract'],
    "query": {"match" : { "extract": "airport" }},
  },
  "query_hint": "airport",
  "field_mapping": {
    "title": ["_source.title"],
    "content": ["_source.text_entry"]
  },
  "algorithm": "Bisecting K-Means"
 } 
  

#response = requests.post('http://localhost:9200/our-index/_search_with_clusters', data=data)

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".

# response = es.transport.perform_request(method='POST',url='http://localhost:9200/our-index/_search_with_clusters', body=json.dumps(data))


response = requests.post('http://localhost:9200/our-index/_search_with_clusters?pretty', data=json.dumps(data), headers= {
    'Content-Type': 'application/json'
  })
result =response.text
d = json.loads(result)

# pprint.pprint(d)
print([cluster['phrases'][:2] for cluster in d["clusters"]])
