from database.database_config import create_session
from database.db_setup import Ticket, TimeSlot, Employee
from .ticketService import TicketService

class TimeSlotDTO:
    def __init__(self, startTime, endTime, employeeId, ticketId, registrationId):
        self.startTime = startTime
        self.endTime = endTime
        self.employeeId = employeeId
        self.ticketId = ticketId
        self.registrationId = registrationId
   
class TimeService: 
    def createTimeSlot(self, startTime, endTime, employeeId, ticketId) -> tuple[bool, str]:
        try:
            if not startTime or not endTime or not employeeId or not ticketId:
                return False, "All fields are required."
            session = create_session()
            timeSlot = TimeSlot(startTime, endTime, employeeId, ticketId)
            session.add(timeSlot)
            session.commit()
            session.close()
            return True, "Time slot created successfully."
        except Exception as e:
            return self.handleError(e)

    def getTimeSlotsForTicket(self, ticketId) -> tuple[bool, list | str]:
        try:
            session = create_session()
            timeSlots = session.query(TimeSlot).filter_by(ticketId=ticketId).all()
            session.close()
            return True, timeSlots
        except Exception as e:
            return self.handleError(e)
        
    def getTimeSlot(self, timeSlotId) -> tuple[bool, str | TimeSlot]:
        try:
            session = create_session()
            timeSlot = session.query(TimeSlot).get(timeSlotId)
            session.close()
            return True, timeSlot
        except Exception as e:
            return self.handleError(e)
        
    def getTimeSlotsForEmployee(self, employeeId) -> tuple[bool, list | str]:
        try:
            session = create_session()
            tickets = session.query(Ticket).filter_by(employeeId=employeeId).all()
            if not tickets:
                session.close()
                return False, "No time slots found for this employee."
            else:
                timeSlots = []
                for ticket in tickets:
                    gotTimeSlots = session.query(TimeSlot).filter_by(ticketId=ticket.id).all()
                    
                    for gotTimeSlot in gotTimeSlots:
                        newTimeSlot = TimeSlotDTO(gotTimeSlot.startTime, gotTimeSlot.endTime, gotTimeSlot.employeeId, gotTimeSlot.ticketId, ticket.registrationId)
                    timeSlots.append(newTimeSlot)
                session.close()
                return True, timeSlots
        except Exception as e:
            return self.handleError(e)
                    
            

    def deleteTimeSlot(self, timeSlotId) -> tuple[bool, str]:
        try:
            session = create_session()
            timeSlot = session.query(TimeSlot).get(timeSlotId)
            session.delete(timeSlot)
            session.commit()
            TicketService().recalculateExpanses(timeSlot.ticketId)
            session.close()
            return True, "Time slot deleted successfully."
        except Exception as e:
            return self.handleError(e)
        
    def updateTimeSlot(self, timeSlotId, startTime, endTime) -> tuple[bool, str]:
        try:
            if not startTime or not endTime:
                return False, "All fields are required."
            session = create_session()
            timeSlot = session.query(TimeSlot).get(timeSlotId)
            timeSlot.startTime = startTime
            timeSlot.endTime = endTime
            session.commit()
            TicketService().recalculateExpanses(timeSlot.ticketId)
            session.close()
            return True, "Time slot updated successfully."
        except Exception as e:
            return self.handleError(e)
        
    
    def handleError(self, e):
        print(e)
        return False, "An error occurred. Please try again later."