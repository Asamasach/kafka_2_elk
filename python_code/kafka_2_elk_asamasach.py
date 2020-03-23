from datetime import datetime
from elasticsearch import Elasticsearch
import json
from time import sleep
from kafka import KafkaConsumer

es = Elasticsearch(["elasticsearch"], http_auth="asamasach:1qaz!QAZ",timeout=30, max_retries=10, retry_on_timeout=True)

if __name__ == '__main__':
    print('Running Consumer..')

    topic_name = 'asamasach_3'
 
    consumer = KafkaConsumer(topic_name,   bootstrap_servers=['kafka:9093'], api_version=(0, 10),auto_offset_reset='earliest',auto_commit_interval_ms=120 * 1000, value_deserializer=lambda m: json.loads(m.decode('ascii')))
    print(es.info())
    for msg in consumer:
        value = msg.value
        print("\n"+str(value)+"\n")
        unique_id=str(datetime.now())
        doc = {
  	    'person': value,
	    'timestamp': datetime.now()
              }
    
        res = es.index(index="asamasach", id=unique_id, body=doc)
        print("\n")
        print(res['result'])
        #res = es.get(index="asamasach", id=unique_id)
        #print("\n")
        #print(res['_id'])
        es.indices.refresh(index="asamasach")
    #consumer.close()
    sleep(1)
