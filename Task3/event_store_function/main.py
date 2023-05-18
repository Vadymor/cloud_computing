import base64
from google.cloud import storage
import json


def upload_blob(bucket_name, blob_text, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(blob_text)

    print(f'File uploaded to {destination_blob_name}')


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

    data = json.loads(pubsub_message)

    BUCKET_NAME = 'tf_events_storage'
    BLOB_NAME = data['data']['request_id'] + '_' + str(data['data']['processed_at']) + '.json'
    BLOB_STR = json.dumps(data)

    upload_blob(BUCKET_NAME, BLOB_STR, BLOB_NAME)
    return f'Success!', 200
