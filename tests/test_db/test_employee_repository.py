import unittest
from src.db.connection import DatabaseConnection
from src.db.employee_repository import EmployeeRepository


class TestEmployeeRepository(unittest.TestCase):
    def setUp(self):
        self.db_connection = DatabaseConnection()
        with self.db_connection as connection:
            self.repository = EmployeeRepository(connection)

    def test_add_employee(self):
        with self.db_connection as connection:
            self.repository.add_employee('John Doe', 'Software Engineer', 70000)
            employees = self.repository.get_all_employees()
            self.assertTrue(any(emp[1] == 'John Doe' for emp in employees))

    def test_update_employee_salary(self):
        with self.db_connection as connection:
            self.repository.add_employee('Jane Doe', 'Data Scientist', 80000)
            employees = self.repository.get_all_employees()
            employee_id = next(emp[0] for emp in employees if emp[1] == 'Jane Doe')
            self.repository.update_employee_salary(employee_id, 85000)
            updated_employee = self.repository.get_all_employees()
            self.assertTrue(any(emp[0] == employee_id and emp[3] == 85000 for emp in updated_employee))

    def test_delete_employee(self):
        with self.db_connection as connection:
            self.repository.add_employee('Alice Johnson', 'Product Manager', 90000)
            employees = self.repository.get_all_employees()
            employee_id = next(emp[0] for emp in employees if emp[1] == 'Alice Johnson')
            self.repository.delete_employee(employee_id)
            updated_employees = self.repository.get_all_employees()
            self.assertFalse(any(emp[0] == employee_id for emp in updated_employees))


if __name__ == '__main__':
    unittest.main()
