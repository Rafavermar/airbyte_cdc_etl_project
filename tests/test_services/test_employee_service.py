import unittest
from src.services.employee_service import EmployeeService

class TestEmployeeService(unittest.TestCase):
    def setUp(self):
        self.service = EmployeeService()

    def test_add_employee(self):
        self.service.add_employee('John Doe', 'Software Engineer', 70000)
        employees = self.service.get_all_employees()
        self.assertTrue(any(emp[1] == 'John Doe' for emp in employees))
        # Aquí podrías agregar una verificación adicional para asegurar que la sincronización ocurrió

    def test_update_employee_salary(self):
        self.service.add_employee('Jane Doe', 'Data Scientist', 80000)
        employees = self.service.get_all_employees()
        employee_id = next(emp[0] for emp in employees if emp[1] == 'Jane Doe')
        self.service.update_employee_salary(employee_id, 85000)
        updated_employees = self.service.get_all_employees()
        self.assertTrue(any(emp[0] == employee_id and emp[3] == 85000 for emp in updated_employees))
        # Aquí podrías agregar una verificación adicional para asegurar que la sincronización ocurrió

    def test_delete_employee(self):
        self.service.add_employee('Alice Johnson', 'Product Manager', 90000)
        employees = self.service.get_all_employees()
        employee_id = next(emp[0] for emp in employees if emp[1] == 'Alice Johnson')
        self.service.delete_employee(employee_id)
        updated_employees = self.service.get_all_employees()
        self.assertFalse(any(emp[0] == employee_id for emp in updated_employees))
        # Aquí podrías agregar una verificación adicional para asegurar que la sincronización ocurrió

if __name__ == '__main__':
    unittest.main()
