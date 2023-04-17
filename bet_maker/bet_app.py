import os

import fastapi
import httpx
from bet_session import create_sessionmaker
from db_bet.bet_crud import Bet_DB
from dotenv import load_dotenv
from fastapi import Response
from valid_models import Bet

load_dotenv()
api_host = os.getenv("EVENT_API_HOST")
api_port = os.getenv("EVENT_API_PORT")


app = fastapi.FastAPI()


async def get_session():
    return await create_sessionmaker()


@app.on_event("startup")
async def startup():
    app.state.sessionmaker = await get_session()


@app.get('/events/')
async def get_events():
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{api_host}:{api_port}/get_events/')
    response = response.json()
    if not response:
        return Response('Sorry, we don`t have active events atm, stay tuned', status_code=200)
    return response


@app.post('/bet/')
async def make_bet(request: Bet):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{api_host}:{api_port}/get_event/{request.event_id}')
    if response.status_code == 404:
        return Response('Event doesn`t exist', status_code=404)
    else:
        values = response.json()
        if values['Event']['state'] != 1:
            return Response('Event ended', status_code=404)
    start_session = Bet_DB(session=app.state.sessionmaker())
    response = await start_session.create_bet(request.event_id, request.bet_amount)
    return response


@app.get('/bets/')
async def get_all_bets():
    start_session = Bet_DB(session=app.state.sessionmaker())
    result = await start_session.get_all_bets()
    return result
