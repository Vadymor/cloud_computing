import base64
import uuid
import json
import os
import time
from google.cloud import pubsub_v1
from flask import Request

publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.getenv('My Project 20110')


def http_triggered_function(request: Request):

    data = request.data

    if data is None:
        print('Request is empty')
        return 'Request is empty', 400

    print(f"Request data: {data}")

    data_json = json.loads(data)
    event_name = data_json['event_name']

    request_id = str(uuid.uuid4())
    timestamp = int(time.time())

    topic_path = 'projects/centered-motif-229719/topics/event-stream'

    message_json = json.dumps({
        "data": {
            "event_name": event_name,
            "request_id": request_id,
            "processed_at": timestamp
        }
    })

    message_bytes = message_json.encode('utf-8')

    try:
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()
    except Exception as e:
        print(e)
        return e, 500

    return 'Message received and published to Pub/Sub', 200
