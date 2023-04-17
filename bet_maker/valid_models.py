'''Base models to validate requests and states'''
import decimal
import enum

from pydantic import BaseModel


class BetState(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class Bet(BaseModel):
    event_id: int
    bet_amount: decimal.Decimal