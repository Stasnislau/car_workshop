from database.database_config import create_session
from database.db_setup import Part
from .ticketService import TicketService

class PartService:
    def createPart(self, ticketId, name, amount, unitPrice) -> tuple[bool, str]:
        try:
            if not name or not amount or not unitPrice:
                return False, "All fields are required."
            session = create_session()
            part = Part( name, amount, unitPrice, ticketId)
            session.add(part)
            session.commit()
            TicketService().recalculateExpanses(part.ticketId)
            session.close()
            
            return True, "Part created successfully."
        except Exception as e:
            return self.handleError(e)

    def updatePart(self, partId, name, amount, unitPrice) -> tuple[bool, str]:
        try:
            if not name or not amount or not unitPrice:
                return False, "All fields are required."
            
            session = create_session()
            part = session.query(Part).get(partId)
            part.name = name
            part.amount = amount
            part.unitPrice = unitPrice
            session.commit()
            TicketService().recalculateExpanses(part.ticketId)
            session.close()
            
            return True, "Part updated successfully."
        except Exception as e:
            return self.handleError(e)

    def deletePart(self, partId) -> tuple[bool, str]:
        try:
            session = create_session()
            part = session.query(Part).get(partId)
            session.delete(part)
            session.commit()
            TicketService().recalculateExpanses(part.ticketId)
            session.close()
            return True, "Part deleted successfully."
        except Exception as e:
            return self.handleError(e)

    def getPartsForTicket(self, ticketId) -> tuple[bool, list | str]:
        try:
            session = create_session()
            parts = session.query(Part).filter_by(ticketId=ticketId).all()
            session.close()
            
            return True, parts
        except Exception as e:
            return self.handleError(e)

    def handleError(self, error) -> tuple[bool, str]:
        print(f"Error: {error}")
        return False, "An error occurred. Please try again later."
