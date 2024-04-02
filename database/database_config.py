from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_session():
    engine = create_engine('postgresql://postgres:12345@localhost:5432/carWorkshop')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session