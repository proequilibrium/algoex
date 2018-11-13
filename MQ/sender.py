import pika
import sys

login = pika.credentials.PlainCredentials("test","test")
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.76',credentials=login))
channel = connection.channel()

message = ' '.join(sys.argv[1:]) or "Sender runned withnout input"

channel.queue_declare(queue='abcd123')

channel.basic_publish(exchange='',
                      routing_key='abcd123',
                      body=message)

print('Odeslano: {}'.format(message))

connection.close()
