from elasticsearch import Elasticsearch

user="elastic"
psw = "changeme"
access_url = f"http://{user}:{psw}@localhost:9200/"
es = Elasticsearch(hosts=access_url)


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