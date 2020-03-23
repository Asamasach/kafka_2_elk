from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch(["localhost:9200"], http_auth="asamasach:1qaz!QAZ")

doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
}
res = es.index(index="asamasach", id=1, body=doc)
print(res['result'])

res = es.get(index="asamasach", id=1)
print(res['_source'])

es.indices.refresh(index="asamasach")

res = es.search(index="asamasach", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for hit in res['hits']['hits']:
    print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
