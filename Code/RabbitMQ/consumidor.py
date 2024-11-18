# Consumer
# By Ed Scrimaglia

import pika

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")

def consume_messages():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='cola_test')

        channel.basic_consume(queue='cola_test', on_message_callback=callback, auto_ack=True)

        print(' [*] Leyendo cola en RabbitMQ. To exit press CTRL+C')
        
        channel.start_consuming()
    except (Exception, KeyboardInterrupt) as err:
        print (err)

if __name__ == "__main__":
    consume_messages()
