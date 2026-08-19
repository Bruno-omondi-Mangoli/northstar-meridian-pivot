import pika
import json

# 1. Connect to RabbitMQ running on localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. Declare the queue (creates it if it doesn't exist yet)
channel.queue_declare(queue='inventory_updates')

# 3. Build a fake inventory update message
message = {
    "product_id": "SKU-1001",
    "quantity": 18,
    "event": "inventory.updated"
}

# 4. Publish the message to the queue
channel.basic_publish(
    exchange='',
    routing_key='inventory_updates',
    body=json.dumps(message)
)

print(f" [x] Sent {message}")

# 5. Close the connection cleanly
connection.close()