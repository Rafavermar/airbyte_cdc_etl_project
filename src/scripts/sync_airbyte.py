import requests

AIRBYTE_API_URL = "http://localhost:8000/api/v1"
CONNECTION_ID = "Postgres_Local_JSON"


def trigger_sync(connection_id):
    response = requests.post(f"{AIRBYTE_API_URL}/connections/sync", json={"connectionId": connection_id})
    if response.status_code == 200:
        print("Sync triggered successfully!")
    else:
        print("Failed to trigger sync:", response.text)


if __name__ == "__main__":
    trigger_sync(CONNECTION_ID)
