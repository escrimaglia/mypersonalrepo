# RabbitMQ on Docker

## Implementing the Producer/Consumer Pattern in Python 3.12

RabbitMQ is one of the most well-known message brokers for implementing the Producer/Consumer pattern.

Others include Kafka, Redis, ActiveMQ, Python Message Service, etc.

### Run the following command to create the container (requires Docker and the Pika library to be installed)

docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management

- `-d`: Runs the container in detached mode (in the background).
- `--name rabbitmq`: Names the container "rabbitmq" for easy identification.
- `-p 5672:5672`: Exposes RabbitMQ's standard port for the AMQP protocol (messaging port).
- `-p 15672:15672`: Exposes port 15672 for RabbitMQ's web management interface.
- `rabbitmq:management`: Official RabbitMQ image.

### Access the RabbitMQ Management Portal

Visit: [http://localhost:15672](http://localhost:15672)

Default credentials to log into the management portal:

- Username: guest  
- Password: guest

### Run the Consumer in One Terminal

python3 consumidor.py


### Run the Producer in Another Terminal

python3 productor.py
