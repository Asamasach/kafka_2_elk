from kafka import KafkaProducer
from kafka.errors import KafkaError
import json 
from faker import Faker
import random
from random import randint
import msgpack
import logging
#from bson import json_util

#producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Asynchronous by default
fake = Faker('en_US')


producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
#producer.send('asamasach', {'key': 'value'})
#print("json_sent")

#producer = KafkaProducer(value_serializer=msgpack.dumps)
for _ in range(10):
    my_dict = {  'first_name': fake.first_name(), 'last_name': fake.last_name(), 'age': randint(0, 100)   } 
    print(str(my_dict))
    print("\n")
#    print(bytes(my_dict, 'utf-8'))
#    my_dict_encoded=str(my_dict)
    future = producer.send('asamasach_3', my_dict)
#    future = producer.send('asamasach', json.dumps( my_dict, default=json_util).encode('utf-8'))
# Block for 'synchronous' sends
try:
    record_metadata = future.get(timeout=10)
except KafkaError:
    # Decide what to do if produce request failed...
    log.exception()
    pass

# Successful result returns assigned partition and offset
print (record_metadata.topic)
print (record_metadata.partition)
print (record_metadata.offset)
