import requests
import os
import json


def http_request():

    url = "https://us-central1-centered-motif-229719.cloudfunctions.net/tf_http_triggered_function"

    # generate token
    output_stream = os.popen("gcloud auth print-identity-token")
    token = output_stream.read()[:-1]  # cut th last character, new line delimiter

    headers = {
        "Authorization": f"bearer {token}",
        "Content-Type": "application/json"
    }

    data = json.dumps({
        "event_name": "10_event"
    })

    response = requests.post(url, headers=headers, data=data)

    print(response.text)


if __name__ == '__main__':
    http_request()

