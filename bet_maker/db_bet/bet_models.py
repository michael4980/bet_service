from sqlalchemy import Column, Integer, Numeric, String, CheckConstraint
from sqlalchemy.orm import declarative_base
Base = declarative_base()


class Bet(Base):
    __tablename__ = 'bets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bet_id = Column(String)
    event_id = Column(Integer)
    bet_amount = Column(Numeric(precision=10, scale=2),
                        CheckConstraint('bet_amount > 0'))
    bet_state = Column(Integer)

    def as_dict(self):
        return {
            'bet_id': self.bet_id,
            'event_id': self.event_id,
            'bet_amount': float(self.bet_amount),
            'bet_state': self.bet_state
        }
