# Consumer
# By Ed Scrimaglia

import pika
import subprocess

def publish_message(message, queue_name='cola_test', host='localhost'):
    
    connection_parameters = pika.ConnectionParameters(host)
    with pika.BlockingConnection(connection_parameters) as connection:
        channel = connection.channel()

        channel.queue_declare(queue=queue_name)

        channel.basic_publish(exchange='', routing_key=queue_name, body=message)
        print(f" [x] Sent '{message}'")


if __name__ == "__main__":
    cmd = 'ls -l'
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
    output, err = proc.communicate()
    publish_message(output)
