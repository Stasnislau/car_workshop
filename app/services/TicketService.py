from datetime import timedelta
import datetime
from database.database_config import create_session
from database.db_setup import Ticket, TimeSlot


class TicketService:
    def createTicket(self, brand, model, registrationId, problemDescription, employeeId, startDate, endDate) -> tuple[bool, str]:
        try:
            if not brand or not model or not registrationId or not problemDescription or not employeeId:
                return False, "All fields are required."
            if not startDate or not endDate:
                return False, "Start date and end date required."
            print(
                f"Creating ticket: {brand}, {model}, {registrationId}, {problemDescription}, {employeeId}")
            ticket = Ticket(brand, model, registrationId,
                            problemDescription, employeeId)

            session = create_session()
            session.add(ticket)
            session.flush()
            timeSlot = TimeSlot(
                startDate, endDate, employeeId, ticket.id)
            session.add(timeSlot)
            session.commit()
            session.close()
            return True, "Ticket created successfully."
        except Exception as e:
            return self.handleError(e)

    def getTicket(self, ticketId) -> tuple[bool, str | Ticket]:
        try:
            session = create_session()
            ticket = session.query(Ticket).get(ticketId)
            session.close()
            return ticket
        except Exception as e:
            return self.handleError(e)

    def getTickets(self) -> tuple[bool, list | str]:
        try:
            session = create_session()
            tickets = session.query(Ticket).all()
            session.close()
            return True, tickets
        except Exception as e:
            return self.handleError(e)

    def getEmployeeTickets(self, employeeId) -> tuple[bool, list | str]:
        try:
            session = create_session()
            tickets = session.query(Ticket).filter_by(
                employeeId=employeeId).all()
            session.close()
            return True, tickets
        except Exception as e:
            return self.handleError(e)

    def updateTicket(self, ticketId, brand, model, registrationId, problemDescription) -> tuple[bool, str]:
        try:
            session = create_session()
            ticket = session.query(Ticket).get(ticketId)
            ticket.brand = brand
            ticket.model = model
            ticket.registrationId = registrationId
            ticket.problemDescription = problemDescription
            session.commit()
            session.close()
            return True, "Ticket updated successfully."
        except Exception as e:
            return self.handleError(e)

    def deleteTicket(self, ticketId) -> tuple[bool, str]:
        try:
            session = create_session()
            ticket = session.query(Ticket).get(ticketId)
            session.delete(ticket)
            session.commit()
            session.close()
            return True, "Ticket deleted successfully."
        except Exception as e:
            return self.handleError(e)

    def getTicketTimeSlots(self, ticketId) -> tuple[bool, list | str]:
        try:
            session = create_session()
            timeSlots = session.query(TimeSlot).filter_by(
                ticketId=ticketId).all()
            session.close()
            return True, timeSlots
        except Exception as e:
            return self.handleError(e)

    def updateTicketTimeSlot(self, timeSlotId, startTime, endTime, employeeId) -> tuple[bool, str]:
        try:
            session = create_session()
            timeSlot = session.query(TimeSlot).get(timeSlotId)
            timeSlot.startTime = startTime
            timeSlot.endTime = endTime
            timeSlot.employeeId = employeeId
            session.commit()
            session.close()
            return True, "Time slot updated successfully."
        except Exception as e:
            return self.handleError(e)
        
    def approvePreliminary(self, ticketId) -> tuple[bool, str]:
        try:
            session = create_session()
            ticket = session.query(Ticket).get(ticketId)
            if ticket.estimateAccepted:
                return False, "Ticket already approved."
            ticket.estimateAccepted = True
            session.commit()
            session.close()
            return True, "Ticket approved successfully."
        except Exception as e:
            return self.handleError(e)

    def deleteTicketTimeSlot(self, timeSlotId) -> tuple[bool, str]:
        try:
            session = create_session()
            timeSlot = session.query(TimeSlot).get(timeSlotId)
            session.delete(timeSlot)
            session.commit()
            session.close()
            return True, "Time slot deleted successfully."
        except Exception as e:
            return self.handleError(e)

    def handleError(self, error) -> tuple[bool, str]:
        print(f"Error: {error}")
        return False, "An error occurred. Please try again later."
