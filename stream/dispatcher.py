import pika
import json
import time
import random
import uuid
from datetime import datetime, timezone

AMQP_URL = "amqp://guest:guest@localhost:5672/"
EXCHANGE = "rapido-dispatch"

def main():
    conn = pika.BlockingConnection(pika.URLParameters(AMQP_URL))
    ch = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type='topic')

    cities = ["bangalore", "chennai"]
    zones = ["koramangala", "indiranagar", "whitefield", "tnagar"]
    types = ["ride", "food"]

    print("Starting dispatcher... (Sending 15 messages, injecting bad data every 5th msg)")
    
    count = 1
    for _ in range(15):
        city = random.choice(cities)
        zone = random.choice(zones)
        req_type = random.choice(types)
        routing_key = f"{city}.{zone}.{req_type}"

        msg = {
            "id": str(uuid.uuid4())[:8],
            "city": city,
            "zone": zone,
            "type": req_type,
            "ts": datetime.now(timezone.utc).isoformat()
        }

        # Part D3 Logic: Inject a bad message every 5th iteration for a quicker demo
        if count % 5 == 0:
            del msg["zone"]
            routing_key = f"bangalore.missing.{req_type}"
            print(f"[x] Dispatcher sent BAD MESSAGE: {routing_key}")
        else:
            print(f"[x] Dispatcher sent: {routing_key}")

        ch.basic_publish(
            exchange=EXCHANGE,
            routing_key=routing_key,
            body=json.dumps(msg)
        )
        
        count += 1
        time.sleep(1)
        
    conn.close()

if __name__ == "__main__":
    main()