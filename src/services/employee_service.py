import time

import requests
from requests.auth import HTTPBasicAuth

from src.db.employee_repository import EmployeeRepository
from src.db.connection import DatabaseConnection

AIRBYTE_API_URL = "http://localhost:8000/api/v1"
CONNECTION_ID = "7b763e99-b964-4d99-a26c-5c92c1ae12da"


class EmployeeService:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def is_sync_running(self):
        url = f"{AIRBYTE_API_URL}/jobs/list"
        username = "airbyte"
        password = "password"

        payload = {
            "configTypes": ["sync"],
            "configId": CONNECTION_ID,
            "pagination": {
                "pageSize": 1,
                "rowOffset": 0
            }
        }

        response = requests.post(url, json=payload, auth=HTTPBasicAuth(username, password))

        if response.status_code == 200:
            jobs = response.json().get('jobs', [])
            if jobs:
                status = jobs[0].get('status')
                return status in ("running", "pending")
            return False
        else:
            print(f"Failed to check sync status: {response.text}")
            return False

    def wait_for_sync_to_complete(self):
        while self.is_sync_running():
            print("Waiting for the current sync to complete...")
            time.sleep(50)

    def trigger_sync(self):
        self.wait_for_sync_to_complete()

        url = f"{AIRBYTE_API_URL}/connections/sync"
        username = "airbyte"
        password = "password"

        payload = {
            "connectionId": CONNECTION_ID
        }

        response = requests.post(url, json=payload, auth=HTTPBasicAuth(username, password))

        if response.status_code == 200:
            print("Sync triggered successfully")
            self.wait_for_sync_to_complete()  # Wait for the sync to complete before returning
        else:
            print(f"Failed to trigger sync: {response.text}")

    def get_all_employees(self):
        with self.db_connection as connection:
            repository = EmployeeRepository(connection)
            return repository.get_all_employees()

    def add_employee(self, name, position, salary):
        with self.db_connection as connection:
            repository = EmployeeRepository(connection)
            repository.add_employee(name, position, salary)
        self.trigger_sync()

    def update_employee_salary(self, employee_id, new_salary):
        with self.db_connection as connection:
            repository = EmployeeRepository(connection)
            repository.update_employee_salary(employee_id, new_salary)
        self.trigger_sync()

    def delete_employee(self, employee_id):
        with self.db_connection as connection:
            repository = EmployeeRepository(connection)
            repository.delete_employee(employee_id)
        self.trigger_sync()