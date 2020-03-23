from datetime import datetime
from elasticsearch import Elasticsearch
import json
from time import sleep
from bs4 import BeautifulSoup
from kafka import KafkaConsumer, KafkaProducer



es = Elasticsearch(["localhost:9200"], http_auth="asamasach:1qaz!QAZ")

if __name__ == '__main__':
    print('Running Consumer..')

    topic_name = 'asamasach_3'
    group_name='asamasach_group'

    #consumer = KafkaConsumer(topic_name,  bootstrap_servers=['localhost:9092'], api_version=(0, 10),auto_offset_reset='earliest',auto_commit_interval_ms=120 * 1000)
    # consumer_timeout_ms=1000 , 
    consumer = KafkaConsumer(topic_name,   bootstrap_servers=['localhost:9092'], api_version=(0, 10),auto_offset_reset='earliest',auto_commit_interval_ms=120 * 1000, value_deserializer=lambda m: json.loads(m.decode('ascii')))

    for msg in consumer:
        value = msg.value
#        value_json=value.decode()
        print("\n")
        print(value)
        print("\n")
        print(str(value))
    #    print(str(json.dumps(value)))
        unique_id=str(datetime.now())
        doc = {
  	    'person': value,
	    'timestamp': datetime.now()
              }
        res = es.index(index="asamasach", id=unique_id, body=doc)
        print("\n")
        print(res['result'])
        res = es.get(index="asamasach", id=unique_id)
        print("\n")
        print(res['_source'])
        es.indices.refresh(index="asamasach")
    #consumer.commit()
    consumer.close()
    sleep(1)
