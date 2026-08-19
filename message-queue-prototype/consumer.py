import pika
import json

# 1. Connect to RabbitMQ, same as the producer
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Declare the same queue (safe even if it already exists)
channel.queue_declare(queue='inventory_updates')

# 3. Define what happens when a message arrives
def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f" [x] Received {message}")

    # Simulate processing the inventory update
    print(f"     Processing update for {message['product_id']}: quantity = {message['quantity']}")

    # Acknowledge the message - tells RabbitMQ "I'm done, you can delete it"
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"     Acknowledged.")

# 4. Tell RabbitMQ to call our callback function for each message
channel.basic_consume(queue='inventory_updates', on_message_callback=callback)

print(' [*] Waiting for messages. Press CTRL+C to exit.')
channel.start_consuming()