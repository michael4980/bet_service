import os
import uuid

import httpx
from db_bet.bet_models import Bet
from dotenv import load_dotenv
from sqlalchemy import select
from valid_models import BetState

load_dotenv()
api_host = os.getenv("EVENT_API_HOST")
api_port = os.getenv("EVENT_API_PORT")


class Bet_DB(Bet):
    """A class representing a database of bets.

    Attributes:
        session (sqlalchemy.orm.Session): A database session object used for querying the database.
    """

    def __init__(self, session) -> None:
        self.session = session

    async def create_bet(self, event_id: int, amount: float) -> str:
        """
        Creates a new bet and adds it to the database.

        Args:
            event_id (int): The ID of the event for which the bet is being placed.
            amount (float): The amount being bet.

        Returns:
            str: The ID of the newly created bet.
        """
        bet = Bet(bet_id=uuid.uuid4().hex,
                  event_id=event_id,
                  bet_amount=amount,
                  bet_state=BetState.NEW.value)
        async with self.session as session:
            session.add(bet)
            await session.commit()
            return bet.as_dict()

    async def get_all_bets(self) -> list:
        """
        Gets all bets from the database and updates the state.

        Returns:
            list: A list of dictionaries representing the bets in the database.
        """
        async with self.session as session:
            statement = select(Bet)
            result = await session.execute(statement)
            bets = result.fetchall()
            bets_all = []
            for bet in bets:
                if bet[0].bet_state == 1:
                    result = await self._update_bet_state(event_id=bet[0].event_id)
                    bets_all.append(result)
                else:
                    bets_all.append(bet[0].as_dict())
            return bets_all

    async def _update_bet_state(self, event_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{api_host}:{api_port}/get_event/{event_id}')
        values = response.json()
        async with self.session as session:
            statement = select(Bet).filter_by(event_id=event_id)
            result = await session.execute(statement)
            bet = result.first()
            bet[0].bet_state = values['Event']['state']
            session.add(bet[0])
            await session.commit()
            return bet[0].as_dict()
