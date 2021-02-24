
from datetime import datetime
from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np
import time
import json


a = pd.DataFrame(np.random.randint(0, 100, size=(1, 2)), columns=list('AB'))
c = pd.DataFrame(np.random.randint(0, 100, size=(1, 2)), columns=list('CD'))
abcd = a.join(c)
print(a)
print(c)
print(abcd)

user = "elastic"
psw = "jjosLBNU9NmTsU5vatFU"
access_url = f"http://{user}:{psw}@localhost:9200/"
es = Elasticsearch(hosts=access_url)
# es.indices.create_data_stream("test-network")
for i in range(1000):
    data = pd.DataFrame(np.random.randint(0, 100, size=(1, 4)), columns=list('ABCD')).to_dict('records')
    # data['@timestamp'] = datetime.utcnow()
    # print(data)
    for d in data:
        d['@timestamp'] = datetime.utcnow()
    print(data)

    res = es.create(index="testing", id=i, body=data[0])
    print(res['result'])
    #
    # res = es.get(index="testing", id=i)
    # print(res['_source'])

    es.indices.refresh(index="testing")

    res = es.search(index="testing", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total']['value'])


    time.sleep(1)
