class Employee:
    def __init__(self, employee_id, name, position, salary):
        self.id = employee_id
        self.name = name
        self.position = position
        self.salary = salary

    def __repr__(self):
        return f"Employee(id={self.id}, name={self.name}, position={self.position}, salary={self.salary})"
