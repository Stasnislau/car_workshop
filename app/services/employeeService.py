from database.database_config import create_session
from database.db_setup import Employee, Ticket, TimeSlot

class documentDTO: 
    def __init__(self, name, hourlyRate, tickets, timeSlots):
        self.name = name
        self.hourlyRate = hourlyRate
        self.tickets = tickets
        self.timeSlots = timeSlots

class EmployeeService:
    def createEmployee(self, name, hourlyRate):
        try:
            hourly_rate = float(hourlyRate)
            if hourly_rate <= 0:
                raise ValueError
            print(f"Creating employee: {name}, {hourlyRate}")
            employee = Employee(name, hourly_rate)
            session = create_session()
            session.add(employee)
            session.commit()
            session.close()
            return True, "Employee created successfully."
        except ValueError:
            return False, "Price per hour must be a positive number."
        except Exception as e:
            return self.handleError(e)

    def getEmployees(self):
        try:
            session = create_session()
            employees = session.query(Employee).all()
            session.close()
            return True, employees
        except Exception as e:
            return self.handleError(e)

    def getEmployee(self, employeeId):
        try:
            session = create_session()
            employee = session.query(Employee).get(employeeId)
            session.close()
            return employee
        except Exception as e:  # Capture the exception
            return self.handleError(e)

    def updateEmployee(self, employeeId, name, hourlyRate):
        try:
            hourly_rate = float(hourlyRate)
            if hourly_rate <= 0:
                raise ValueError
            session = create_session()
            employee = session.query(Employee).get(employeeId)
            employee.name = name
            employee.hourly_rate = hourly_rate
            session.commit()
            session.close()
            return True, "Employee updated successfully."
        except ValueError:
            return False, "Price per hour must be a positive number."
        except Exception as e:
            return self.handleError(e)
    
    def deleteEmployee(self, employeeId):
        try:
            session = create_session()
            employee = session.query(Employee).get(employeeId)
            session.delete(employee)
            session.commit()
            session.close()
            return True, "Employee deleted successfully."
        except Exception as e:
            return self.handleError(e)
        
    def fetchEmployeeDocument(self, employeeId):
        try:
            session = create_session()
            employee = session.query(Employee).get(employeeId)
            tickets = session.query(Ticket).filter_by(employeeId=employeeId).all()
            timeSlots = []
            for ticket in tickets:
                slots = session.query(TimeSlot).filter_by(ticketId=ticket.id).all()
                timeSlots.extend(slots)
            session.close()
            
            dto = documentDTO(employee.name, employee.hourlyRate, tickets, timeSlots)
            return True, dto
        except Exception as e:
            return self.handleError(e)

    def handleError(self, error):
        print(f"Error: {error}")
        return False, "An error occurred. Please try again later."        
