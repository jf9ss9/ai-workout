#from log.logconfig import logger
from database.credentials import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy import Table, Column, Integer, String, LargeBinary, DateTime, MetaData, ForeignKey, create_engine
from sqlalchemy import func

Base = declarative_base()


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    password = Column(String, nullable=False)
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


def register_user(username: str, name: str, age: int, password: str) -> bool:
    with Session(engine) as session:
        try:
            session.add(User(username=username, name=name, age=age, password=create_bcrypt_hash(password)))
            session.commit()
        except IntegrityError:
            print("Username already taken.")
            #logger.warning("Username already taken")
            return False
        else:
            return True


def verify_user(username: str, password: str) -> bool:
    with Session(engine) as session:
        row = session.query(User).filter(User.username == username).first()
        if row is not None:
            hashed_password = row.password
        else:
            print(f"Username: {username} not found")
            #logger.warning(f"Username: {username} not found")
    return verify_password(password, hashed_password)


def create_workout(user_id: int, workout_type: str, repetitions: int, duration):
    with Session(engine) as session:
        session.add(Workout(user_id=user_id, workout_type=workout_type, repetitions=repetitions, duration=duration))
        session.commit()


def get_user(username: str):
    with Session(engine) as session:
        return session.query(User).filter(User.username == username).first()


def send_in_db(instance: Base):
    with Session(engine) as session:
        session.add(instance)
        session.commit()


def retrieve_from_db(instance: Base):
    with Session(engine) as session:
        return session.query(instance).all()


def get_max_workout_id():
    with Session(engine) as session:
        row = session.query(func.max(Workout.id)).first()
        return row[0] if row is not None else 0


if __name__ == "__main__":
    connect_to_db()


