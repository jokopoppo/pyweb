import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

def regismember(user,password):
    engine = create_engine('sqlite:///tutorial.db', echo=True)

    # create a Session
    Session = sessionmaker(bind=engine)
    session = Session()

    user = User(user,password)
    session.add(user)

    # commit the record the database
    session.commit()

    session.commit()

