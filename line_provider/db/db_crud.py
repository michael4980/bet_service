import time
import random
from db.db_models import Event
from fastapi import Response
from pydantic_models import EventState
from sqlalchemy import select


class Event_DB(Event):
    """A CRUD class for interacting with the database and managing `Event` objects.

    Args:
        session (Session): A SQLAlchemy database session.

    Attributes:
        session (Session): A SQLAlchemy database session.
    """
    def __init__(self, session) -> None:
        self.session = session

    async def get_all_events(self) -> list:
        """Retrieve all events from the database.

        Returns:
            list: A list of `Event` objects.
        """
        await self.update_state()
        async with self.session as session:
            statement = select(Event).filter_by(state=1)
            result = await session.execute(statement)
            events = result.fetchall()
            events_all = []
            for event in events:
                raw_time = event[0].deadline
                event[0].deadline = self._time_util(raw_time)
                events_all.append(event[0].as_dict())
            return events_all

    async def create_event(self, event_id: int, coefficient: float, deadline: int) -> list:
        """Create a new event in the database with the given parameters.

        Args:
            event_id (int): The ID of the event.
            coefficient (float): The coefficient of the event.
            deadline (int): The deadline of the event (a Unix timestamp).

        Returns:
            list: A dictionary representing the newly created `Event` object.
        """
        check = await self.get_event_by_id(id=event_id)
        if check.status_code == 404:
            event = Event(event_id=event_id,
                          coefficient=coefficient,
                          deadline=deadline,
                          state=EventState.NEW.value)
            async with self.session as session:
                session.add(event)
                await session.commit()
                return event.as_dict()
        return Response('This event_id already using', status_code=403)

    async def get_event_by_id(self, id: int) -> dict:
        """Retrieve an event from the database by its ID.

        Args:
            id (int): The ID of the event to retrieve.

        Returns:
            dict: A dictionary representing the `Event` object with the given ID.
        """
        await self.update_state()
        async with self.session as session:
            statement = select(Event).filter_by(event_id=id)
            event_info = await session.execute(statement)
            event = event_info.first()
            if event is None:
                return Response('No event with this id', status_code=404)
            validator = event._asdict()
            del validator["Event"].id
            timest = validator["Event"].deadline
            validator["Event"].deadline = self._time_util(timest)
            return validator

    async def update_state(self):
        """Update state if deadline is up.

        Returns:
            200 if update is okay
        """
        async with self.session as session:
            statement = select(Event)
            result = await session.execute(statement)
            events = result.fetchall()
            for event in events:
                deadline = event[0].deadline
                state = event[0].state
                if deadline < int(time.time()) and state==1:
                    match_result = random.choice(list(EventState)[1:])
                    event[0].state = match_result.value
                    session.add(event[0])
                    await session.commit()
            return Response('Update successfull', status_code=200)
        
    def _time_util(self, time_to):
        struct_time = time.localtime(time_to)
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)
        return formatted_time