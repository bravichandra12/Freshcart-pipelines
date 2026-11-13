import pika
import sys
import json

AMQP_URL = "amqp://guest:guest@localhost:5672/"
EXCHANGE = "rapido-dispatch"

def main():
    name = sys.argv[1]
    pattern = sys.argv[2]

    conn = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type='topic')

    result = ch.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    ch.queue_bind(exchange=EXCHANGE, queue=queue_name, routing_key=pattern)
    
    print(f"[{name}] waiting for messages matching '{pattern}'...")

    def callback(ch, method, properties, body):
        msg = json.loads(body)
        
        # Part D3 Logic: Validate data quality and ACK/NACK
        if "zone" not in msg:
            print(f"[{name}] ERROR: Missing 'zone'. Rejecting message: {msg}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        else:
            print(f"[{name}] Accepted: {msg}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    ch.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=False
    )
    
    ch.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass