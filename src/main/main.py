import time
from src.services.employee_service import EmployeeService
from src.db.connection import initialize_database

def main():
    # # Inicializar la base de datos y crear la tabla si no existe
    # try:
    #     initialize_database()
    # except Exception as e:
    #     print(f"Error during database initialization: {e}")
    #     return

    # Crear una instancia del servicio de empleados
    employee_service = EmployeeService()

    time.sleep(35)

    # Insertar empleados iniciales
    print("Insertando empleados iniciales...")
    employee_service.add_employee('John Doe', 'Data Engineer', 70000)
    employee_service.add_employee('Jane Smith', 'Data Scientist', 80000)

    # Esperar unos segundos para asegurar que las operaciones se completen
    time.sleep(35)

    # Sincronizar los cambios con Airbyte
    print("Sincronizando los cambios con Airbyte después de la inserción inicial...")
    employee_service.trigger_sync()

    # Esperar unos segundos para asegurar que la sincronización se complete
    time.sleep(35)

    # Mostrar todos los empleados
    print("Empleados después de la inserción inicial:")
    employees = employee_service.get_all_employees()
    for emp in employees:
        print(emp)

    # Actualizar salario de un empleado
    print("Actualizando salario de John Doe...")
    employee_id = next(emp[0] for emp in employees if emp[1] == 'John Doe')
    employee_service.update_employee_salary(employee_id, 75000)

    # Esperar unos segundos para asegurar que las operaciones se completen
    time.sleep(35)

    # Sincronizar los cambios con Airbyte
    print("Sincronizando los cambios con Airbyte después de actualizar el salario de John Doe...")
    employee_service.trigger_sync()

    # Esperar unos segundos para asegurar que la sincronización se complete
    time.sleep(45)

    # Mostrar todos los empleados después de la actualización
    print("Empleados después de actualizar el salario de John Doe:")
    employees = employee_service.get_all_employees()
    for emp in employees:
        print(emp)

    # Eliminar un empleado
    print("Eliminando a Jane Smith...")
    employee_id = next(emp[0] for emp in employees if emp[1] == 'Jane Smith')
    employee_service.delete_employee(employee_id)

    data_engineers = [emp for emp in employees if emp[2] == 'Data Engineer']
    if len(data_engineers) > 0:
        employee_service.delete_employee(data_engineers[0][0])
    if len(data_engineers) > 1:
        employee_service.delete_employee(data_engineers[1][0])

    # Esperar unos segundos para asegurar que las operaciones se completen
    time.sleep(75)

    # Sincronizar los cambios con Airbyte
    print("Sincronizando los cambios con Airbyte después de eliminar a Jane Smith...")
    employee_service.trigger_sync()

    # Esperar unos segundos para asegurar que la sincronización se complete
    time.sleep(45)

    # Mostrar todos los empleados después de la eliminación
    print("Empleados después de eliminar a Jane Smith:")
    employees = employee_service.get_all_employees()
    for emp in employees:
        print(emp)


if __name__ == "__main__":
    main()