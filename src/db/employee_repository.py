from src.db.base_repository import BaseRepository


class EmployeeRepository(BaseRepository):
    def get_all_employees(self):
        query = "SELECT id, name, position, salary FROM employees"
        return self.fetch_all(query)

    def add_employee(self, name, position, salary):
        query = "INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s)"
        self.execute_query(query, (name, position, salary))

    def update_employee_salary(self, employee_id, new_salary):
        query = "UPDATE employees SET salary = %s WHERE id = %s"
        self.execute_query(query, (new_salary, employee_id))

    def delete_employee(self, employee_id):
        query = "DELETE FROM employees WHERE id = %s"
        self.execute_query(query, (employee_id,))
