#kafka stream users
from confluent_kafka import Producer
import requests
import json
import time 

# define url source and request data
url = 'https://dummyjson.com/users'
response = requests.get(url)

# read and parse the data using json()
users = response.json()
 
# define the producer by specifying the port of Kafka cluster
p = Producer({'bootstrap.servers':'localhost:9092'})
print('Kafka Producer Started...')

# Define a callback function for errors. 
# Valid message will be decoded to utf-8 and printed in the
def receipt(err,msg):
    if err is not None:
        print('Error: {}'.format(err))
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
        print(message)

# Define topic name here
topic_name = 'users'

def main():
    for user in users['users']: # in the json file users there is key namely 'users'
        p.produce(topic_name, json.dumps(user).encode('utf-8'), callback=receipt) # json.dumps(): convert dict to json file
        p.poll(1)
        p.flush()
        time.sleep(2) # suspends execution for 2 sec.

if __name__ == '__main__':
    main()

