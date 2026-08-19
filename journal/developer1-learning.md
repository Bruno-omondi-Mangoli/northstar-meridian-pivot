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

### Blocker: Docker CLI can't connect to Docker daemon
**Exact Error:** failed to connect to the docker API at npipe:////./pipe/docker_engine...
**What I Tried:** ran `docker run` directly
**Result:** connection error — daemon not reachable
**Next Approach:** waited / Docker Desktop finished starting, retried the same command
**Final Solution:** re-ran `docker run` after Docker Desktop was fully up
**Why It Worked:** the Docker CLI needs the Docker Desktop background service (daemon) running first — it wasn't ready yet on the first attempt
**Time Spent:** [fill in]
**Lesson Learned:** always confirm Docker Desktop is fully started (steady whale icon) before running docker commands, not just installed

## What I Learned
- A connection opens a link to the RabbitMQ server; a channel is a lightweight
  pathway within that connection where actual work (declaring queues, sending
  messages) happens.
- queue_declare() is idempotent - safe to call every run, it won't duplicate
  an existing queue.
- basic_publish() with exchange='' routes directly to the queue named in
  routing_key - the simplest routing mode RabbitMQ supports.
- Messages must be sent as text/bytes, not Python objects - json.dumps()
  converts the dictionary into a string RabbitMQ can carry.
- Producer and consumer never talk to each other directly - they're only
  connected by both declaring the same queue name.

## Resource Consulted
- Built producer.py with AI assistant guidance, line-by-line explanation
- Verified against RabbitMQ concepts (connection/channel/queue) explained
  by assistant before writing code

  ### Blocker: RabbitMQ dashboard login rejected
**Exact Error:** Not_Authorized / HTTP access denied: user 'mangolibruno@gmail.com' - invalid credentials
**What I Tried:** logged in at localhost:15672
**Result:** rejected
**Next Approach:** checked docker logs rabbitmq --tail 50, found browser had
  auto-filled my email instead of the default 'guest' credentials
**Final Solution:** manually cleared both fields and typed guest/guest directly
**Why It Worked:** browser autofill was substituting saved email/password
  credentials instead of RabbitMQ's actual default guest account
**Lesson Learned:** docker logs is the right first place to check when a
  service behaves unexpectedly - it showed the real cause immediately,
  and confirmed my actual producer/consumer scripts were authenticating
  correctly the whole time, so the queue logic itself was never broken
  **Confirmed Fixed:** dashboard now shows Overview with Connections: 1,
Channels: 1, Queues: 1, Consumers: 1 - matches consumer.py still running
from the terminal

## What I Learned (continued)
- RabbitMQ queues persist messages even when no consumer is connected -
  producer and consumer are decoupled in TIME, not just in code structure.
- Demonstrated this by running producer.py multiple times across the
  session without a consumer always active; when consumer.py started,
  it immediately drained all 3 backlogged messages in order.
- This is the core reliability advantage over a direct function call:
  if the receiving service is temporarily down, messages aren't lost,
  they simply wait.

  Target Completion Time: 0106hrs
## Definition of Done
A producer script publishes a fake inventory-update message to a RabbitMQ
queue; a consumer script, running independently, receives and acknowledges
that message; messages persist in the queue when no consumer is active and
are delivered in order once a consumer connects, demonstrated by publishing
3 messages with no consumer running and confirming all 3 were drained on
consumer startup.

## Known Limitations
- Single queue, single consumer - no demonstration of multiple consumers
  sharing load (a real production setup might run several consumer
  instances for scaling).
- No explicit failure-handling test (e.g. consumer crashing mid-message,
  message requeueing via basic_nack) - acknowledgement was demonstrated
  on the success path only.
- Credentials (guest/guest) are RabbitMQ's local defaults, not suitable
  for any real deployment.

## Time Spent
0506hrs

## What I Would Do Differently
pick RabbitMQ again 