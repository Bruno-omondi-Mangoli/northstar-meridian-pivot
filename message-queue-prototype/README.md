# Message Queue Prototype — Northstar Meridian Pivot

Demonstrates a producer/consumer pattern using RabbitMQ, simulating an
inventory-update event moving through a queue.

## Requirements
- Docker Desktop running
- Python 3.11+

## Setup
```bash
docker run -d --hostname my-rabbit --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

## Run
Terminal 1:
```bash
python consumer.py
```

Terminal 2:
```bash
python producer.py
```

Dashboard: http://localhost:15672 (guest/guest)

## What This Demonstrates
- Producer publishes a message without needing a consumer to be listening.
- Consumer processes and acknowledges messages independently.
- Messages persist in the queue if no consumer is connected, and are
  delivered in order once one connects — demonstrated by publishing
  3 messages with no active consumer, then draining all 3 on startup.