import requests
import os
import json


url = "https://us-central1-centered-motif-229719.cloudfunctions.net/http_triggered_function"

output_stream = os.popen("gcloud auth print-identity-token")
token = output_stream.read()

headers = {
    "Authorization": f"bearer {token[:-1]}",
    "Content-Type": "application/json"
}

data = json.dumps({
    "event_name": "20_event"
})

response = requests.post(url, headers=headers, data=data)

print(response.text)

