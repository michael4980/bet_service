from sqlalchemy import Column, Integer, Numeric
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer)
    coefficient = Column(Numeric(precision=10, scale=2))
    deadline = Column(Integer)
    state = Column(Integer)

    def as_dict(self):
        return {
            'event_id': self.event_id,
            'coefficient': float(self.coefficient),
            'deadline': self.deadline,
            'state': self.state
        }
