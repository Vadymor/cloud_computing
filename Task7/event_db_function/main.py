import base64
import json
import os

from google.cloud.sql.connector import Connector, IPTypes
import pymysql


def connect_with_connector() -> pymysql.connections.Connection:
    """
    Initializes a connection pool for a Cloud SQL instance of MySQL.

    Uses the Cloud SQL Python Connector package.
    """
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.

    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]  # e.g. 'project:region:instance'
    db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    connector = Connector(ip_type)

    conn: pymysql.connections.Connection = connector.connect(
        instance_connection_name,
        "pymysql",
        user=db_user,
        password=db_pass,
        db=db_name,
    )
    return conn


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

    data = json.loads(pubsub_message)

    event_name = data['data']['event_name']
    request_id = data['data']['request_id']
    processed_at = data['data']['processed_at']

    mydb = connect_with_connector()
    mycursor = mydb.cursor()

    mycursor.execute("""CREATE TABLE IF NOT EXISTS events_schema.event(
        event_name varchar(250),
        request_id varchar(250),
        processed_at int
    );""")

    mydb.commit()

    insert_query = "INSERT INTO events_schema.event (event_name, request_id, processed_at) VALUES (%s, %s, %s)"
    insert_val = (event_name, request_id, processed_at)
    mycursor.execute(insert_query, insert_val)

    mydb.commit()

    return f'Success!', 200
