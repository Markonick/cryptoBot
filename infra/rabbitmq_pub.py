#!/usr/bin/env python
import abc
import pika
import sys

class IPublisher(abc.ABC):       
    @abc.abstractmethod 
    async def publish(self, data: dict) -> None:
        pass

class RabbitmqPublisher(IPublisher):
    """
    RabbitMQ implementation of IPublisher 
    """
    def __init__(self, config):
        self.config = config

    def publish(self, routing_key, message):       
       connection = self._create_connection()

       # Create a new channel with the next available channel number or pass in a channel number to use
       channel = connection.channel()

       # Creates an exchange if it does not already exist, and if the exchange exists,
       # verifies that it is of the correct and expected class. 
       channel.exchange_declare(exchange=self.config['exchange'], exchange_type='topic')
       
       #Publishes message to the exchange with the given routing key
       channel.basic_publish(exchange=self.config['exchange'], routing_key=routing_key, body=message)
       print(f"[x] Sent message {message} for {routing_key}")

    # Create new connection
    def _create_connection(self):
        param = pika.ConnectionParameters(host=self.config['host'], port=self.config['port']) 
        return pika.BlockingConnection(param)