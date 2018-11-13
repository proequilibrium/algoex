import pika
import time

login = pika.credentials.PlainCredentials("test","test")
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.76',credentials=login))

channel = connection.channel()
channel.queue_declare(queue='abcd123', durable=True)

def callback(ch, method, properties, body):
    print(" [x] RECEIVED %r" % body)
    time.sleep(body.count(b'.'))
    print(" [x] Done")

channel.basic_consume(callback,
                      queue='abcd123',
                      no_ack=True)

print('WAITING FOR MESSAGE...')
channel.start_consuming()
