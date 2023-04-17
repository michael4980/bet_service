# Bet services

## Description
Bet Services is a project that consists of two services: bet_maker and line_provider. The bet_maker service allows users to create a wallet and place bets on events. The line_provider service provides information about events, including their odds and outcomes.

## Features
Features for the bet_maker app:

 - Make a bet on a specific event and update the bet state accordingly
 - View the bet history
 - Retrieve the details of a specific bet

Features for the line_provider app:

 - Create an event with a given ID, coefficient, and deadline time and save it to the database
 - Retrieve the details of a specific event by its ID
 - Retrieve all the events in the database with their details.

## Technologies Used
 - Python
 - FastAPI
 - Docker
 - PostgreSQL

## Getting Started
1. Clone the repository to your PC
2. create .env file like in example:
```
DB_NAME=postgres
DB_HOST=db_event
DB_PORT=5433
DB_USER=postgres
DB_PASS=mypassword
DB_BET_NAME=postgres
DB_BET_HOST=db_bet
DB_BET_PORT=5432
DB_BET_USER=postgres
DB_BET_PASS=mypassword
EVENT_API_HOST=
EVENT_API_PORT=8086
```
3. In the project directory, run the following command:
```
docker-compose up --build -d
```
## License
This project is licensed under the MIT License - see the LICENSE.md file for details.