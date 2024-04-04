from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, DECIMAL, Boolean, ForeignKey, Enum, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from enum import Enum


Base = declarative_base()


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hourlyRate = Column(DECIMAL(10, 2), nullable=False)
    timeSlots = relationship("TimeSlot", back_populates="employee")

    def __init__(self, name, hourlyRate):
        self.name = name
        self.hourlyRate = hourlyRate


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    registrationId = Column(String, nullable=False)
    problemDescription = Column(Text, nullable=False)
    state = Column(Text, nullable=False,
                   default="Created")
    employeeId = Column(Integer, ForeignKey('employees.id'), nullable=False)
    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    estimateDescription = Column(Text)
    estimateCost = Column(DECIMAL(10, 2))
    estimateAccepted = Column(Boolean, default=False)

    pricePaid = Column(DECIMAL(10, 2))
    parts = relationship("Part", back_populates="ticket")

    timeSlots = relationship("TimeSlot", back_populates="ticket")

    def __init__(self, brand, model, registrationId, problemDescription, employeeId ):
        self.brand = brand
        self.model = model
        self.registrationId = registrationId
        self.problemDescription = problemDescription
        self.employeeId = employeeId
        self.estimateCost = 0
        self.estimateAccepted = False
        self.pricePaid = 0
        self.state = "Created"
        


class TimeSlot(Base):
    __tablename__ = 'timeSlots'

    id = Column(Integer, primary_key=True)
    startTime = Column(DateTime(timezone=True), nullable=False)
    endTime = Column(DateTime(timezone=True), nullable=False)
    employeeId = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee", back_populates="timeSlots")
    ticketId = Column(Integer, ForeignKey('tickets.id'))
    ticket = relationship("Ticket", back_populates="timeSlots")

    def __init__(self, startTime, endTime, employeeId, ticketId):
        self.startTime = startTime
        self.endTime = endTime
        self.employeeId = employeeId
        self.ticketId = ticketId


class Part(Base):

    __tablename__ = 'parts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    unitPrice = Column(DECIMAL(10, 2), nullable=False)
    totalPrice = Column(DECIMAL(10, 2), nullable=False)
    ticketId = Column(Integer, ForeignKey('tickets.id'))
    ticket = relationship("Ticket", back_populates="parts")
    
    def __init__(self, name, amount, unitPrice, ticketId):
        self.name = name
        self.amount = amount
        self.unitPrice = unitPrice
        self.totalPrice = float(amount) * float(unitPrice)
        self.ticketId = ticketId


def createDatabase():
    engine = create_engine(
        'postgresql://postgres:12345@localhost:5432/carWorkshop')
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    createDatabase()
