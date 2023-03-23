#kafka stream consumer user 
from confluent_kafka import Consumer
import json

# define the consumer instance. 
c = Consumer({'bootstrap.servers':'localhost:9092','group.id':'python-consumer','auto.offset.reset':'earliest'})
print('Kafka Consumer Started...')


# show topic list
print('Available topics to consume: ', c.list_topics().topics)

#define topic to subscribe
c.subscribe(['users'])
 
# create loop and define a specific offset:

def main():
    while True:
        msg = c.poll(1.0) #timeout
        if msg is None:
            continue
        if msg.error():
            print('Error: {}'.format(msg.error()))
            continue

        with open('users.json','a') as file:  #'a' append mode
            data = msg.value().decode('utf-8')
            file.write(''.join(data))
            file.write(',')
    c.close()

if __name__ == '__main__':
    main()
