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
    hourly_rate = Column(DECIMAL(10, 2), nullable=False)
    time_slots = relationship("TimeSlot", back_populates="employee")


class TimeSlot(Base):
    __tablename__ = 'time_slots'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship("Employee", back_populates="time_slots")
    tickets = relationship("TicketTimeSlot", back_populates="time_slot")


ticket_time_slot_table = Table(
    'ticket_time_slots',
    Base.metadata,
    Column('ticket_id', Integer, ForeignKey('tickets.id'), primary_key=True),
    Column('time_slot_id', Integer, ForeignKey(
        'time_slots.id'), primary_key=True)
)


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    registration_id = Column(String, nullable=False)
    problem_description = Column(Text, nullable=False)
    state = Column(Text, nullable=False,
                   default="Created")
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    estimate_description = Column(Text)
    estimate_cost = Column(DECIMAL(10, 2))
    estimate_accepted = Column(Boolean, default=False)

    price_paid = Column(DECIMAL(10, 2))
    time_slots = relationship("TicketTimeSlot", back_populates="ticket")
    parts = relationship("Part", back_populates="ticket")
    work_logs = relationship("WorkLog", back_populates="ticket")


class Part(Base):

    __tablename__ = 'parts'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    unit_price = Column(DECIMAL(10, 2), nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    ticket = relationship("Ticket", back_populates="parts")


class WorkLog(Base):

    __tablename__ = 'work_logs'

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    time_slot_id = Column(Integer, ForeignKey('time_slots.id'))
    ticket_id = Column(Integer, ForeignKey('tickets.id'))

    ticket = relationship("Ticket", back_populates="work_logs")
    employee = relationship("Employee", back_populates="work_logs")
    time_slot = relationship("TimeSlot", back_populates="work_logs")


def create_database():
    engine = create_engine(
        'postgresql://postgres:12345@localhost:5432/car_workshop')
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_database()
