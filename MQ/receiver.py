import pika

login = pika.credentials.PlainCredentials("test","test")
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.76',credentials=login))

channel = connection.channel()
channel.queue_declare(queue='abcd1234')

def callback(ch, method, properties, body):
    print("RECEIVED: {}".format(body))

channel.basic_consume(callback,
                      queue='abcd1234',
                      no_ack=True)

print('WAITING FOR MESSAGE...')
channel.start_consuming()
