import requests
from requests.auth import HTTPBasicAuth

AIRBYTE_API_URL = "http://localhost:8000/api/v1"
username = "airbyte"
password = "password"


def get_workspaces():
    url = f"{AIRBYTE_API_URL}/workspaces/list"
    response = requests.post(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get workspaces: {response.text}")
        return None


workspaces = get_workspaces()
if workspaces:
    print(workspaces)
