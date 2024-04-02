from database.database_config import create_session
from database.db_setup import Employee


class EmployeeService:
    def createEmployee(self, name, hourly_rate):
        # Ensure price per hour is a valid number
        try:
            hourly_rate = float(hourly_rate)
            if hourly_rate <= 0:
                raise ValueError
        except ValueError:
            return False, "Price per hour must be a positive number."

        print(f"Creating employee: {name}, {hourly_rate}")
        # put the employee in the database
        employee = Employee(name, hourly_rate)
        session = create_session()
        session.add(employee)
        session.commit()
        session.close()
        return True, employee
