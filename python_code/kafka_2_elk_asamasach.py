from datetime import datetime
from elasticsearch import Elasticsearch
import json
from time import sleep
from kafka import KafkaConsumer
import unittest2

#connect to elasticsearch container
es = Elasticsearch(["elasticsearch"], http_auth="asamasach:1qaz!QAZ",timeout=30, max_retries=10, retry_on_timeout=True)

test_c=unittest2.TestCase('__init__') #for testing

if __name__ == '__main__':
    print('Running Consumer..')
	#topic name which created in kafkaproduce code
    topic_name = 'asamasach_3'
 	#consume messages in kafka continer and chech the elasticsearch connection
    consumer = KafkaConsumer(topic_name,   bootstrap_servers=['kafka:9093'], api_version=(0, 10),auto_offset_reset='earliest',auto_commit_interval_ms=120 * 1000, value_deserializer=lambda m: json.loads(m.decode('ascii')))
    print(es.info())
    a=0
    b=0
    for msg in consumer:
	a+=1 #count number of masseges
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
	if (str(res['result'])=="created"): 
            b+=1 #count number of object sent to elasticsearch
        es.indices.refresh(index="asamasach") # refresh index
    try:
        test_c.assertEqual(a,b), "the quantity of messages conusumed arent equal to messages sent to elasticsearch!"
    except AssertionError:
        logging.basicConfig(filename='kafka_2_elk.log', filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.info('the number of kafka messages conusumed arent equal sent elk!')
        pass
    sleep(1) #wait for next data (it can be eliminated)
