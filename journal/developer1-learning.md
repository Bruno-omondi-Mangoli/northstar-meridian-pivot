# Learning & Blocker Journal — Message Queues

Date: 18/08/2026
Developer: Bruno Omondi Mang'oli
Technology: Message Queues
Start Time: [2100hrs]
Target Completion Time: 0000hrs

## Learning Objective
Understand producer / consumer / queue / message / acknowledgement,
and build a working prototype that moves a fake inventory-update
message from a producer, through a queue, to a consumer.

## Resource Consulted
chatgpt

## What I Learned
A Message Queue (MQ) is a communication mechanism that allows different applications, services, or components to exchange messages asynchronously. Instead of communicating directly, the sender places a message into a queue, and the receiver processes it whenever it is ready.

How it works

+-----------+        Message         +-------------+        Message        +-----------+
| Producer  | ---------------------> | Message     | -------------------> | Consumer  |
| (Sender)  |                        | Queue       |                      | (Receiver)|
+-----------+                        +-------------+                      +-----------+
Producer sends a message.

The message is stored in the queue.

The consumer retrieves and processes the message.

After successful processing, the message is removed from the queue.

Why use a Message Queue?
Message queues provide several benefits:

Asynchronous processing – The sender doesn't have to wait for the receiver.

Decoupling – Producers and consumers don't need to know about each other.

Scalability – Multiple consumers can process messages in parallel.

Reliability – Messages can be persisted until successfully processed.

Load balancing – Work can be distributed among multiple workers.

Real-world example
Imagine an e-commerce website:

A customer places an order.

The order service immediately confirms the order.

Instead of sending emails, updating inventory, and generating invoices synchronously, it sends messages to a queue.

Separate services consume these messages:

Email Service → Sends confirmation email

Inventory Service → Updates stock

Billing Service → Generates invoice

Shipping Service → Starts delivery process

This allows the website to respond quickly even if downstream tasks take time.

Example flow

Customer
    |
    v
Order Service
    |
    +----> Message Queue
             |
      +------+------+------+
      |      |      |      |
      v      v      v      v
   Email  Inventory Billing Shipping
  Service   Service  Service  Service
Common Message Queue Systems
Some popular message queue technologies include:

RabbitMQ – General-purpose message broker using AMQP.

Apache Kafka – Distributed event streaming platform for high-throughput data pipelines.

Amazon SQS – Fully managed message queue service on AWS.

ActiveMQ – Open-source messaging broker supporting multiple protocols.

IBM MQ – Enterprise-grade messaging solution.

Azure Service Bus – Microsoft cloud messaging service.

Queue vs Direct Communication
Direct Communication	Message Queue
Sender waits for receiver	Sender sends and continues
Tightly coupled	Loosely coupled
Failures can block requests	Messages remain in queue until processed
Harder to scale	Easy to scale with multiple consumers

Example
Without a queue:


User -> Order Service -> Email Service
                     -> Inventory Service
                     -> Payment Service
If the Email Service is slow, the entire request may be delayed.

With a queue:


User -> Order Service -> Queue
                         |
                  Worker 1 (Email)
                  Worker 2 (Inventory)
                  Worker 3 (Payment)
The user receives a response immediately, while background workers process the queued tasks.

Summary
A Message Queue is a middleware component that enables applications to exchange messages asynchronously. It improves performance, reliability, scalability, and fault tolerance by allowing producers to send messages without waiting for consumers to process them. It is widely used in microservices, distributed systems, background job processing, and event-driven architectures.

---

## Blocker Log
(add entries below each time you hit a real problem, using this shape:)

### Blocker:
**Exact Error:**
**What I Tried:**
**Result:**
**Next Approach:**
**Final Solution:**
**Why It Worked:**
**Time Spent:**
**Lesson Learned:**