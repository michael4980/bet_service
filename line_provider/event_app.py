import time

import fastapi
from db.db_crud import Event_DB
from pydantic_models import Event
from session import create_sessionmaker

app = fastapi.FastAPI()


async def get_session():
    return await create_sessionmaker()


@app.on_event("startup")
async def startup():
    app.state.sessionmaker = await get_session()


@app.post('/create_event/')
async def create_event(request: Event):
    start_session = Event_DB(session=app.state.sessionmaker())
    deadline = int(time.time()) + request.deadline
    response = await start_session.create_event(request.event_id, request.coefficient, deadline)
    return response


@app.get('/get_event/{event_id}')
async def get_event(event_id: int):
    start_session = Event_DB(session=app.state.sessionmaker())
    result = await start_session.get_event_by_id(id=event_id)
    return result


@app.get('/get_events/')
async def get_all_events():
    start_session = Event_DB(session=app.state.sessionmaker())
    result = await start_session.get_all_events()
    return result
