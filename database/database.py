from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.orm.exc import DetachedInstanceError
from sqlalchemy import Table, Column, Integer, String, LargeBinary, DateTime, MetaData, ForeignKey, create_engine
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    workouts = relationship("Workout", backref="user")

    # def __repr__(self):
    #     return self._repr(id=self.id, name=self.name, age=self.age)


class Workout(Base):
    __tablename__ = "Workout"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("User.id"))
    workout_type = Column(String, nullable=False)
    repetitions = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    faults = relationship("Faults", backref="workout")

    # def __repr__(self):
    #     return self._repr(id=self.id, user_id=self.user_id, workout_type=self.workout_type,
    #                       repetitions=self.repetitions, duration=self.duration)


class Faults(Base):
    __tablename__ = "Faults"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    screenshot = Column(LargeBinary, nullable=True)
    workout_id = Column(Integer, ForeignKey("Workout.id"))

    # def __repr__(self):
    #     return self._repr(id=self.id, description=self.description, date=self.date,
    #                       screenshot=self.screenshot, workout_id=self.workout_id)

engine = create_engine("mssql://@DESKTOP-80E4OFB\SQLEXPRESS/AI_Workout_DB?driver=ODBC Driver 17 for SQL Server")


def connect_to_db():
    conn = engine.connect()
    Base.metadata.create_all(engine)


def send_in_db(instance: Base):
    with Session(engine) as session:
        session.add(instance)
        session.commit()


def retrieve_from_db(instance: Base):
    with Session(engine) as session:
        return session.query(instance).all()
