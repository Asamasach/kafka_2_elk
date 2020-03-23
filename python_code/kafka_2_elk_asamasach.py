from datetime import datetime
from elasticsearch import Elasticsearch
import json
from time import sleep
from kafka import KafkaConsumer
#connect to elasticsearch container
es = Elasticsearch(["elasticsearch"], http_auth="asamasach:1qaz!QAZ",timeout=30, max_retries=10, retry_on_timeout=True)

if __name__ == '__main__':
    print('Running Consumer..')
	#topic name which created in kafkaproduce code
    topic_name = 'asamasach_3'
 	#consume messages in kafka continer and chech the elasticsearch connection
    consumer = KafkaConsumer(topic_name,   bootstrap_servers=['kafka:9093'], api_version=(0, 10),auto_offset_reset='earliest',auto_commit_interval_ms=120 * 1000, value_deserializer=lambda m: json.loads(m.decode('ascii')))
    print(es.info())
    for msg in consumer:
        value = msg.value
        print("\n"+str(value)+"\n") #show the values in topic
        unique_id=str(datetime.now()) #create a unique id for elasticsearch
        doc = {
  	    'person': value,
	    'timestamp': datetime.now()
              }
    
        res = es.index(index="asamasach", id=unique_id, body=doc) #add documnets in elasticsearch, in index named "asamasach"
        print("\n")
        print(res['result']) #show the result of creation, if done print created
        es.indices.refresh(index="asamasach") # refresh index
    sleep(1) #wait for next data (it can be eliminated)
