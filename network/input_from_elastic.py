from elasticsearch import Elasticsearch

user="elastic"
psw = "changeme"
access_url = f"http://{user}:{psw}@localhost:9200/"
es = Elasticsearch(hosts=access_url)
# doc = {
#     'author': 'kimchy',
#     'text': 'Elasticsearch: cool. bonsai cool.',
#     'timestamp': 12,
# }
# res = es.index(index="test-index", id=1, body=doc)
# print(res['result'])
# print(2)
#
# res = es.get(index="test-index", id=1)
# print(res['_source'])

try:
    es = Elasticsearch(hosts=[access_url], verify_certs=False, request_timeout=120)
    body = {
      "query": {
        "terms": {
          "_id": ["1"]
        }
      }
    }
    searchRes = es.search(index="hyperparameters", body=body)

except Exception as error:
    print ("Elasticsearch Client Error:", error)


print(searchRes['hits']['hits'][0]["_source"])