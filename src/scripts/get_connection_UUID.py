import requests
from requests.auth import HTTPBasicAuth

AIRBYTE_API_URL = "http://localhost:8000/api/v1"
username = "airbyte"
password = "password"
workspace_id = "bf3ce332-3248-4da8-91fe-0f63f824e037"  # Reemplaza con el ID de tu workspace


def get_connections(workspace_id):
    url = f"{AIRBYTE_API_URL}/connections/list"
    payload = {
        "workspaceId": workspace_id
    }
    response = requests.post(url, json=payload, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get connections: {response.text}")
        return None


connections = get_connections(workspace_id)
if connections:
    print(connections)
