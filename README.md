# dDeliver json objects from kafka to elasticsearch using python
---
1. clone the repository in your desire folder using `git clone https://github.com/Asamasach/kafka_2_elk.git` (install git beforehand)
2. be sure that, map memory size in host machine is set to your desire value, for instance running below command as root user, can temproraley increase mmapfs for it: `sysctl -w vm.max_map_count=262145`
and for permanent soultion, change the setting in `/etc/sysctl.conf`
3. run `docker-compose up -d` to build and start all containers, which contains:
    - elasticsearch on port 9200
    - kibana on port 5601 to visualize data easily
    - nginx on port 80 which proxy_pass kibana to have public access to dashboards ( in my case I use kibana.asamasach.ir as a subdomain for this service, you can change it in ./nginx/nginx.conf file)
    - kafka as log broker on port 9092
    - zookeeper as cordiantor on port 2181
    - kafka to elasticsearch deliver python container
4. inside elasticsearch create an index by using development tools as below, and then press run key:
`PUT /asamasach
{
    "settings" : {
        "number_of_shards" : 2
        , "number_of_replicas": 2
    },
    "mappings" : {
        "properties" : {
            "person" : { "type" : "object" },
            "timestamp" : { "type" : "date" }
        }
    }
}`
5. for testing the data line, run python_test_producer.py, which create 10 random json object by using `python3 python_test_producer.py`

----
##having done steps, you can check discover menu in kibana to be sure that data deliver correctly 
